from functools import cached_property

from utils import File, Log

log = Log("ChapterFile")


class ChapterFile(File):

    @cached_property
    def lines(self):
        return self.read_lines()

    @cached_property
    def first_line(self):
        first_line = self.lines[0]
        return first_line

    @cached_property
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

        for k in ["lines", "first_line", "number_and_title"]:
            if k in self.__dict__:
                del self.__dict__[k]

    @cached_property
    def title(self) -> str:
        number_and_title = self.number_and_title
        assert (
            "." in number_and_title
        ), f"No '.' in number_and_title: {number_and_title}"
        title = number_and_title.split(".", 1)[1].strip()
        return title

    @cached_property
    def title_cleaned(self) -> str:
        title = self.title
        title_cleaned = title.replace(" ", "-").replace("/", "-")
        return title_cleaned.lower()

    @cached_property
    def content(self) -> str:
        return "\n".join(self.lines)

    @cached_property
    def n_chars(self) -> int:
        return len(self.content)

    @cached_property
    def n_words(self) -> int:
        return len(self.content.split())
