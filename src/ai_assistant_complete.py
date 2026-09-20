import os
import sys
import subprocess
import shutil
import glob
import time
from pathlib import Path

# Добавляем текущую директорию в путь для импортов
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

try:
    from langchain_community.document_loaders import PyPDFLoader
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_community.embeddings import HuggingFaceEmbeddings
    from langchain_community.vectorstores import Chroma
    from langchain_community.chat_models import ChatOllama
except ImportError as e:
    print(f"❌ Ошибка импорта библиотек: {e}")
    print("Убедитесь, что все зависимости установлены")
    input("Нажмите Enter для выхода...")
    sys.exit(1)

class AIAssistantComplete:
    def __init__(self):
        self.base_dir = self.get_base_dir()
        self.data_path = os.path.join(self.base_dir, "data")
        self.chroma_path = os.path.join(self.base_dir, "chroma_db")
        self.readme_path = os.path.join(self.base_dir, "README.txt")
        
    def get_base_dir(self):
        """Определяет правильную базовую директорию"""
        if getattr(sys, 'frozen', False):
            return os.path.dirname(sys.executable)
        else:
            return os.path.dirname(os.path.abspath(__file__))
    
    def setup_environment(self):
        """Создает все необходимые папки и файлы"""
        print("🛠️  Настройка окружения...")
        
        # Создаем папки
        os.makedirs(self.data_path, exist_ok=True)
        os.makedirs(self.chroma_path, exist_ok=True)
        
        # Создаем README файл
        self.create_readme()
        
        print(f"✅ Папка для документов: {self.data_path}")
        print(f"✅ Папка базы данных: {self.chroma_path}")
        
        return True
    
    def create_readme(self):
        """Создает файл с инструкцией для пользователя"""
        readme_content = """🤖 AI-АССИСТЕНТ ДЛЯ ИНЖЕНЕРОВ HUAWEI

📋 КРАТКАЯ ИНСТРУКЦИЯ:

1. ДОБАВЛЕНИЕ ДОКУМЕНТОВ:
   - Положите PDF-файлы с документацией Huawei в папку 'data'
   - Перезапустите программу и выберите "Создать базу знаний"

2. ЗАПУСК АССИСТЕНТА:
   - После создания базы знаний выберите "Запустить ассистента"
   - Задавайте вопросы на русском или английском

3. ТРЕБОВАНИЯ К СИСТЕМЕ:
   - Установленная Ollama (скачайте с ollama.com)
   - Загруженная модель: qwen2.5:7b (запустите: ollama pull qwen2.5:7b)
   - Видеокарта NVIDIA с 4+ ГБ памяти (рекомендуется)

📞 ПОДДЕРЖКА:
   - Программа работает полностью локально
   - Не требует интернета после настройки
   - Данные не передаются третьим лицам

💡 ПРИМЕРЫ ВОПРОСОВ:
   - "Что такое 5G Core Network?"
   - "Опиши архитектуру пакетной маршрутизации"
   - "Какие протоколы использует Huawei?"
"""
        with open(self.readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
    
    def check_ollama(self):
        """Проверяет установку Ollama и наличие модели"""
        print("🔍 Проверка Ollama...")
        
        try:
            # Проверяем, что Ollama установлена
            result = subprocess.run(["ollama", "list"], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=30)
            
            if result.returncode != 0:
                print("❌ Ollama не установлена или не запущена")
                print("📥 Скачайте с: https://ollama.com")
                return False
            
            # Проверяем наличие модели
            if "qwen2.5:7b" in result.stdout:
                print("✅ Модель qwen2.5:7b загружена")
                return True
            else:
                print("❌ Модель qwen2.5:7b не найдена")
                print("📥 Загрузите модель командой: ollama pull qwen2.5:7b")
                return False
                
        except subprocess.TimeoutExpired:
            print("❌ Таймаут проверки Ollama")
            return False
        except Exception as e:
            print(f"❌ Ошибка проверки Ollama: {e}")
            return False
    
    def create_database(self):
        """Создает базу знаний из PDF-файлов"""
        print("📚 Создание базы знаний...")
        
        # Проверяем наличие PDF-файлов
        pdf_files = glob.glob(os.path.join(self.data_path, "*.pdf"))
        if not pdf_files:
            print("❌ В папке 'data' нет PDF-файлов!")
            print(f"📁 Добавьте файлы в: {self.data_path}")
            input("Нажмите Enter для продолжения...")
            return False
        
        print(f"📄 Найдено PDF-файлов: {len(pdf_files)}")
        
        try:
            all_documents = []
            
            for pdf_file in pdf_files:
                try:
                    print(f"📖 Обрабатывается: {os.path.basename(pdf_file)}")
                    loader = PyPDFLoader(pdf_file)
                    documents = loader.load()
                    all_documents.extend(documents)
                    print(f"✅ Загружено {len(documents)} страниц")
                except Exception as e:
                    print(f"❌ Ошибка при обработке {pdf_file}: {e}")
                    continue
            
            if not all_documents:
                print("❌ Не удалось загрузить ни одного документа!")
                return False
            
            # Разбиваем на фрагменты
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=800,
                chunk_overlap=100
            )
            chunks = text_splitter.split_documents(all_documents)
            print(f"📊 Создано {len(chunks)} текстовых фрагментов")
            
            # Создаем векторную базу
            embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                model_kwargs={'device': 'cpu'}
            )
            
            print("💾 Сохранение в базу данных...")
            Chroma.from_documents(
                documents=chunks,
                embedding=embeddings,
                persist_directory=self.chroma_path
            )
            
            print("✅ База знаний успешно создана!")
            return True
            
        except Exception as e:
            print(f"❌ Ошибка при создании базы знаний: {e}")
            return False
    
    def check_database_exists(self):
        """Проверяет существование базы знаний"""
        if not os.path.exists(self.chroma_path) or not os.listdir(self.chroma_path):
            return False
        
        try:
            embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                model_kwargs={'device': 'cpu'}
            )
            vectorstore = Chroma(persist_directory=self.chroma_path, embedding_function=embeddings)
            count = vectorstore._collection.count()
            return count > 0
        except:
            return False
    
    def run_assistant(self):
        """Запускает AI-ассистента"""
        if not self.check_database_exists():
            print("❌ База знаний не найдена или пуста!")
            print("📝 Сначала создайте базу знаний через главное меню")
            input("Нажмите Enter для продолжения...")
            return
        
        print("🚀 Запуск AI-ассистента...")
        
        try:
            # Настраиваем систему
            embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                model_kwargs={'device': 'cpu'}
            )
            vectorstore = Chroma(persist_directory=self.chroma_path, embedding_function=embeddings)
            llm = ChatOllama(model="qwen2.5:7b", temperature=0.1, num_ctx=2048, num_gpu=1)
            
            print("✅ Ассистент готов к работе!")
            print("💡 Задавайте вопросы на русском или английском")
            print("🚪 Для выхода введите 'exit' или 'выход'")
            print("-" * 50)
            
            while True:
                try:
                    question = input("\n🧑 Ваш вопрос: ").strip()
                    
                    if question.lower() in ['exit', 'quit', 'выход']:
                        print("👋 Возврат в главное меню...")
                        break
                        
                    if not question:
                        continue
                    
                    # Ищем релевантные документы
                    docs = vectorstore.similarity_search(question, k=3)
                    
                    if not docs:
                        print("🤷 Не найдено информации в документации.")
                        continue
                    
                    # Создаем контекст
                    context = "\n\n".join([doc.page_content for doc in docs])
                    
                    # Создаем промпт
                    prompt = f"""
                    Ты — AI-ассистент для инженеров мобильной связи. Отвечай на русском языке.
                    Используй ТОЛЬКО предоставленный контекст из документации Huawei.
                    
                    Контекст из документации:
                    {context}
                    
                    Вопрос: {question}
                    
                    Ответ (будь точным и используй только информацию из контекста):
                    """
                    
                    print("💭 Генерация ответа...")
                    response = llm.invoke(prompt)
                    print(f"\n🤖 Ответ: {response.content}")
                    
                except KeyboardInterrupt:
                    print("\n👋 Возврат в главное меню...")
                    break
                except Exception as e:
                    print(f"❌ Ошибка: {e}")
                    
        except Exception as e:
            print(f"❌ Ошибка запуска ассистента: {e}")
            input("Нажмите Enter для продолжения...")
    
    def show_system_info(self):
        """Показывает информацию о системе"""
        print("\n--- 📊 ИНФОРМАЦИЯ О СИСТЕМЕ ---")
        
        # Проверяем папку с документами
        pdf_files = glob.glob(os.path.join(self.data_path, "*.pdf"))
        print(f"📚 PDF-документов: {len(pdf_files)} файлов")
        
        # Проверяем базу данных
        if self.check_database_exists():
            try:
                embeddings = HuggingFaceEmbeddings(
                    model_name="sentence-transformers/all-MiniLM-L6-v2",
                    model_kwargs={'device': 'cpu'}
                )
                vectorstore = Chroma(persist_directory=self.chroma_path, embedding_function=embeddings)
                count = vectorstore._collection.count()
                print(f"✅ База знаний: загружена ({count} фрагментов)")
            except:
                print("❌ База знаний: ошибка доступа")
        else:
            print("❌ База знаний: не создана")
        
        # Проверяем Ollama
        self.check_ollama()
        
        input("\nНажмите Enter для продолжения...")
    
    def show_main_menu(self):
        """Показывает главное меню"""
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("\n" + "="*60)
            print("           🤖 AI-АССИСТЕНТ HUAWEI - ПОЛНАЯ ВЕРСИЯ")
            print("="*60)
            print(f"📁 Рабочая папка: {self.base_dir}")
            print("="*60)
            print("1. 📚 Создать/обновить базу знаний (из PDF в папке 'data')")
            print("2. 🗣️  Запустить AI-ассистента")
            print("3. 📊 Показать информацию о системе")
            print("4. 📖 Открыть инструкцию (README.txt)")
            print("5. 📁 Открыть папку с документами")
            print("6. 🚪 Выйти")
            print("="*60)
            
            choice = input("\nВыберите действие (1-6): ").strip()
            
            if choice == "1":
                self.create_database()
            elif choice == "2":
                self.run_assistant()
            elif choice == "3":
                self.show_system_info()
            elif choice == "4":
                self.open_readme()
            elif choice == "5":
                self.open_data_folder()
            elif choice == "6":
                print("👋 До свидания!")
                break
            else:
                print("❌ Неверный выбор. Попробуйте снова.")
                time.sleep(1)
    
    def open_readme(self):
        """Открывает файл с инструкцией"""
        try:
            if os.name == 'nt':  # Windows
                os.startfile(self.readme_path)
            else:  # Mac/Linux
                subprocess.run(['open', self.readme_path] if sys.platform == 'darwin' else ['xdg-open', self.readme_path])
            print("✅ Инструкция открыта")
        except Exception as e:
            print(f"❌ Не удалось открыть инструкцию: {e}")
        input("Нажмите Enter для продолжения...")
    
    def open_data_folder(self):
        """Открывает папку с документами"""
        try:
            if os.name == 'nt':  # Windows
                os.startfile(self.data_path)
            else:  # Mac/Linux
                subprocess.run(['open', self.data_path] if sys.platform == 'darwin' else ['xdg-open', self.data_path])
            print("✅ Папка с документами открыта")
        except Exception as e:
            print(f"❌ Не удалось открыть папку: {e}")
        input("Нажмите Enter для продолжения...")
    
    def run(self):
        """Основной метод запуска"""
        try:
            print("🚀 Инициализация AI-ассистента...")
            
            # Настраиваем окружение
            self.setup_environment()
            
            # Проверяем Ollama
            if not self.check_ollama():
                print("\n⚠️  ВНИМАНИЕ: Ollama не настроена корректно!")
                print("   Ассистент может работать некорректно")
                input("Нажмите Enter для продолжения...")
            
            # Запускаем главное меню
            self.show_main_menu()
            
        except Exception as e:
            print(f"❌ Критическая ошибка: {e}")
            input("Нажмите Enter для выхода...")

def main():
    """Точка входа программы"""
    # Устанавливаем кодировку для Windows
    if os.name == 'nt':
        os.system('chcp 65001 > nul')
    
    # Запускаем приложение
    app = AIAssistantComplete()
    app.run()

if __name__ == "__main__":
    main()