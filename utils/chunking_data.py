from langchain.text_splitter import RecursiveCharacterTextSplitter

def chunk_documents(docs, chunk_size=3000, chunk_overlap=300, separators=None):
    if separators is None:
        separators = ["\n\n", "\n", "Section ", "SECTION ", "Sec. ", "CHAPTER ", "Chapter ", " "]
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=separators
    )
    return splitter.split_documents(docs)
