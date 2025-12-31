import os
import sys
import unittest

from utils import File

from writing_utils import BookDir

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


class TestDocXRoundTrip(unittest.TestCase):
    CHAPTER1_CONTENT = """# 1. First Chapter

This is the first chapter with some text.

"This is a QUOTE"

This is in single quotes. And should be ignored.

*This text is italicized.*

**This text is bold.**

*This is in italics. with a "quote" inside.*

"This is a quote with *italics* and **bold** inside."

It has multiple paragraphs.
This is the second paragraph.

---

Some more stuff. And more stuff.

"But Neth's guts have already tightened"

---

**Later**

---

*"Falling, he swaggered, a trail of grim deception,"*

*"Calling out breasts that spread like foul infection,"*

*"Stalling with grins that bent truth past reflection,"*

*"Hauling us all through the mass of his erection."*

And the whole mob join in a rowdy chorus - loud as ever, and completely off key:

*"Hauling us all through the mess of his erection."*


"""

    CHAPTER2_CONTENT = """# 2. Second Chapter

This is the second chapter.

Another paragraph here.
"""

    CHAPTER1_TEX = r"""\chapter{First Chapter}%
\label{chap:FirstChapter}%
This is the first chapter with some text.

\say{This is a QUOTE}

This is in single quotes. And should be ignored.

\textit{This text is italicized.}

\textbf{This text is bold.}

\textit{This is in italics. with a \say{quote} inside.}

\say{This is a quote with \textit{italics} and \textbf{bold} inside.}

It has multiple paragraphs.

This is the second paragraph.

\sectionbreak{}

Some more stuff. And more stuff.

\say{But Neth's guts have already tightened}

\sectionbreak{}

\textbf{Later}

\sectionbreak{}

\textit{\say{Falling, he swaggered, a trail of grim deception,}}

\textit{\say{Calling out breasts that spread like foul infection,}}

\textit{\say{Stalling with grins that bent truth past reflection,}}

\textit{\say{Hauling us all through the mass of his erection.}}

And the whole mob join in a rowdy chorus---loud as ever, and completely off key:

\textit{\say{Hauling us all through the mess of his erection.}}

%"""

    def setUp(self):
        self.dir_test_output = os.path.join(
            "tests", "output", "test_roundtrip"
        )
        # shutil.rmtree(self.dir_test_output, ignore_errors=True)
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

    def test_latex(self):
        book_dir1 = BookDir(self.dir_book)
        book_dir1.clean_and_write_all()

        latex_file_path = book_dir1.build_latex()
        self.assertTrue(
            os.path.exists(latex_file_path), "LaTeX file was not created"
        )

        all_lines = File(latex_file_path).read_lines()
        i_start = all_lines.index(r"\chapter{First Chapter}%")
        i_end = all_lines.index(r"\chapter{Second Chapter}%")
        actual_lines = all_lines[i_start:i_end]
        expected_lines = self.CHAPTER1_TEX.splitlines()
        assert len(expected_lines) == len(
            actual_lines
        ), "Number of lines in LaTeX output does not match expected"
        for i, (expected_line, actual_line) in enumerate(
            zip(expected_lines, actual_lines), start=1
        ):
            self.assertEqual(
                expected_line,
                actual_line,
                f'{i}: "{expected_line}" != "{actual_line}"',
            )

    def test_docx_roundtrip(self):
        book_dir1 = BookDir(self.dir_book)
        book_dir1.clean_and_write_all()

        docx_file_path = book_dir1.build_docx(10)
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
