# PS Core RAG Assistant

Local **RAG chatbot** for packet-core / telecom engineering documentation.

Stack: **LangChain + ChromaDB + Hugging Face embeddings + Ollama (Qwen2.5:7B)**.

> Author: Gleb Voronkov · Apache-2.0

## Why it matters
Engineers waste time searching multi-hundred-page standards. This assistant builds a **local** vector knowledge base from documents and answers in RU/EN **without sending data to the cloud** (after models are pulled).

## Architecture
```
PDF/MD docs → RecursiveCharacterTextSplitter → HF embeddings (all-MiniLM-L6-v2)
        → Chroma persistent store → Ollama Qwen2.5:7B → answer
```

## Quickstart
1. Install [Ollama](https://ollama.com) and pull the model:
   ```powershell
   ollama pull qwen2.5:7b
   ```
2. Run:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   python src/ai_assistant_complete.py
   ```
3. Put docs into `data/` (a synthetic sample is included), build the knowledge base from the menu, ask questions.

## Notes
- Production deployments used larger private corpora (up to multi‑GB). This public repo ships **synthetic sample docs only**.
- Typical local answer latency depends on GPU/CPU; on a capable NVIDIA box responses were often in the **5–40 s** range for Qwen2.5:7B.

## License
Apache-2.0. Contact: `mybook3@mail.ru` / Telegram `@Gleb_Voronkov`.