import os
import shutil
import sys
import unittest

from utils import File

from writing_utils import BookDir

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


class TestDocXRoundTrip(unittest.TestCase):
    CHAPTER1_CONTENT = """# 1. First Chapter

"This is a QUOTE"

*This text is italicized.*

**This text is bold.**

This is the first chapter with some text.

It has multiple paragraphs.
This is the second paragraph.

---

Some more stuff. And more stuff.

"But Neth's guts have already tightened"

---

**Later**


"""

    CHAPTER2_CONTENT = """# 2. Second Chapter

This is the second chapter.

Another paragraph here.
"""

    def setUp(self):
        self.dir_test_output = os.path.join(
            "tests", "output", "test_roundtrip"
        )
        shutil.rmtree(self.dir_test_output, ignore_errors=True)
        os.makedirs(self.dir_test_output, exist_ok=True)
        self._setup_chapters()

    def _setup_chapters(self):
        self.dir_book = os.path.join(self.dir_test_output, "original_book")
        os.makedirs(self.dir_book, exist_ok=True)
        chapter1_path = os.path.join(self.dir_book, "01-First_Chapter.md")
        chapter2_path = os.path.join(self.dir_book, "02-Second_Chapter.md")
        File(chapter1_path).write(self.CHAPTER1_CONTENT)
        File(chapter2_path).write(self.CHAPTER2_CONTENT)

    def tearDown(self):
        pass

    def test_docx_roundtrip(self):
        book_dir1 = BookDir(self.dir_book)
        book_dir1.clean_and_write_all()

        docx_file_path = book_dir1.build_docx()
        self.assertTrue(
            os.path.exists(docx_file_path), "DOCX file was not created"
        )

        book_dir2 = BookDir.from_docx(docx_file_path)
        self.assertEqual(book_dir1, book_dir2)

    def test_md_roundtrip(self):
        book_dir1 = BookDir(self.dir_book)
        book_dir1.clean_and_write_all()

        md_file_path = book_dir1.build_md()
        self.assertTrue(
            os.path.exists(md_file_path), "Markdown file was not created"
        )

        output_dir = self.dir_book + ".dir_from_md"
        book_dir3 = BookDir.from_md(
            md_file_path,
            output_dir,
        )
        self.assertEqual(book_dir1, book_dir3)


if __name__ == "__main__":
    unittest.main()
