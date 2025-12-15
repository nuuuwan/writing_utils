import os
import re

from docx import Document
from utils import File, Log

log = Log("BookDirReverseDocXMixin")


class BookDirReverseDocXMixin:
    @staticmethod
    def extract_formatted_text(para):
        formatted_text = ""
        for run in para.runs:
            text = run.text
            if run.bold:
                text = f"**{text}**"
            if run.italic:
                text = f"*{text}*"
            formatted_text += text
        return formatted_text.strip()

    @classmethod
    def from_docx(cls, docx_path: str):
        """Load BookDir from a DOCX file."""
        doc = Document(docx_path)
        temp_dir = docx_path + ".bookdir"
        os.makedirs(temp_dir, exist_ok=True)

        chapters = cls._parse_chapters_from_doc(doc)
        cls._save_chapters_to_files(chapters, temp_dir)

        book_dir = cls(temp_dir)
        book_dir.clean_and_write_all()
        log.info(f"📖 Loaded BookDir from {docx_path}")
        return book_dir

    @classmethod
    def _parse_chapters_from_doc(cls, doc):
        """Extract chapters from Document, preserving formatting."""
        chapters = {}
        current_chapter_num = None
        current_chapter_title = None
        current_chapter_lines = []
        found_first_chapter = False

        for para in doc.paragraphs:
            style_name = para.style.name
            text = cls.extract_formatted_text(para)

            if style_name.startswith("Heading 1"):
                heading_match = re.match(r"(\d+)\.\s+(.+)", text)
                if heading_match:
                    found_first_chapter = True
                    if current_chapter_num is not None:
                        chapters[current_chapter_num] = (
                            current_chapter_title,
                            "\n".join(current_chapter_lines),
                        )
                    current_chapter_num = int(heading_match.group(1))
                    current_chapter_title = heading_match.group(2)
                    current_chapter_lines = [
                        f"# {current_chapter_num}. {current_chapter_title}"
                    ]
            elif (
                found_first_chapter
                and current_chapter_num is not None
                and text
            ):
                current_chapter_lines.append(text)

        if current_chapter_num is not None:
            chapters[current_chapter_num] = (
                current_chapter_title,
                "\n".join(current_chapter_lines),
            )

        return chapters

    @staticmethod
    def _save_chapters_to_files(chapters, temp_dir):
        """Write chapters to individual markdown files."""
        for chapter_num, (title, content) in sorted(chapters.items()):
            filename = f"{chapter_num:02d}-{title.replace(' ', '_')}.md"
            filepath = os.path.join(temp_dir, filename)
            File(filepath).write(content)
