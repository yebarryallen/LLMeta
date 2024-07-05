
def process_row(client, row_data, variable_list, vector_path, txt_folder_name, apikey):
    import os
    import numpy as np
    from .generate_hypothetical_text import generate_hypothetical_text
    from .get_relate_doc import get_relate_doc
    from .generate_judgement import generate_judgement
    title = row_data["Title"]
    abstract = row_data["abstract"]
    key = row_data["Key"] + ".md"
    print(f"Processing paper: {key}")
    for index, row in variable_list.iterrows():
        identity = row["identity"]
        variable = row["Variable"]
        definition = row["Definition"]
        value = row["Value"]
        where_to_find = row["Where to find"]
        if os.path.exists(f"./raw_output/{txt_folder_name}/answer/{key}_{identity}.txt"):
            print(f"File {key}_{identity} already exists, skipping...")
            continue
        hypothetical_text = generate_hypothetical_text(client, variable, definition, value, where_to_find, title, abstract)
        vector_name = key
        result_string = get_relate_doc(client, vector_name, vector_path, apikey, hypothetical_text, variable)
        response = generate_judgement(client, result_string, variable, definition, value, title, abstract)
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
