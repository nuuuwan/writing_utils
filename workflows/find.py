import sys

from writing_utils import BookDir

if __name__ == "__main__":
    book_dir = BookDir.from_args_or_environs()
    search_key = sys.argv[1]
    prev_number_and_title = None
    for find_info in book_dir.find(search_key):
        number_and_title = find_info["number_and_title"]
        if prev_number_and_title != number_and_title:
            print("")
            print(number_and_title)
        print(" " * 4, find_info["i_line"], find_info["line"])
        prev_number_and_title = number_and_title
