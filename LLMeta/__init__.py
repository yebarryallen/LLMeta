import os
import numpy as np
import pandas as pd
from openai import OpenAI
from langchain.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from concurrent.futures import ThreadPoolExecutor



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


def split_markdown_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    text_list = text.split("---\n")

    def append_next_element_start(elements):
        if not elements:
            return []

        result = []
        for i in range(len(elements) - 1):
            next_element = elements[i + 1]
            period_index = next_element.find('.')
            if period_index != -1:
                result.append(elements[i] + next_element[:period_index + 1])
            else:
                result.append(elements[i])
        result.append(elements[-1])
        return result

    final_text_list = append_next_element_start(text_list)
    return final_text_list


def save_vectorstore(vector_name, saving_path, text_chunks):
    from langchain.vectorstores import FAISS
    from langchain_openai import OpenAIEmbeddings
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    FAISS.save_local(vectorstore, saving_path, vector_name)

def markdown_to_vectorstore(path, saving_path):
    files = os.listdir(path)
    for md in files:
        print(f"Processing markdown file: {md}")
        # get md text
        text_list = split_markdown_file(os.path.join(path, md))
        save_vectorstore(md, saving_path, text_list)

def generate_hypothetical_text(variable, definition, value, where_to_find, title, abstract, apikey=None):
    if apikey is None:
        with open("api.txt", "r") as f:
            apikey = f.read()
    from openai import OpenAI
    messages = [
        {"role": "system",
         "content": "You are an expert in conducting systematic Review. Your task is to generate a paragraph of text that could plausibly appear in the article, based on the given variables, their definitions, and corresponding values, considering the context of the provided title and abstract."},
        {"role": "system", "content": f"Title: {title}"},
        {"role": "system", "content": f"Abstract: {abstract}"},
        {"role": "user",
         "content": f"Generate a hypothetical text using the following information:\nVariable: {variable}\nDefinition: {definition}\nPossible scenarios (corresponding values): {value}\nWhere to find: {where_to_find}"}
    ]
    client = OpenAI(api_key=apikey)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=messages,
        temperature=0.7,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    hypothetical_text = response.choices[0].message.content
    return hypothetical_text


def get_relate_doc(vector_name, vectorstore_path, hypothetical_text, variable, apikey=None):
    if apikey is None:
        with open("api.txt", "r") as f:
            apikey = f.read()
    from langchain.vectorstores import FAISS
    from langchain_openai import OpenAIEmbeddings
    print(f"Processing question for PDF {vector_name}, variable {variable}")
    embeddings = OpenAIEmbeddings(openai_api_key=apikey)
    vectorstore = FAISS.load_local(vectorstore_path, embeddings=embeddings, index_name=vector_name, allow_dangerous_deserialization=True)
    retriever = vectorstore.as_retriever()
    original_docs = retriever.get_relevant_documents(hypothetical_text)
    result_string = "\npage".join(
        [f"{i + 1}:{doc.page_content}" for i, doc in enumerate(original_docs) if hasattr(doc, 'page_content')]
    )
    return result_string


def generate_judgement(result_string, variable, definition, possible_values, title, abstract, format=None, selected_model="gpt-3.5-turbo-0125", apikey=None):
    if format is None:
        format = """The output should be a JSON string with the following format:{"value": str   Based on the given context, determine the content. If the article mentions the concept corresponding to the variable and the situation matches one of the values in 'value', fill in the corresponding value. If the variable is not mentioned or there is no corresponding value for the situation, fill in None.}"""
    if apikey is None:
        with open("api.txt", "r") as f:
            apikey = f.read()
    from openai import OpenAI
    client = OpenAI(api_key=apikey)
    response = client.chat.completions.create(
        model=selected_model,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": "You are an expert in systematic review and are now working on extraction information from papers to code variables pre-defined."
            },
            {"role": "system", "content": format},
            {
                "role": "system",
                "content": f"""
                Information about the text of the paper that needs to be judged: "
                [Title: "{title}",
                Abstract: "{abstract}",
                Selected passages from the article:{result_string}]"""
            },
            {
                "role": "user",
                "content": f"""
                following is the variable you need to identify and extract:
                [Variable: "{variable}",
                Definition: "{definition}",
                Possible Values: {possible_values}]"""
            },
            {
                "role": "user",
                "content": f"""Based on the given context, determine if the text mentions the concept corresponding to the variable '{variable}' and if the situation matches one of the values in 'possible_values'. If mentioned, fill in the corresponding value. If not mentioned or no matching value, fill in None."""
            }
        ],
        temperature=0,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        logprobs=True
    )

    return response






def process_row(row_data, variable_list, vector_path, txt_folder_name, apikey=None):
    title = row_data["Title"]
    abstract = row_data["abstract"]
    key = row_data["Key"] + ".md"
    print(f"Processing paper: {key}")
    if apikey is None:
        with open("api.txt", "r") as f:
            apikey = f.read()
    for index, row in variable_list.iterrows():
        identity = row["identity"]
        variable = row["Variable"]
        definition = row["Definition"]
        value = row["Value"]
        where_to_find = row["Where to find"]
        # 检测文件是否已经存在
        if os.path.exists(f"./raw_output/{txt_folder_name}/answer/{key}_{identity}.txt"):
            print(f"File {key}_{identity} already exists, skipping...")
            continue
        hypothetical_text = generate_hypothetical_text(variable, definition, value, where_to_find, title, abstract, apikey)
        vector_name = key
        result_string = get_relate_doc(vector_name, vector_path, hypothetical_text, variable, apikey)
        response = generate_judgement(result_string, variable, definition, value, title, abstract, format=None, apikey=apikey)
        content_value = response.choices[0].message.content
        prob_content = response.choices[0].logprobs.content

        linear_probability = [np.exp(token.logprob) * 100 for token in prob_content]
        n_probability = np.mean(linear_probability)
        logprobs = [token.logprob for token in prob_content]
        perplexity_score = np.exp(-np.mean(logprobs))

        with open(f"./raw_output/{txt_folder_name}/answer/{vector_name}_{identity}.txt", "w", encoding="utf-8") as f:
            f.write(str(content_value))
        with open(f"./raw_output/{txt_folder_name}/source/{vector_name}_{identity}.txt", "w", encoding="utf-8") as f:
            f.write(str(result_string))
        with open(f"./raw_output/{txt_folder_name}/probability/{vector_name}_{identity}.txt", "w", encoding="utf-8") as f:
            f.write(str(prob_content) + "\n\n" + str(n_probability) + "\n\n" + str(perplexity_score))

def process_papers(variable_list_path, merged_csv_path, vector_path, txt_folder_name, markdown_file_path, apikey,
                   max_workers=16):
    from concurrent.futures import ThreadPoolExecutor
    from LLMeta import process_row
    variable_list = pd.read_excel(variable_list_path)
    merged = pd.read_csv(merged_csv_path)

    # 读取 Markdown 文件夹下的所有文件
    md_files = os.listdir(markdown_file_path)
    keys = [os.path.splitext(md)[0] for md in md_files]
    # 筛选出merged中 Key 存在于keys中的行
    merged = merged[merged["Key"].isin(keys)]

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_row, row_data, variable_list, vector_path, txt_folder_name, apikey) for
                   _, row_data in merged.iterrows()]
        for future in futures:
            future.result()  # 如果需要处理结果，可以在这里处理


def formated_output(answer_folder, source_folder, probability_folder, merged_csv_path, variable_excel_path, output_csv_path):
    import json
    # 获取文件夹中的所有文件名
    answer_files = os.listdir(answer_folder)
    source_files = os.listdir(source_folder)
    probability_files = os.listdir(probability_folder)

    # 创建一个空的数据框
    df = pd.DataFrame(columns=['filename', 'source', 'extraction', 'prob_value', 'n_probability', 'perplexity_score'])

    errofile = []
    # 遍历文件夹中的每个文件
    for filename in answer_files:
        # 只处理.txt文件
        if filename.endswith('.txt'):
            # 获取文件名（不含扩展名）
            file_name = os.path.splitext(filename)[0]

            # 构建完整路径
            answer_file_path = os.path.join(answer_folder, filename)
            source_file_path = os.path.join(source_folder, filename)
            probability_file_path = os.path.join(probability_folder, filename)
            if filename in source_files:
                try:
                    # 读取答案文件
                    with open(answer_file_path, 'r', encoding='utf-8') as f:
                        answer_data = json.load(f)
                    # 读取来源文件
                    with open(source_file_path, 'r', encoding='utf-8') as f:
                        source_data = f.read()
                    # 读取概率文件
                    with open(probability_file_path, 'r', encoding='utf-8') as f:
                        text = f.read()
                        prob_value, n_probability, perplexity_score = text.split('\n\n')

                    # 提取答案的两个维度
                    dimension1 = answer_data['value']

                    # 将文件名、来源、维度1和维度2添加到数据框中
                    df = pd.concat([df, pd.DataFrame(
                        {'filename': [file_name], 'source': [source_data], 'extraction': [dimension1],
                         'prob_value': [prob_value], 'n_probability': [n_probability],
                         'perplexity_score': [perplexity_score]})])
                except Exception as e:
                    # 记录出错的文件名
                    errofile.append(filename)
                    print(f"处理文件 {filename} 时出错：{e}")
                    continue

    df[['Key', 'identity']] = df['filename'].str.split('_', expand=True)
    # 去除 Key 中的 .md
    df['Key'] = df['Key'].str.replace('.md', '')
    # 导入 merged.csv dataframe
    df1 = pd.read_csv(merged_csv_path)
    # left join 合并两个dataframe
    df = pd.merge(df, df1, left_on='Key', right_on='Key', how='left')
    # 导入 protocol for variable extraction.xlsx 文件
    df2 = pd.read_excel(variable_excel_path)
    # 将 df2 中的 identity 列转化为字符串
    df2['identity'] = df2['identity'].astype(str)
    # left join 合并两个dataframe
    df = pd.merge(df, df2, left_on='identity', right_on='identity', how='left')

    # 保存合并后的 dataframe 为 merged_final.csv
    df.to_csv(output_csv_path, index=False)



