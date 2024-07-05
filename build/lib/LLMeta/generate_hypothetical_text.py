from openai import OpenAI

def generate_hypothetical_text(client, variable, definition, value, where_to_find, title, abstract):
    messages = [
        {"role": "system",
         "content": "You are an expert in conducting systematic Review. Your task is to generate a paragraph of text that could plausibly appear in the article, based on the given variables, their definitions, and corresponding values, considering the context of the provided title and abstract."},
        {"role": "system", "content": f"Title: {title}"},
        {"role": "system", "content": f"Abstract: {abstract}"},
        {"role": "user",
         "content": f"Generate a hypothetical text using the following information:\nVariable: {variable}\nDefinition: {definition}\nPossible scenarios (corresponding values): {value}\nWhere to find: {where_to_find}"}
    ]

    response = client.chat_completions.create(
        model="gpt-3.5-turbo-0125",
        messages=messages,
        temperature=0.7,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    hypothetical_text = response.choices[0].message.content
    return hypothetical_text
