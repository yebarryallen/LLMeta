def process_threads(variable_file_path, merged_file_path, vector_path, markdown_file_path, txt_folder_name, worker=16):
    import pandas as pd
    import os
    from concurrent.futures import ThreadPoolExecutor
    from LLMeta import process_row
    variable_list = pd.read_excel(variable_file_path)
    merged = pd.read_csv(merged_file_path)
    # 读取 Markdown 文件夹下的所有文件
    md_files = os.listdir(markdown_file_path)
    keys = [os.path.splitext(md)[0] for md in md_files]
    # 筛选出merged中 Key 存在于keys中的行
    merged = merged[merged["Key"].isin(keys)]

    with ThreadPoolExecutor(max_workers=worker) as executor:
        futures = [executor.submit(process_row, row_data, variable_list, vector_path, txt_folder_name) for _, row_data in merged.iterrows()]
        for future in futures:
            future.result()  # 如果需要处理结果，可以在这里处理



