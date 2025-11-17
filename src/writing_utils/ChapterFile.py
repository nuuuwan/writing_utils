from utils import File, Log

log = Log("ChapterFile")


class ChapterFile(File):

    @property
    def first_line(self):
        lines = self.read_lines()
        first_line = lines[0]
        return first_line

    @property
    def number_and_title(self) -> str | None:
        first_line = self.first_line
        assert first_line.startswith(
            "# "
        ), f"First line does not start with '# ': {first_line}"
        return first_line[2:].strip()

    @property
    def number(self) -> int:
        number_and_title = self.number_and_title
        assert (
            "." in number_and_title
        ), f"No '.' in number_and_title: {number_and_title}"
        number_str = number_and_title.split(".")[0]
        return int(number_str)

    @number.setter
    def number(self, new_number: int):
        assert isinstance(
            new_number, int
        ), f"new_number must be an integer: {new_number}"
        lines = self.read_lines()
        title = self.title
        lines[0] = f"# {new_number}. {title}"
        self.write_lines(lines)

    @property
    def title(self) -> str:
        number_and_title = self.number_and_title
        assert (
            "." in number_and_title
        ), f"No '.' in number_and_title: {number_and_title}"
        title = number_and_title.split(".", 1)[1].strip()
        return title

    @property
    def title_cleaned(self) -> str:
        title = self.title
        title_cleaned = title.replace(" ", "-").replace("/", "-")
        return title_cleaned.lower()
