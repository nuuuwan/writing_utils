from writing_utils import BookDir

if __name__ == "__main__":
    book_dir = BookDir.from_args_or_environs()
    book_dir.rename_files(name_map=book_dir.get_name_map_from_titles())
