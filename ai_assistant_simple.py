# ai_assistant_simple.py
import os
import sys
import subprocess
import glob
import time

def setup_environment():
    """Создает необходимые папки"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, "data")
    chroma_path = os.path.join(base_dir, "chroma_db")
    
    os.makedirs(data_path, exist_ok=True)
    os.makedirs(chroma_path, exist_ok=True)
    
    return base_dir, data_path, chroma_path

def check_dependencies():
    """Проверяет наличие необходимых библиотек"""
    try:
        # Пытаемся импортировать все необходимые библиотеки
        import langchain_community
        import chromadb
        import sentence_transformers
        import pypdf
        print("✅ Все библиотеки загружены успешно")
        return True
    except ImportError as e:
        print(f"❌ Ошибка импорта: {e}")
        return False

def check_ollama():
    """Проверяет наличие Ollama"""
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=10)
        if "qwen2.5:7b" in result.stdout:
            print("✅ Модель qwen2.5:7b найдена")
            return True
        else:
            print("❌ Модель qwen2.5:7b не найдена")
            return False
    except:
        print("❌ Ollama не установлена или не запущена")
        return False

def create_database():
    """Создает базу знаний из PDF файлов"""
    base_dir, data_path, chroma_path = setup_environment()
    
    pdf_files = glob.glob(os.path.join(data_path, "*.pdf"))
    if not pdf_files:
        print("❌ В папке 'data' нет PDF файлов!")
        print(f"📁 Добавьте файлы в: {data_path}")
        return False
    
    print(f"📚 Найдено {len(pdf_files)} PDF файлов")
    
    try:
        # Импортируем здесь, чтобы ошибки были видны
        from langchain_community.document_loaders import PyPDFLoader
        from langchain_text_splitters import RecursiveCharacterTextSplitter
        from langchain_community.embeddings import HuggingFaceEmbeddings
        from langchain_community.vectorstores import Chroma
        
        all_documents = []
        for pdf_file in pdf_files:
            print(f"📖 Обрабатывается: {os.path.basename(pdf_file)}")
            loader = PyPDFLoader(pdf_file)
            documents = loader.load()
            all_documents.extend(documents)
            print(f"✅ Загружено {len(documents)} страниц")
        
        # Разбиваем на фрагменты
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=100
        )
        chunks = text_splitter.split_documents(all_documents)
        print(f"📊 Создано {len(chunks)} фрагментов")
        
        # Создаем базу данных
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        
        Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=chroma_path
        )
        
        print("✅ База знаний создана!")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при создании базы: {e}")
        return False

def run_assistant():
    """Запускает ассистента"""
    base_dir, data_path, chroma_path = setup_environment()
    
    # Проверяем базу данных
    if not os.path.exists(chroma_path) or not os.listdir(chroma_path):
        print("❌ База знаний не найдена!")
        return
    
    try:
        from langchain_community.embeddings import HuggingFaceEmbeddings
        from langchain_community.vectorstores import Chroma
        from langchain_community.chat_models import ChatOllama
        
        # Загружаем базу и модель
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        vectorstore = Chroma(persist_directory=chroma_path, embedding_function=embeddings)
        llm = ChatOllama(model="qwen2.5:7b", temperature=0.1)
        
        print("✅ Ассистент готов!")
        print("💡 Задавайте вопросы (для выхода введите 'exit')")
        
        while True:
            question = input("\n🧑 Ваш вопрос: ").strip()
            if question.lower() in ['exit', 'quit']:
                break
            
            try:
                docs = vectorstore.similarity_search(question, k=3)
                context = "\n\n".join([doc.page_content for doc in docs])
                
                prompt = f"Ответь на русском на основе контекста: {context}\n\nВопрос: {question}\n\nОтвет:"
                response = llm.invoke(prompt)
                print(f"\n🤖 {response.content}")
                
            except Exception as e:
                print(f"❌ Ошибка: {e}")
                
    except Exception as e:
        print(f"❌ Ошибка запуска ассистента: {e}")

def show_menu():
    """Показывает главное меню"""
    base_dir, data_path, chroma_path = setup_environment()
    
    while True:
        print("\n" + "="*50)
        print("🤖 AI-АССИСТЕНТ HUAWEI")
        print("="*50)
        print("1. 📚 Создать базу знаний из PDF в папке 'data'")
        print("2. 🗣️  Запустить ассистента")
        print("3. 📊 Проверить систему")
        print("4. 🚪 Выйти")
        print("="*50)
        
        choice = input("Выберите действие (1-4): ").strip()
        
        if choice == "1":
            create_database()
        elif choice == "2":
            run_assistant()
        elif choice == "3":
            check_dependencies()
            check_ollama()
            pdf_files = glob.glob(os.path.join(data_path, "*.pdf"))
            print(f"📄 PDF файлов: {len(pdf_files)}")
        elif choice == "4":
            print("👋 До свидания!")
            break
        else:
            print("❌ Неверный выбор")

def main():
    """Основная функция"""
    print("🚀 Запуск AI Assistant...")
    
    # Настраиваем окружение
    base_dir, data_path, chroma_path = setup_environment()
    
    # Проверяем зависимости
    if not check_dependencies():
        print("\n⚠️  Не все библиотеки доступны!")
        print("   Убедитесь, что все зависимости установлены")
        input("Нажмите Enter для выхода...")
        return
    
    # Проверяем Ollama
    if not check_ollama():
        print("\n⚠️  Ollama не настроена!")
        print("   Скачайте с ollama.com и выполните: ollama pull qwen2.5:7b")
    
    # Показываем меню
    show_menu()

if __name__ == "__main__":
    main()