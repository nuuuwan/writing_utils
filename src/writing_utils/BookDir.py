import os
import sys
from functools import cached_property
from typing import Generator

from utils import FileOrDirectory, Log

from writing_utils.BookDirLaTeXMixin import BookDirLaTeXMixin
from writing_utils.BookDirUtilsMixin import BookDirUtilsMixin
from writing_utils.ChapterFile import ChapterFile

log = Log("BookDir")


class BookDir(FileOrDirectory, BookDirUtilsMixin, BookDirLaTeXMixin):
    # Construction
    @classmethod
    def from_args_or_environs(cls) -> "BookDir":
        return BookDir(
            sys.argv[1]
            if len(sys.argv) > 1
            else os.environ["DIR_WRITING_DEFAULT_PROJECT_DIR"]
        )

    # Data Access
    def gen_chapter_docs(self) -> Generator[ChapterFile, None, None]:
        for file_name in os.listdir(self.path):
            if file_name.endswith(".md"):
                yield ChapterFile(os.path.join(self.path, file_name))

    def get_name_map_from_titles(self) -> dict[str, str]:
        name_map = {}
        for chapter_doc in self.gen_chapter_docs():
            new_file_name = (
                f"{chapter_doc.number:02d}-{chapter_doc.title_cleaned}.md"
            )
            if new_file_name:
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
