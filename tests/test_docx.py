import os
import shutil
import sys
import tempfile
import unittest

from utils import File

from writing_utils import BookDir

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


class TestDocXRoundTrip(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp(prefix="test_bookdir_")

    def tearDown(self):
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_docx_roundtrip(self):
        chapter1_content = """# 1. First Chapter

This is the first chapter with some text.

It has multiple paragraphs.
This is the second paragraph.
"""

        chapter2_content = """# 2. Second Chapter

This is the second chapter.

Another paragraph here.
"""

        chapter1_path = os.path.join(self.temp_dir, "01-First_Chapter.md")
        chapter2_path = os.path.join(self.temp_dir, "02-Second_Chapter.md")
        File(chapter1_path).write(chapter1_content)
        File(chapter2_path).write(chapter2_content)
        book_dir1 = BookDir(self.temp_dir)
        book_dir1.clean_all()

        book_dir1.build_docx()
        docx_file_path = self.temp_dir + ".docx"
        self.assertTrue(
            os.path.exists(docx_file_path), "DOCX file was not created"
        )

        book_dir2 = BookDir.from_docx(docx_file_path)

        self.assertEqual(book_dir1, book_dir2)


if __name__ == "__main__":
    unittest.main()
