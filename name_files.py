import os
import sys
from functools import cached_property

from utils import File, Log

log = Log("name_files")


class ChapterDoc:

    def __init__(self, file_path):
        self.file_path = file_path

    @cached_property
    def lines(self):
        return File(self.file_path).read_lines()

    @property
    def file_name_from_title(self):
        lines = self.lines
        first_line = lines[0]
        if first_line.startswith("# ") and "." in first_line:
            title = first_line[2:].partition(".")[-1].strip()
            file_name = (
                title.lower().replace(" ", "-").replace(".", "-") + ".md"
            )
            return file_name
        return None

    @classmethod
    def gen_from_dir(cls, dir_path: str):
        for file_name in os.listdir(dir_path):
            if file_name.endswith(".md"):
                yield cls(os.path.join(dir_path, file_name))

    @classmethod
    def rename_files(cls, dir_path: str):
        name_pairs = []
        for chapter_doc in cls.gen_from_dir(dir_path):
            new_file_name = chapter_doc.file_name_from_title
            if new_file_name:
                new_file_path = os.path.join(dir_path, new_file_name)
                name_pair = (chapter_doc.file_path, new_file_path)
                name_pairs.append(name_pair)

        name_pairs.sort(key=lambda pair: pair[1])
        for old_file_path, new_file_path in name_pairs:
            log.info(f"Renaming '{old_file_path}' to '{new_file_path}'")
            os.rename(old_file_path, new_file_path)


if __name__ == "__main__":

    ChapterDoc.rename_files(dir_path=sys.argv[1])
