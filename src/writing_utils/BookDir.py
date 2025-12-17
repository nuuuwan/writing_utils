import os
import shutil
import sys
from functools import cached_property
from typing import Generator

from utils import FileOrDirectory, Log, Time, TimeFormat

from writing_utils.BookDirDocXMixin import BookDirDocXMixin
from writing_utils.BookDirLaTeXMixin import BookDirLaTeXMixin
from writing_utils.BookDirMarkdownMixin import BookDirMarkdownMixin
from writing_utils.BookDirReverseDocXMixin import BookDirReverseDocXMixin
from writing_utils.BookDirUtilsMixin import BookDirUtilsMixin
from writing_utils.ChapterFile import ChapterFile

log = Log("BookDir")


class BookDir(
    FileOrDirectory,
    BookDirUtilsMixin,
    BookDirLaTeXMixin,
    BookDirDocXMixin,
    BookDirMarkdownMixin,
    BookDirReverseDocXMixin,
):
    # Construction
    @classmethod
    def from_args_or_environs(cls) -> "BookDir":
        return BookDir(
            sys.argv[1]
            if len(sys.argv) > 1
            and os.path.exists(sys.argv[1])
            and os.path.isdir(sys.argv[1])
            else os.environ["DIR_WRITING_DEFAULT_PROJECT_DIR"]
        )

    # Data Access
    def gen_chapter_docs(self) -> Generator[ChapterFile, None, None]:
        file_names = sorted(os.listdir(self.path))
        for file_name in file_names:
            if file_name.endswith(".md"):
                yield ChapterFile(os.path.join(self.path, file_name))

    def get_name_map_from_titles(self) -> dict[str, str]:
        name_map = {}
        for i_chapter, chapter_doc in enumerate(
            self.gen_chapter_docs(), start=1
        ):
            new_file_name = f"{i_chapter:02d}-{chapter_doc.title_cleaned}.md"
            old_file_name = os.path.basename(chapter_doc.path)
            name_map[old_file_name] = new_file_name
        return name_map

    # Properties
    @cached_property
    def n_chars(self) -> int:
        return sum(
            [chapter_doc.n_chars for chapter_doc in self.gen_chapter_docs()]
        )

    @cached_property
    def n_words(self) -> int:
        return sum(
            [chapter_doc.n_words for chapter_doc in self.gen_chapter_docs()]
        )

    def find(self, search_key: str):
        for chapter_doc in self.gen_chapter_docs():
            for find_info in chapter_doc.find(search_key):
                yield find_info

    def replace(self, find_text: str, replace_text: str):
        n_replace_files = 0
        for chapter_doc in self.gen_chapter_docs():
            if chapter_doc.replace(find_text, replace_text):
                n_replace_files += 1

        log.info(
            f'Replaced "{find_text}" with "{replace_text}"'
            + f" in {n_replace_files} chapters."
        )
        return n_replace_files > 0

    def backup(self):
        ts = TimeFormat.TIME_ID.format(Time.now())
        backup_dir_path = f"{self.path}.backup.{ts}"
        shutil.copytree(self.path, backup_dir_path)
        log.info(f"Wrote {backup_dir_path}")

    def __eq__(self, other):
        if not isinstance(other, BookDir):
            return False

        self_chapters = list(self.gen_chapter_docs())
        other_chapters = list(other.gen_chapter_docs())

        if len(self_chapters) != len(other_chapters):
            log.debug(
                f"Different number of chapters: {
                    len(self_chapters)} vs {
                    len(other_chapters)}"
            )
            return False

        for self_chapter, other_chapter in zip(self_chapters, other_chapters):
            if self_chapter != other_chapter:
                log.debug(
                    f"Different chapter contents: {self_chapter} vs {other_chapter}"
                )
                return False

        return True
