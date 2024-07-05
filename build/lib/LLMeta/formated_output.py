import os
import json
import pandas as pd

def formated_output(answer_folder, source_folder, probability_folder, merged_csv_path, variable_excel_path, output_csv_path):
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


