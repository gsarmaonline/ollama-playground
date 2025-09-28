import sys

def rag_chatter():
    from chatter import Chatter
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

def categorise_resume_pdf(file_path: str):
    """Use RAG to answer questions about a PDF document."""
    from chatter import Chatter
    
    question: str = "Return his skills categorised by industry in a json format"
    
    # Initialize chatter
    chatter = Chatter(embedding_model="EmbeddingGemma", model="gemma3")
    
    # Load PDF into RAG system
    splits = chatter.load_pdf(file_path)
    print(f"\nLoaded {len(splits)} document splits")
    
    # Answer the question
    print("\n=== ANSWER ===")
    answer = chatter.answer(question)
    print(answer)
    
    return answer

def main(args: list[str]):
    if len(args) == 0:
        print("Invalid arguments. Use 'python run.py' for usage help.")
    else:
        # Default: just extract text
        print(categorise_resume_pdf(args[0]))


if __name__ == "__main__":
    main(sys.argv[1:])