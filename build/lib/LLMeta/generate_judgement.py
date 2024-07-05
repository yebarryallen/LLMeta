import numpy as np
from openai import OpenAI


def generate_judgement(client, result_string, variable, definition, possible_values, title, abstract, format=None,
                       selected_model="gpt-3.5-turbo-0125"):
    if format is None:
        format = """The output should be a JSON string with the following format:{"value": str   Based on the given context, determine the content. If the article mentions the concept corresponding to the variable and the situation matches one of the values in 'value', fill in the corresponding value. If the variable is not mentioned or there is no corresponding value for the situation, fill in None.}"""

    response = client.chat_completions.create(
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
