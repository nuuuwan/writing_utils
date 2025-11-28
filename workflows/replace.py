import sys

from writing_utils import BookDir

if __name__ == "__main__":
    book_dir = BookDir.from_args_or_environs()
    book_dir.backup()
    find_text = sys.argv[1]
    replace_text = sys.argv[2]
    prev_number_and_title = None
    book_dir.replace(find_text, replace_text)
