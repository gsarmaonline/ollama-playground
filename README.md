# Ollama Playground

A Python application that demonstrates Retrieval-Augmented Generation (RAG) using Ollama with Gemma models for chat and embedding generation.

## Prerequisites

### 1. Install Ollama

First, install Ollama on your system:

**macOS:**

```bash
brew install ollama
```

**Linux:**

```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### 2. Start Ollama Service

Start the Ollama service:

```bash
ollama serve
```

### 3. Pull Required Models

This application uses two Gemma models:

**For Chat (gemma2:2b):**

```bash
ollama pull gemma3
```

**For Embeddings:**

```bash
ollama pull EmbeddingGemma
```

> **Note:** The code references "gemma3" and "EmbeddingGemma" but these should map to available Ollama models. You may need to adjust the model names in the code or pull different models based on availability.

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/gsarmaonline/ollama-playground.git
cd ollama-playground
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Configuration

The application is configured to use:

- **Chat Model:** `gemma3` (you may need to change this to `gemma2:2b` or another available model)
- **Embedding Model:** `EmbeddingGemma` (you may need to change this to `mxbai-embed-large` or another embedding model)

To modify the models, edit the `main()` function in `src/run.py`:

```python
chatter = Chatter(embedding_model="mxbai-embed-large", model="gemma2:2b")
```

## Running the Application

### Method 1: Direct Execution

```bash
cd src
python run.py
```

### Method 2: Module Execution

```bash
python -m src.run
```

## How It Works

1. **Initialization:** Creates a `Chatter` instance with specified Ollama models
2. **Text Embedding:** Adds sample text to the vector store
3. **Web Content Loading:** Scrapes and processes content from a specified URL (default: Lilian Weng's blog post on AI agents)
4. **Document Splitting:** Breaks down the content into manageable chunks
5. **Question Answering:** Uses RAG to answer questions based on the loaded content

## Example Output

The application will:

1. Load and process document splits from the web
2. Print the number of loaded document splits
3. Answer the question "What is Task Decomposition?" using the loaded context
4. Display the response along with metadata

## Customization

### Changing the Data Source

Modify the website URL in `src/run.py`:

```python
all_splits = chatter.load_website("https://your-website-here.com")
```

### Modifying Questions

Change the question in `src/run.py`:

```python
question: str = "Your question here?"
```

### Adjusting Model Parameters

Edit the `Chatter` class initialization in `src/chatter.py`:

```python
self.llm: ChatOllama = ChatOllama(
    model=self.model,
    validate_model_on_init=True,
    temperature=0.8,  # Adjust creativity (0.0 = deterministic, 1.0 = creative)
    num_predict=256,  # Maximum tokens in response
)
```

## Troubleshooting

### Common Issues

1. **Model Not Found:**

   - Ensure Ollama is running: `ollama serve`
   - Check available models: `ollama list`
   - Pull required models if missing

2. **Connection Errors:**

   - Verify Ollama is running on the default port (11434)
   - Check firewall settings

3. **Import Errors:**
   - Ensure virtual environment is activated
   - Reinstall dependencies: `pip install -r requirements.txt`

### Checking Ollama Status

```bash
# List available models
ollama list

# Check if Ollama is running
curl http://localhost:11434/api/tags

# Test a model
ollama run gemma2:2b "Hello, world!"
```

## Project Structure

```
ollama-playground/
├── requirements.txt          # Python dependencies
├── README.md                # This file
└── src/
    ├── __init__.py          # Package initialization
    ├── chatter.py           # Main Chatter class with RAG implementation
    └── run.py               # Entry point script
```

## License

This project is open source. Please check the repository for license details.
