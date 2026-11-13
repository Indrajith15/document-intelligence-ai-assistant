from langchain_text_splitters import RecursiveCharacterTextSplitter

def process_document(pdf_reader, filename):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    all_chunks = []

    for page_number, page in enumerate(pdf_reader.pages, start=1):
        page_text = page.extract_text() or ""

        page_chunks = text_splitter.split_text(page_text)

        for chunk_number, chunk in enumerate(page_chunks):
            all_chunks.append({
                "text": chunk,
                "metadata": {
                    "filename": filename,
                    "page": page_number,
                    "chunk_id": len(all_chunks)
                }
            })

    return all_chunks
