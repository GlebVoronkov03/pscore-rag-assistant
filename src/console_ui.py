# console_ui.py
import os
import glob
import sys
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.chat_models import ChatOllama

DATA_PATH = "./data/"
CHROMA_PATH = "./chroma_db/"

def setup_qa_system():
    """Настраивает систему вопрос-ответ"""
    try:
        # Загружаем эмбеддинги
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'}
        )
        
        # Загружаем векторную базу
        vectorstore = Chroma(
            persist_directory=CHROMA_PATH,
            embedding_function=embeddings
        )
        
        # Настраиваем языковую модель
        llm = ChatOllama(
            model="qwen2.5:7b",
            temperature=0.1,
            num_ctx=2048,
            num_gpu=1
        )
        
        return llm, vectorstore
        
    except Exception as e:
        print(f"❌ Ошибка при настройке системы: {str(e)}")
        return None, None

def ask_question(llm, vectorstore, question):
    """Задает вопрос ассистенту и возвращает ответ"""
    try:
        # Ищем релевантные документы
        docs = vectorstore.similarity_search(question, k=3)
        
        if not docs:
            return "🤷 Не найдено подходящей информации в документации."
        
        # Создаем контекст из найденных документов
        context = "\n\n".join([doc.page_content for doc in docs])
        
        # Создаем промпт вручную
        prompt = f"""
        Ты — AI-ассистент для инженеров мобильной связи. Отвечай на русском языке.
        Используй ТОЛЬКО предоставленный контекст из документации.
        
        Контекст из документации:
        {context}
        
        Вопрос: {question}
        
        Ответ (будь точным и используй только информацию из контекста):
        """
        
        # Получаем ответ
        response = llm.invoke(prompt)
        return response.content
        
    except Exception as e:
        return f"❌ Ошибка при получении ответа: {str(e)}"

def show_menu():
    """Показывает главное меню"""
    print("\n" + "="*50)
    print("🤖 AI-АССИСТЕНТ ДЛЯ ИНЖЕНЕРОВ МОБИЛЬНОЙ СВЯЗИ")
    print("="*50)
    print("1. 🗣️  Задать вопрос")
    print("2. 📊  Проверить состояние системы")
    print("3. 📚  Обновить базу знаний (добавлены новые PDF)")
    print("4. 🚪  Выйти")
    print("="*50)

def check_system_status():
    """Проверяет состояние системы"""
    print("\n--- 📊 СТАТУС СИСТЕМЫ ---")
    
    # Проверяем базу данных
    if os.path.exists(CHROMA_PATH):
        try:
            embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                model_kwargs={'device': 'cpu'}
            )
            vectorstore = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
            count = vectorstore._collection.count()
            print(f"✅ База знаний: загружена ({count} фрагментов)")
        except:
            print("❌ База знаний: повреждена")
    else:
        print("❌ База знаний: не найдена")
    
    # Проверяем папку с документами
    pdf_files = glob.glob(os.path.join(DATA_PATH, "*.pdf"))
    print(f"📚 PDF-документов: {len(pdf_files)} файлов")
    
    # Проверяем Ollama
    try:
        import subprocess
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
        if "qwen2.5:7b" in result.stdout:
            print("✅ Модель Qwen2.5: загружена")
        else:
            print("❌ Модель Qwen2.5: не найдена")
    except:
        print("❌ Ollama: не запущена")

def main():
    """Основная функция"""
    print("Загрузка AI-ассистента...")
    
    # Проверяем существование базы данных
    if not os.path.exists(CHROMA_PATH):
        print("❌ База данных не найдена. Сначала запустите:")
        print("   python manage_database.py")
        print("   И выберите опцию 1 для создания базы знаний.")
        return
    
    print("⚙️ Загрузка AI-модели...")
    llm, vectorstore = setup_qa_system()
    
    if llm is None:
        print("❌ Не удалось настроить систему. Проверьте:")
        print("   1. Запущена ли Ollama (ollama serve)")
        print("   2. Загружена ли модель (ollama list)")
        print("   3. Существует ли база данных в папке chroma_db")
        return
    
    print("✅ Система готова к работе!")
    
    while True:
        try:
            show_menu()
            choice = input("\nВыберите действие (1-4): ").strip()
            
            if choice == "1":
                question = input("\n🧑 Введите ваш вопрос: ").strip()
                if question:
                    print("\n⏳ Ассистент думает...")
                    answer = ask_question(llm, vectorstore, question)
                    print(f"\n🤖 Ответ: {answer}")
                else:
                    print("❌ Вопрос не может быть пустым.")
                    
            elif choice == "2":
                check_system_status()
                
            elif choice == "3":
                print("\n🔄 Для обновления базы знаний выполните:")
                print("   python manage_database.py")
                print("   Затем выберите опцию 1")
                input("   Нажмите Enter для возврата в меню...")
                
            elif choice == "4":
                print("👋 До свидания!")
                break
            else:
                print("❌ Неверный выбор. Попробуйте снова.")
                
        except KeyboardInterrupt:
            print("\n👋 До свидания!")
            break
        except Exception as e:
            print(f"❌ Произошла непредвиденная ошибка: {str(e)}")

if __name__ == "__main__":
    main()