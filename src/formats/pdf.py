import pymupdf


class PdfExtractor:
    def extract_text(self, file_path):
        import pymupdf # imports the pymupdf library
        """Extract text from a PDF file."""
        text_content = []
        doc = pymupdf.open(file_path)  # open the PDF document
        for page in doc:  # iterate through the pages
            text = page.get_text()  # type: ignore # extract text from each page
            text_content.append(text)
        return "\n".join(text_content)  # join all page texts into a single string

    def extract_as_markdown(self, file_path: str) -> str:
        import pymupdf4llm
        """Extract text from a PDF file and convert to markdown."""
        md_text = pymupdf4llm.to_markdown(file_path)
        return str(md_text.encode())

    def extract_with_pdfplumber(self, file_path: str) -> str:
        import pdfplumber
        
        all_pages_text = []
        
        with pdfplumber.open(file_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                page_text = page.extract_text()
                if page_text:
                    all_pages_text.append(f"# Page {page_num}\n\n{page_text}\n")
        
        return '\n---\n'.join(all_pages_text)