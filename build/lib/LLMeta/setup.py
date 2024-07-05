
def setup(program_name):
    import os
    base_path = os.getcwd()
    directories = [
        "markdown_file",
        "pdf_folder",
        f"raw_output/{program_name}/answer",
        f"raw_output/{program_name}/probability",
        f"raw_output/{program_name}/source",
        "temp",
        "vectorstore"
    ]
    for dir_path in directories:
        os.makedirs(os.path.join(base_path, dir_path), exist_ok=True)

    print("Directories created.")
