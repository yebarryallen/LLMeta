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
