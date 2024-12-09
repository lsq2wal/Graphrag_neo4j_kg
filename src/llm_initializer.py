from langchain_ollama import ChatOllama

def initialize_llm():
    return ChatOllama(
        model="llama3.1",
        temperature=0.5,
        base_url="http://localhost:11434"  # 本地 Ollama 服务的 URL
    )
