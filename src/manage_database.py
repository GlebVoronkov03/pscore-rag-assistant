import os
import glob
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

DATA_PATH = "./data/"
CHROMA_PATH = "./chroma_db/"

def update_database():
    """Обновляет векторную базу данных всеми PDF-файлами из папки data"""
    
    # Проверяем существование папки data
    if not os.path.exists(DATA_PATH):
        print("❌ Папка 'data' не существует! Создайте папку и добавьте PDF-файлы.")
        return
    
    # Ищем все PDF-файлы
    pdf_files = glob.glob(os.path.join(DATA_PATH, "*.pdf"))
    
    if not pdf_files:
        print("❌ В папке 'data' не найдено PDF-файлов!")
        return
    
    print("📚 Найдены следующие PDF-файлы:")
    for i, pdf_file in enumerate(pdf_files, 1):
        print(f"   {i}. {os.path.basename(pdf_file)}")
    
    # Загружаем и обрабатываем все документы
    all_documents = []
    for pdf_file in pdf_files:
        try:
            print(f"\n📖 Обрабатывается: {os.path.basename(pdf_file)}")
            loader = PyPDFLoader(pdf_file)
            documents = loader.load()
            all_documents.extend(documents)
            print(f"✅ Загружено {len(documents)} страниц")
        except Exception as e:
            print(f"❌ Ошибка: {str(e)}")
    
    if not all_documents:
        print("❌ Не удалось загрузить ни одного документа!")
        return
    
    # Разбиваем на фрагменты
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=200
    )
    chunks = text_splitter.split_documents(all_documents)
    print(f"\n📊 Всего создано {len(chunks)} текстовых фрагментов")
    
    # Создаем векторную базу
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'}
    )
    
    print("💾 Сохранение в векторную базу данных...")
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_PATH
    )
    
    print("✅ База данных успешно обновлена!")

def check_database():
    """Проверяет состояние базы данных"""
    if os.path.exists(CHROMA_PATH):
        # Можно добавить более детальную проверку
        print("✅ База данных существует")
        return True
    else:
        print("❌ База данных не найдена")
        return False

if __name__ == "__main__":
    print("🛠️ Менеджер базы знаний")
    print("1. Обновить базу данных")
    print("2. Проверить базу данных")
    
    choice = input("Выберите действие (1 или 2): ").strip()
    
    if choice == "1":
        update_database()
    elif choice == "2":
        check_database()
    else:
        print("❌ Неверный выбор")
        