## End-to-End RAG & Agentic AI Platform

A collection of notebooks and resources exploring Retrieval-Augmented Generation (RAG) and LlamaIndex. This repo is organized primarily around Jupyter notebooks under `LlamaIndex/KN LlamaIndex/`.

### Repo structure
- `LlamaIndex/KN LlamaIndex/` – notebooks, e.g. `Llama2_with_llamaindex.ipynb`, `Basic Rag/test.ipynb`
- `data/` (ignored) – raw/private datasets
- `storage/`, `index_storage/`, `vector_store/` (ignored) – LlamaIndex artifacts
- `models/`, `checkpoints/`, `outputs/` (ignored) – model weights and generated artifacts

### Requirements
- Python 3.10+
- pip (or conda/mamba)
- Jupyter Lab/Notebook

Suggested Python packages (install as needed):
- `llama-index` and relevant integrations (LLMs/vector stores you plan to use)
- `jupyter`, `ipykernel`, `python-dotenv`

### Quick start
1) Create and activate a virtual environment
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows PowerShell/CMD
```

2) Install packages
```bash
python -m pip install --upgrade pip
pip install jupyter ipykernel python-dotenv llama-index
# add any extra integrations you need, e.g.:
# pip install llama-index-llms-openai llama-index-embeddings-openai
```

3) Register the kernel (optional, for a named Jupyter kernel)
```bash
python -m ipykernel install --user --name hamza-venv --display-name "Hamza (venv)"
```

4) Launch Jupyter and open notebooks
```bash
jupyter lab
# or: jupyter notebook
```

### Environment variables
Create a `.env` file at the repo root for credentials and settings (kept out of git by `.gitignore`). Example:
```bash
OPENAI_API_KEY=...
ANTHROPIC_API_KEY=...
LLAMA_CLOUD_API_KEY=...
```
Load with `python-dotenv` inside notebooks if needed.

### Data and artifacts
- Keep raw data in `data/` and large/generated artifacts in `outputs/`, `models/`, `storage/` etc. These are ignored by default.
- If you want to commit small sample files, add a `README.md` inside those ignored folders and unignore selectively in `.gitignore`.

### Tips (Windows)
- If you hit long path issues, enable long paths in Windows or keep repo path short.
- For large binary files (e.g., model weights), consider Git LFS.

### License
Add your preferred license here.

