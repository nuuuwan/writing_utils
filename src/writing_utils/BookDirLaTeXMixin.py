import os
import re

from pylatex import Chapter, Command, Document
from pylatex.utils import NoEscape
from utils import Log

from private import data

log = Log("BookDirLaTeXMixin")


class BookDirLaTeXMixin:
    def open_latex(self):
        latex_dir = self.__create_latex_directory__()
        pdf_path = os.path.join(latex_dir, "book.pdf")
        os.system(f'open "{pdf_path}"')

    def build_latex(self) -> str:
        latex_dir = self.__create_latex_directory__()
        output_path = os.path.join(latex_dir, "book")

        chapters = sorted(self.gen_chapter_docs(), key=lambda ch: ch.number)

        # Calculate word count from chapters
        word_count = sum(
            len(" ".join(ch.lines[1:]).split()) for ch in chapters
        )

        doc = self.__create_latex_document__(word_count)
        self.__add_chapters_to_latex_document__(doc)

        doc.generate_pdf(output_path, clean_tex=False)
        log.info(f"📄 Wrote {output_path}.pdf")
        return output_path + ".tex"

    def __create_latex_directory__(self) -> str:
        compiled_dir = self.path + ".compiled"
        latex_dir = os.path.join(compiled_dir, "latex")
        os.makedirs(latex_dir, exist_ok=True)
        return latex_dir

    def __create_latex_document__(self, word_count: int) -> Document:
        doc = Document(
            documentclass="book", document_options=["a4paper", "12pt"]
        )

        self.__configure_latex_page_layout__(doc)
        self.__add_latex_title_page__(doc, word_count)

        return doc

    def __configure_latex_page_layout__(self, doc: Document):
        doc.preamble.append(NoEscape(r"\usepackage[margin=1in]{geometry}"))
        doc.preamble.append(NoEscape(r"\usepackage{mathpazo}"))
        doc.preamble.append(NoEscape(r"\usepackage{setspace}"))
        doc.preamble.append(NoEscape(r"\doublespacing"))
        doc.preamble.append(NoEscape(r"\usepackage{csquotes}"))
        doc.preamble.append(NoEscape(r"\usepackage{fancyhdr}"))
        doc.preamble.append(NoEscape(r"\pagestyle{fancy}"))
        doc.preamble.append(NoEscape(r"\fancyhf{}"))
        doc.preamble.append(
            NoEscape(r"\fancyhead[L]{\textit{\nouppercase{\leftmark}}}")
        )
        doc.preamble.append(
            NoEscape(r"\fancyhead[R]{\textit{" + data.TITLE + r"}}")
        )
        doc.preamble.append(NoEscape(r"\fancyfoot[C]{\thepage}"))
        doc.preamble.append(NoEscape(r"\renewcommand{\headrulewidth}{0.5pt}"))
        doc.preamble.append(
            NoEscape(r"\renewcommand{\chaptermark}[1]{\markboth{#1}{#1}}")
        )
        doc.preamble.append(NoEscape(r"\usepackage{titlesec}"))
        chapter_format = (
            r"\titleformat{\chapter}[hang]"
            r"{\normalfont\huge\bfseries}{\thechapter.}{1em}{}"
        )
        doc.preamble.append(NoEscape(chapter_format))
        doc.preamble.append(NoEscape(r"\usepackage[dvipsnames]{xcolor}"))

        sectionbreak_command = (
            r"\newcommand{\sectionbreak}{%" + "\n"
            r"  \par\bigskip%" + "\n"
            r"  \centerline{\large\ldots}%" + "\n"
            r"  \bigskip\par%" + "\n"
            r"}"
        )
        doc.preamble.append(NoEscape(sectionbreak_command))

        say_command = r"\newcommand{\say}[1]{{\color{Maroon}\enquote{#1}}}"
        doc.preamble.append(NoEscape(say_command))
        doc.preamble.append(NoEscape(r"\let\cleardoublepage\clearpage"))
        doc.preamble.append(NoEscape(r"\usepackage{hyperref}"))

    def __add_latex_title_page__(self, doc: Document, word_count: int):

        title_with_subtitle = data.TITLE + r"\\" + r"\large " + data.SUBTITLE
        doc.preamble.append(Command("title", NoEscape(title_with_subtitle)))

        doc.preamble.append(Command("author", "By " + data.AUTHOR))

        date_and_wordcount = NoEscape(
            r"\small{\today}"
            + r"\\"
            + r"\vspace{1em}"
            + rf"\small{{{word_count:,} words}}"
        )
        doc.preamble.append(Command("date", date_and_wordcount))

        doc.append(NoEscape(r"\maketitle"))
        doc.append(NoEscape(r"\newpage"))

        self.__add_latex_copyright_page__(doc)

        doc.append(NoEscape(r"\tableofcontents"))
        doc.append(NoEscape(r"\newpage"))

    def __add_latex_copyright_page__(self, doc: Document):
        doc.append(NoEscape(r"\thispagestyle{empty}"))
        doc.append(NoEscape(r"\vspace*{\fill}"))
        doc.append(NoEscape(r"\begin{center}"))
        copyright_line = (
            r"Copyright \textcopyright\ \the\year\ by " + data.AUTHOR + r"\\"
        )
        doc.append(NoEscape(copyright_line))
        doc.append(NoEscape(r"\vspace{1em}"))
        doc.append(NoEscape(r"All rights reserved.\\"))
        doc.append(NoEscape(r"\end{center}"))
        doc.append(NoEscape(r"\vspace*{\fill}"))
        doc.append(NoEscape(r"\newpage"))

    def __add_chapters_to_latex_document__(self, doc: Document):
        chapters = sorted(self.gen_chapter_docs(), key=lambda ch: ch.number)

        for chapter_doc in chapters:
            self.__add_latex_chapter_section__(doc, chapter_doc)

    def __add_latex_chapter_section__(self, doc: Document, chapter_doc):
        with doc.create(Chapter(chapter_doc.title, numbering=True)):
            lines = chapter_doc.lines[1:]
            content = "\n".join(lines).strip()
            content = self.__convert_markdown_to_latex__(content)
            doc.append(NoEscape(content))

    @staticmethod
    def __convert_markdown_to_latex__(content: str) -> str:
        content = BookDirLaTeXMixin.__normalize_punctuation__(content)
        content = BookDirLaTeXMixin.__escape_special_chars__(content)
        content = BookDirLaTeXMixin.__fix_spacing__(content)
        content = BookDirLaTeXMixin.__convert_quotes__(content)
        content = BookDirLaTeXMixin.__convert_text_formatting__(content)
        content = BookDirLaTeXMixin.__convert_headers__(content)
        content = BookDirLaTeXMixin.__convert_rules_and_paragraphs__(content)
        return content

    @staticmethod
    def __fix_spacing__(content: str) -> str:
        # Fix abbreviations: add \  after common abbreviations
        for abbrev in [
            "Mr",
            "Mrs",
            "Ms",
            "Dr",
            "Prof",
            "Sr",
            "Jr",
            "vs",
            "etc",
        ]:
            content = re.sub(rf"\b{abbrev}\.\s+", rf"{abbrev}.\\ ", content)

        return content

    @staticmethod
    def __normalize_punctuation__(content: str) -> str:
        # Convert curly apostrophes to straight apostrophes
        content = content.replace("\u2019", "'")  # ' → '
        content = content.replace("\u2018", "'")  # ' → '
        # Convert em-dash and en-dash
        content = content.replace(" - ", "---")
        content = content.replace(" \u2014 ", "---")
        content = content.replace(" \u2013 ", "---")
        content = content.replace("\u2014", "-")
        content = content.replace("\u2013", "-")

        return content

    @staticmethod
    def __convert_quotes__(content: str) -> str:
        content = re.sub(r'"([^"]*?)"', r"\\say{\1}", content, flags=re.DOTALL)
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
        content = re.sub(
            r"^---+$", r"\\sectionbreak{}", content, flags=re.MULTILINE
        )
        return content
