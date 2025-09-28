import sys

def rag_chatter():
    from .chatter import Chatter
    input_text: str = "The meaning of life is 42"
    question: str =  "What is Task Decomposition?"

    chatter = Chatter(embedding_model="EmbeddingGemma", model="gemma3")
    chatter.add_text_embeddings(input_text)
    all_splits = chatter.load_website(
        "https://lilianweng.github.io/posts/2023-06-23-agent/"
    )
    print(f"Loaded {len(all_splits)} document splits")
    chatter.answer(question)

def read_pdf(file_path: str):
    from formats.pdf import PdfExtractor
    extractor = PdfExtractor()
    text = extractor.extract_with_pdfplumber(file_path)
    return text

def main(args: list[str]):
    if args:
        print(read_pdf(args[0]))
    else:
        print("No PDF file path provided.")


if __name__ == "__main__":
    main(sys.argv[1:])