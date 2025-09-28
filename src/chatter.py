from typing import Optional
from langchain_ollama import OllamaEmbeddings
from langchain_ollama import ChatOllama
from langchain_core.vectorstores import InMemoryVectorStore
import bs4
from langchain import hub
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.documents import Document
from langchain_core.messages.base import BaseMessage
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.graph import START, StateGraph
from typing_extensions import List, TypedDict


class UsageMetadata(TypedDict):
    input_tokens: Optional[int]
    output_tokens: Optional[int]
    total_tokens: Optional[int]

class ResponseMetadata(TypedDict):
    model: str
    usage: Optional[UsageMetadata]
    done: bool
    total_duration: Optional[float]
    load_duration: Optional[float]
    prompt_eval_count: Optional[int]
    prompt_eval_duration: Optional[float]
    eval_duration: Optional[float]
    eval_count: Optional[int]


class Chatter:
    def __init__(self, embedding_model: str, model: str):
        self.model: str = model
        self.embeddings: OllamaEmbeddings = OllamaEmbeddings(model=embedding_model)
        self.vector_store: InMemoryVectorStore = InMemoryVectorStore(self.embeddings)
        self.llm: ChatOllama = ChatOllama(
            model=self.model,
            validate_model_on_init=True,
            temperature=0.8,
            num_predict=256,
        )
        self.prompt = hub.pull("rlm/rag-prompt", api_url="https://api.smith.langchain.com")


    def load_website(self, website_url: str) -> list[Document]:
        loader = WebBaseLoader(
            web_paths=(website_url,),
            bs_kwargs=dict(
                parse_only=bs4.SoupStrainer( # type: ignore
                    class_=("post-content", "post-title", "post-header")
                )
            ),
        )
        docs = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        all_splits: list[Document] = text_splitter.split_documents(docs)

        self.vector_store.add_documents(documents=all_splits)
        return all_splits

    def add_text_embeddings(self, input_text: str) -> None:
        self.vector_store.add_texts(texts=[input_text], metadatas=[{"source": "user_input"}])

    def answer(self, question: str) -> str:
        retrieved_docs = self.vector_store.similarity_search(question)
        docs_content = "\n\n".join(doc.page_content for doc in retrieved_docs)
        prompt = self.prompt.invoke({"question": question, "context": docs_content})
        response: BaseMessage = self.llm.invoke(prompt)
        #print(response.content, response.response_metadata)
        return response.content # type: ignore

    def load_pdf(self, file_path: str, chunk_size: int = 1500, chunk_overlap: int = 200) -> List[Document]:
        """Load and process PDF file for RAG."""
        from formats.pdf import PdfExtractor
        
        extractor = PdfExtractor()
        pdf_text = extractor.extract_with_pdfplumber(file_path)
        
        # Create a document with PDF metadata
        doc = Document(
            page_content=pdf_text,
            metadata={
                "source": file_path,
                "type": "pdf",
                "filename": file_path.split("/")[-1]
            }
        )
        
        # Split the document into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, 
            chunk_overlap=chunk_overlap
        )
        all_splits = text_splitter.split_documents([doc])
        
        # Add to vector store
        self.vector_store.add_documents(documents=all_splits)
        return all_splits


