from utils import Log

from writing_utils import BookDir

log = Log("docx_to_bookdir")

if __name__ == "__main__":
    book_dir = BookDir.from_args_or_environs()
    docx_path = book_dir.path + ".docx"
    book_dir2 = BookDir.from_docx(docx_path)
    if book_dir == book_dir2:
        log.debug("0️⃣ Has not been changed")
    else:
        log.info("✍️ Has been changed")
