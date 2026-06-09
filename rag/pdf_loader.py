import fitz
def extract_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    pages = []
    for page_num in range(len(doc)):
        text = doc[page_num].get_text()
        pages.append(
            {
                "page": page_num + 1,
                "text": text
            }
        )
    return pages