import os
import random

from utils import Log

log = Log("BookDir")


class BookDirUtilsMixin:

    def clean_all(self):
        n_cleaned = 0
        for chapter_doc in self.gen_chapter_docs():
            if chapter_doc.clean():
                n_cleaned += 1
        log.info(f"🧹 Cleaned {n_cleaned} chapters.")

    def rename_files(self, name_map: dict[str, str]):
        n_renamed = 0
        for old_file_name, new_file_name in name_map.items():
            if old_file_name == new_file_name:
                continue
            log.info(f"'    - {old_file_name}' -> '{new_file_name}'")
            os.rename(
                os.path.join(self.path, old_file_name),
                os.path.join(self.path, new_file_name),
            )
            n_renamed += 1
        log.info(f"↔️  Renamed {n_renamed} chapters.")

    def randomize_titles(self):
        chapter_docs = [cd for cd in self.gen_chapter_docs()]
        random.shuffle(chapter_docs)
        for i_chapter, chapter_doc in enumerate(chapter_docs, start=1):
            chapter_doc.number = i_chapter

    def print_statistics(self):
        log.info(f"n_chars={self.n_chars:,}")
        log.info(f"n_words={self.n_words:,}")

    def open(self):
        os.system(f'open "{self.path}"')
