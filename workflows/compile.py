from writing_utils import BookDir

if __name__ == "__main__":
    book_dir = BookDir.from_args_or_environs()
    book_dir.clean_all()
    book_dir.rename_files(name_map=book_dir.get_name_map_from_titles())
    book_dir.print_statistics()

    book_dir.build_latex()
    # book_dir.open_latex()

    docx_path = book_dir.build_docx()
    # book_dir.open_docx()

    book_dir2 = BookDir.from_docx(docx_path)
    assert book_dir == book_dir2

    book_dir.backup()
    # book_dir.open()
