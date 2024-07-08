# LLMeta

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
[![PyPI version](https://badge.fury.io/py/LLMeta.svg)](https://pypi.org/project/LLMeta/)
[![Website](https://img.shields.io/badge/Website-Jinquan_Ye-red)](https://jinquanyescholar.netlify.app)
[![Website](https://img.shields.io/badge/Website-Ziqian_Xia-blue)](https://ziqian-xia.tech/)
[![Twitter Follow](https://img.shields.io/twitter/follow/yebarryallen.svg?style=social)](https://x.com/yebarryallen)
[![Twitter Follow](https://img.shields.io/twitter/follow/Ziqian_Xia.svg?style=social)](https://x.com/Ziqian_Xia)

![img.png](img.png)


LLMeta is a Python package designed for conducting systematic reviews using large language models in conjunction with Retrieval Augmented Generation (RAG) and Hypothetical Document Embeddings (HyDE) techniques.


## Installation

To install LLMeta, you can use pip:

```bash
pip install LLMeta
```
## Table of Contents
- [Setup](#setup)
- [Markdown File Processing](#markdown-file-processing)
  - [split_markdown_file](#split_markdown_file)
  - [save_vectorstore](#save_vectorstore)
  - [markdown_to_vectorstore](#markdown_to_vectorstore)
- [Text Generation](#text-generation)
  - [generate_hypothetical_text](#generate_hypothetical_text)
  - [get_relate_doc](#get_relate_doc)
  - [generate_judgement](#generate_judgement)
- [Paper Processing](#paper-processing)
  - [process_row](#process_row)
  - [process_papers](#process_papers)
- [Output Formatting](#output-formatting)
  - [formated_output](#formated_output)

# LLMeta Python Package Documentation


## Setup

### `setup`
This function creates the necessary directories for the LLMeta project. It initializes folders such as `markdown_file`, `pdf_folder`, `raw_output`, `temp`, and `vectorstore` to organize project files.

## Markdown File Processing

### `split_markdown_file`
This function reads a markdown file, splits it into sections based on a delimiter (`---\n`), and returns a list of these sections. It appends part of the next section's beginning to each section to ensure context continuity.

### `save_vectorstore`
This function saves text chunks into a vectorstore using the FAISS library for efficient retrieval. It uses OpenAI embeddings to convert text chunks into vectors.

### `markdown_to_vectorstore`
This function processes all markdown files in a specified directory, splits them into sections, and saves these sections into a vectorstore for later retrieval.

## Text Generation

### `generate_hypothetical_text`
This function generates a hypothetical text based on given variables, their definitions, and values, within the context of a provided title and abstract. It uses OpenAI's language model to create plausible paragraphs.

### `get_relate_doc`
This function retrieves relevant documents from a vectorstore based on a hypothetical text. It uses FAISS for document retrieval and provides the most relevant passages from the original documents.

### `generate_judgement`
This function generates a judgement or extraction based on the retrieved relevant documents. It evaluates if the text mentions a specific variable and matches its values, outputting the result in a JSON format.

## Paper Processing

### `process_row`
This function processes a single row of data, generating hypothetical texts, retrieving relevant documents, and generating judgements. It saves the results, including extracted values and probability scores, to text files.

### `process_papers`
This function processes multiple papers concurrently, using `process_row` for each paper. It reads variable lists and merged data, then applies the processing to each paper's data.

## Output Formatting

### `formated_output`
This function formats the extracted data and probabilities into a structured CSV file. It reads answer, source, and probability files, processes them, and merges the results with the original metadata and variable definitions.

## Citation


