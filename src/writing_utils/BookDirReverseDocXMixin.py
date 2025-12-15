import os
import re
import tempfile

from docx import Document
from utils import Log

log = Log("BookDirReverseDocXMixin")


class BookDirReverseDocXMixin:
    @classmethod
    def from_docx(cls, docx_path: str):
        from writing_utils import BookDir

        doc = Document(docx_path)
        temp_dir = tempfile.mkdtemp(prefix="writing_utils_")

        chapters = {}
        current_chapter_num = None
        current_chapter_title = None
        current_chapter_lines = []
        found_first_chapter = False

        for para in doc.paragraphs:
            style_name = para.style.name
            text = para.text.strip()

            if style_name.startswith("Heading 1"):
                heading_match = re.match(r"(\d+)\.\s+(.+)", text)
                if heading_match:
                    found_first_chapter = True

                    if current_chapter_num is not None:
                        chapter_text = "\n".join(current_chapter_lines)
                        chapters[current_chapter_num] = (
                            current_chapter_title,
                            chapter_text,
                        )

                    current_chapter_num = int(heading_match.group(1))
                    current_chapter_title = heading_match.group(2)
                    current_chapter_lines = [
                        f"# {current_chapter_num}. {current_chapter_title}"
                    ]
            elif found_first_chapter and current_chapter_num is not None:
                if text:
                    current_chapter_lines.append(text)

        if current_chapter_num is not None:
            chapter_text = "\n".join(current_chapter_lines)
            chapters[current_chapter_num] = (
                current_chapter_title,
                chapter_text,
            )

        for chapter_num, (title, content) in sorted(chapters.items()):
            filename = f"{chapter_num:02d}-{title.replace(' ', '_')}.md"
            filepath = os.path.join(temp_dir, filename)
            with open(filepath, "w") as f:
                f.write(content)

        book_dir = BookDir(temp_dir)
        log.info(f"📖 Loaded BookDir from {docx_path}")
        return book_dir
