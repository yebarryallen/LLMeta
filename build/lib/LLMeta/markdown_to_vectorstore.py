def markdown_to_vectorstore(path, saving_path):
    files = os.listdir(path)
    for md in files:
        print(f"Processing markdown file: {md}")
        # get md text
        text_list = split_markdown_file(os.path.join(path, md))
        save_vectorstore(md, saving_path, text_list)