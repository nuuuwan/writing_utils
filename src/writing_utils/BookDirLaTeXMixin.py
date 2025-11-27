import os
import re

from pylatex import Command, Document, Section
from pylatex.utils import NoEscape
from utils import Log

from private import data

log = Log("BookDirLaTeXMixin")


class BookDirLaTeXMixin:
    def build_latex(self) -> Document:
        latex_dir = self.__create_latex_directory__()
        output_path = os.path.join(latex_dir, "book")

        doc = self.__create_document__()
        self.__add_chapters_to_document__(doc)

        doc.generate_pdf(output_path, clean_tex=False)
        log.info(f"📄 Generated LaTeX/PDF at {output_path}.pdf")

        return doc

    def __create_latex_directory__(self) -> str:
        latex_dir = self.path + ".latex"
        os.makedirs(latex_dir, exist_ok=True)
        return latex_dir

    def __create_document__(self) -> Document:
        doc = Document(documentclass="book", document_options=["a4paper"])

        self.__configure_page_layout__(doc)
        self.__add_title_page__(doc)

        return doc

    def __configure_page_layout__(self, doc: Document):
        doc.preamble.append(NoEscape(r"\usepackage[margin=1in]{geometry}"))
        doc.preamble.append(NoEscape(r"\usepackage{setspace}"))
        doc.preamble.append(NoEscape(r"\doublespacing"))
        doc.preamble.append(NoEscape(r"\usepackage{fancyhdr}"))
        doc.preamble.append(NoEscape(r"\pagestyle{fancy}"))
        doc.preamble.append(NoEscape(r"\fancyhf{}"))
        doc.preamble.append(NoEscape(r"\fancyfoot[C]{\thepage}"))
        doc.preamble.append(NoEscape(r"\renewcommand{\headrulewidth}{0pt}"))

    def __add_title_page__(self, doc: Document):
        doc.preamble.append(Command("title", data.TITLE))
        doc.preamble.append(Command("author", data.AUTHOR))
        doc.preamble.append(Command("date", NoEscape(r"\today")))

        doc.append(NoEscape(r"\maketitle"))
        doc.append(NoEscape(r"\newpage"))

        self.__add_copyright_page__(doc)

        doc.append(NoEscape(r"\tableofcontents"))
        doc.append(NoEscape(r"\newpage"))

    def __add_copyright_page__(self, doc: Document):
        doc.append(NoEscape(r"\thispagestyle{empty}"))
        doc.append(NoEscape(r"\vspace*{\fill}"))
        doc.append(NoEscape(r"\begin{center}"))
        copyright_line = (
            r"Copyright \textcopyright\ \the\year\ by " + data.AUTHOR + r"\\"
        )
        doc.append(NoEscape(copyright_line))
        doc.append(NoEscape(r"\vspace{1em}"))
        doc.append(NoEscape(r"All rights reserved.\\"))
        doc.append(NoEscape(r"\vspace{1em}"))
        doc.append(NoEscape(r"Publisher/Printer: \\" + data.AUTHOR))
        doc.append(NoEscape(r"\end{center}"))
        doc.append(NoEscape(r"\vspace*{\fill}"))
        doc.append(NoEscape(r"\newpage"))

    def __add_chapters_to_document__(self, doc: Document):
        chapters = sorted(self.gen_chapter_docs(), key=lambda ch: ch.number)

        for chapter_doc in chapters:
            log.info(
                f"Adding chapter {chapter_doc.number}: {chapter_doc.title}"
            )
            self.__add_chapter_section__(doc, chapter_doc)

    def __add_chapter_section__(self, doc: Document, chapter_doc):
        with doc.create(Section(chapter_doc.title, numbering=True)):
            lines = chapter_doc.lines[1:]
            content = "\n".join(lines).strip()
            content = self.__convert_markdown_to_latex__(content)
            doc.append(NoEscape(content))

    @staticmethod
    def __convert_markdown_to_latex__(content: str) -> str:
        content = BookDirLaTeXMixin.__convert_text_formatting__(content)
        content = BookDirLaTeXMixin.__convert_headers__(content)
        content = BookDirLaTeXMixin.__escape_special_chars__(content)
        content = BookDirLaTeXMixin.__convert_rules_and_paragraphs__(content)
        return content

    @staticmethod
    def __convert_text_formatting__(content: str) -> str:
        content = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", content)
        content = re.sub(r"\*(.+?)\*", r"\\textit{\1}", content)
        return content

    @staticmethod
    def __convert_headers__(content: str) -> str:
        content = re.sub(
            r"^### (.+)$", r"\\subsubsection{\1}", content, flags=re.MULTILINE
        )
        content = re.sub(
            r"^## (.+)$", r"\\subsection{\1}", content, flags=re.MULTILINE
        )
        return content

    @staticmethod
    def __escape_special_chars__(content: str) -> str:
        content = re.sub(r"(?<!\\)&", r"\\&", content)
        content = re.sub(r"(?<!\\)%", r"\\%", content)
        content = re.sub(r"(?<!\\)\$", r"\\$", content)
        return content

    @staticmethod
    def __convert_rules_and_paragraphs__(content: str) -> str:
        content = re.sub(r"^---+$", r"\\hrule", content, flags=re.MULTILINE)
        content = re.sub(r"\n\n+", r"\n\n\\par\n", content)
        return content
