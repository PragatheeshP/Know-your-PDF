from langchain_text_splitters import (
    RecursiveCharacterTextSplitter)
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200)
def chunk_pages(pages):
    chunks = []

    for page in pages:
        splits = splitter.split_text(
            page["text"]
        )
        for chunk in splits:
            chunks.append(
                {
                    "text": chunk,
                    "page": page["page"]
                }
            )
    return chunks