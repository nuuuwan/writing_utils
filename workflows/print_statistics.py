from utils import Log

from writing_utils import BookDir

log = Log("print_statistics")
if __name__ == "__main__":
    book_dir = BookDir.from_args_or_environs()
    log.info(book_dir.path)
    log.info(f"Number of characters: {book_dir.n_chars}")
    log.info(f"Number of words: {book_dir.n_words}")
