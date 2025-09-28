from .chatter import Chatter


def main():
    input_text: str = "The meaning of life is 42"
    question: str =  "What is Task Decomposition?"

    chatter = Chatter(embedding_model="EmbeddingGemma", model="gemma3")
    chatter.add_text_embeddings(input_text)
    all_splits = chatter.load_website(
        "https://lilianweng.github.io/posts/2023-06-23-agent/"
    )
    print(f"Loaded {len(all_splits)} document splits")
    chatter.answer(question)


if __name__ == "__main__":
    main()