from writing_utils import BookDir

if __name__ == "__main__":
    # doc
    book_dir = BookDir.from_args_or_environs()
    book_dir.clean_and_write_all()
    book_dir.rename_files(name_map=book_dir.get_name_map_from_titles())
    book_dir.print_statistics()

    # latex
    book_dir.build_latex()

    # docx
    docx_path = book_dir.build_docx()
    book_dir2 = BookDir.from_docx(docx_path)
    assert book_dir == book_dir2

    # md
    md_path = book_dir.build_md()
    book_dir3 = BookDir.from_md(
        md_path,
        output_dir=md_path + ".dir_from_md",
    )
    assert book_dir == book_dir3

    # general
    book_dir.backup()
    book_dir.open()
