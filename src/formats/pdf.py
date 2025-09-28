

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
