from writing_utils import BookDir

if __name__ == "__main__":
    book_dir = BookDir.from_args_or_environs()
    book_dir.backup()
