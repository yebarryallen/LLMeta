
def get_relate_doc(client, vector_name, vectorstore_path, apikey, hypothetical_text, variable):
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
