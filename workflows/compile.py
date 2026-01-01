import os

from writing_utils import BookDir

if __name__ == "__main__":
    # doc
    book_dir = BookDir.from_args_or_environs()
    book_dir.clean_and_write_all()
    book_dir.rename_files(name_map=book_dir.get_name_map_from_titles())
    book_dir.print_statistics()
    book_dir.backup()

    # docx
    docx_path = book_dir.build_docx(max_words_per_docx=10_000)
    book_dir2 = BookDir.from_docx(docx_path)
    assert book_dir == book_dir2

    # md
    md_path = book_dir.build_md()
    book_dir3 = BookDir.from_md(
        md_path,
        output_dir=md_path + ".dir_from_md",
    )
    assert book_dir == book_dir3

    # latex
    latex_path = book_dir.build_latex()
    pdf_path = latex_path[:-4] + ".pdf"
    os.system(f'open -a Preview "{pdf_path}"')
