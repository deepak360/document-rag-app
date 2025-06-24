import fitz  # PyMuPDF

def extract_text(filepath: str) -> str:
    if filepath.endswith(".pdf"):
        return extract_pdf_text(filepath)
    elif filepath.endswith(".docx"):
        return extract_docx_text(filepath)
    else:
        return ""

def extract_pdf_text(filepath: str) -> str:
    text = ""
    with fitz.open(filepath) as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_docx_text(filepath: str) -> str:
    from docx import Document
    doc = Document(filepath)
    return "\n".join([p.text for p in doc.paragraphs])
