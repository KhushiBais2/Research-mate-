from pypdf import PdfReader


def extract_text_from_pdf(pdf_path):

    reader = PdfReader(pdf_path)

    extracted_pages = []

    for page_number, page in enumerate(reader.pages, start=1):

        text = page.extract_text()

        if text and text.strip():

            extracted_pages.append({
                "text": text,
                "page": page_number
            })

    return extracted_pages
