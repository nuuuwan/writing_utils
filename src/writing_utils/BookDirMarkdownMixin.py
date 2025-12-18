import os

from utils import File, Log

from private import data

log = Log("BookDirMarkdownMixin")


class BookDirMarkdownMixin:
    def build_md(self) -> str:
        md_path = self.path + ".md"
        lines = []

        lines.append(f"# {data.TITLE}")
        lines.append("")
        lines.append(f"*{data.SUBTITLE}*")
        lines.append("")
        lines.append(f"By {data.AUTHOR}")
        lines.append("")
        lines.append("---")
        lines.append("")

        for chapter_doc in self.gen_chapter_docs():
            chapter_lines = chapter_doc.lines
            for line in chapter_lines:
                if line.startswith("# "):
                    line = "#" + line
                lines.append(line)
            lines.append("")

        File(md_path).write_lines(lines)
        log.info(f"📝 Wrote {File(md_path)}")
        return md_path

    @classmethod
    def from_md(cls, md_path: str, output_dir: str):
        shutil.rmtree(output_dir, ignore_errors=True)
        os.makedirs(output_dir, exist_ok=True)

        lines = File(md_path).read_lines()

        chapters = []
        current_chapter_lines = []

        for line in lines[8:]:
            if line.startswith("## "):
                if current_chapter_lines:
                    chapters.append(current_chapter_lines)
                current_chapter_lines = [line]
            else:
                if current_chapter_lines or line.strip():
                    current_chapter_lines.append(line)

        if current_chapter_lines:
            chapters.append(current_chapter_lines)

        for i, chapter_lines in enumerate(chapters, start=1):
            new_chapter_lines = []
            title_line = None
            for line in chapter_lines:
                if line.startswith("## "):
                    line = "# " + line[3:].strip()
                    if title_line is None:
                        title_line = line
                    else:
                        raise ValueError(
                            "Multiple title lines found in chapter"
                        )
                new_chapter_lines.append(line)

            chapter_content = "\n".join(new_chapter_lines).strip()

            title_only = title_line[2:].strip()
            num_only = int(title_only.split(".", 1)[0].strip())
            name_only = title_only.split(".", 1)[1].strip()
            name_id = name_only.replace(" ", "_").replace("/", "-")
            chapter_filename = f"{num_only:02d}-{name_id}.md"
            chapter_path = os.path.join(output_dir, chapter_filename)

            File(chapter_path).write(chapter_content)

        log.info(f"📚 Created BookDir from {File(md_path)} at {output_dir}")
        return cls(output_dir)
