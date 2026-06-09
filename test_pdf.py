import fitz

doc = fitz.open("RAG paper.pdf")

print(len(doc))

print(doc[0].get_text()[:500])
