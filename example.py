import os
import numpy as np
import pandas as pd
from openai import OpenAI
from langchain.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from concurrent.futures import ThreadPoolExecutor

from LLMeta import (
    formated_output,
    setup,
    generate_hypothetical_text,
    generate_judgement,
    get_relate_doc,
    process_row,
    process_papers,
    save_vectorstore,
    split_markdown_file,
    markdown_to_vectorstore
)
os.environ['http_proxy'] = 'http://127.0.0.1:7890'
os.environ['https_proxy'] = 'http://127.0.0.1:7890'
# 读取api.txt文件中的apikey
with open("api.txt", "r") as f:
    apikey = f.read()
os.environ['OPENAI_API_KEY'] =apikey
client = OpenAI(api_key= apikey)

# 设置路径
path = "markdown_file"
saving_path = "vectorstore"

# 调用示例函数
#markdown_to_vectorstore(path, saving_path)



setup("Digital_Democracy")

if __name__ == "__main__":
    variable_file_path = "protocol for variable extraction.xlsx"
    merged_file_path = "merged.csv"
    vector_path = "vectorstore"
    markdown_file_path = "markdown_file"
    txt_folder_name = "Digital_Democracy"
    apikey = apikey
    process_papers(variable_file_path, merged_file_path, vector_path, txt_folder_name, markdown_file_path, apikey)

import json
if __name__ == "__main__":
    answer_folder = r'A:raw_output\Digital_Democracy\answer'
    source_folder = r'A:raw_output\Digital_Democracy\source'
    probability_folder = r'A:raw_output\Digital_Democracy\probability'
    merged_csv_path = "merged.csv"
    variable_excel_path = "protocol for variable extraction.xlsx"
    output_csv_path = "final_extraction.csv"

    formated_output(answer_folder, source_folder, probability_folder, merged_csv_path, variable_excel_path, output_csv_path)