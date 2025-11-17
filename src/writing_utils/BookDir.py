import os
import random
import sys
from functools import cached_property
from typing import Generator

from utils import FileOrDirectory, Log

from writing_utils.ChapterFile import ChapterFile

log = Log("BookDir")


class BookDir(FileOrDirectory):

    @classmethod
    def from_args_or_environs(cls) -> "BookDir":
        return BookDir(
            sys.argv[1]
            if len(sys.argv) > 1
            else os.environ["DIR_WRITING_DEFAULT_PROJECT_DIR"]
        )

    def gen_chapter_docs(self) -> Generator[ChapterFile, None, None]:
        for file_name in os.listdir(self.path):
            if file_name.endswith(".md"):
                yield ChapterFile(os.path.join(self.path, file_name))

    def get_name_map_from_titles(self) -> dict[str, str]:
        name_map = {}
        for chapter_doc in self.gen_chapter_docs():
            new_file_name = (
                f"{chapter_doc.number}-{chapter_doc.title_cleaned}.md"
            )
            if new_file_name:
                old_file_name = os.path.basename(chapter_doc.path)
                name_map[old_file_name] = new_file_name
        return name_map

    def randomize_titles(self):
        chapter_docs = [cd for cd in self.gen_chapter_docs()]
        random.shuffle(chapter_docs)
        for i_chapter, chapter_doc in enumerate(chapter_docs):
            chapter_doc.number = i_chapter

    def rename_files(self, name_map: dict[str, str]):
        n_renamed = 0
        for old_file_name, new_file_name in name_map.items():
            if old_file_name == new_file_name:
                continue
            log.info(f"'{old_file_name}' -> '{new_file_name}'")
            os.rename(
                os.path.join(self.path, old_file_name),
                os.path.join(self.path, new_file_name),
            )
            n_renamed += 1
        log.info(f"Renamed {n_renamed} files.")

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
