from pypdf import PdfReader


def extract_text(pdf_path):
    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


pdf_path = "data/papers/Biodiversity_For_Food_and_Agriculture.pdf"

text = extract_text(pdf_path)

print("Characters extracted:", len(text))
print("\nFirst 1000 characters:\n")
print(text[:1000])