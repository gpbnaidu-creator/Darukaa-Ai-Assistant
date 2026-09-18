import json
from pdf_loader import extract_text
from langchain_text_splitters import RecursiveCharacterTextSplitter


pdf_path = "data/papers/Biodiversity_For_Food_and_Agriculture.pdf"

text = extract_text(pdf_path)


splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = splitter.split_text(text)



print("Total chunks:", len(chunks))

print("\nFirst chunk:\n")
print(chunks[0])


with open("chunks.json", "w", encoding="utf-8") as file:
    json.dump(chunks, file, ensure_ascii=False, indent=2)

print("\nChunks saved to chunks.json")    
     