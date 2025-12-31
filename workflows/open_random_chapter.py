import random

from writing_utils import BookDir

if __name__ == "__main__":
    book_dir = BookDir.from_args_or_environs()
    chapter_docs = [cd for cd in book_dir.gen_chapter_docs()]
    random.shuffle(chapter_docs)
    book_dir.open()
    chapter_docs[0].open()
