def save_vectorstore(vector_name, saving_path, text_chunks):
    from langchain.vectorstores import FAISS
    from langchain_openai import OpenAIEmbeddings
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    FAISS.save_local(vectorstore, saving_path, vector_name)
