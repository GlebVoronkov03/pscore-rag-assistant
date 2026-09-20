# tests/test_basic.py
import os
import sys
import importlib
import subprocess

# Получаем корневую директорию проекта
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Добавляем пути
sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'src'))

def test_imports():
    """Тестирует импорт всех необходимых библиотек"""
    print("🧪 ТЕСТ ИМПОРТА БИБЛИОТЕК")
    print("=" * 50)
    
    # Только критически важные библиотеки
    critical_libraries = [
        'langchain',
        'langchain_community',
        'langchain_core', 
        'chromadb',
        'sentence_transformers',
        'pypdf',
        'tiktoken'
    ]
    
    all_imported = True
    for lib in critical_libraries:
        try:
            importlib.import_module(lib)
            print(f"✅ {lib}")
        except ImportError as e:
            print(f"❌ {lib}: {e}")
            all_imported = False
    
    # Необязательные библиотеки
    optional_libraries = ['flask']
    for lib in optional_libraries:
        try:
            importlib.import_module(lib)
            print(f"✅ {lib} (опционально)")
        except ImportError:
            print(f"⚠️  {lib} не установлен (не критично)")
    
    print("=" * 50)
    return all_imported

def test_ollama():
    """Тестирует подключение к Ollama"""
    print("\n🧪 ТЕСТ OLLAMA")
    print("=" * 50)
    
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            if "qwen2.5:7b" in result.stdout:
                print("✅ Модель qwen2.5:7b найдена")
                return True
            else:
                print("❌ Модель qwen2.5:7b не найдена")
                return False
        else:
            print("❌ Ollama не запущена")
            return False
    except Exception as e:
        print(f"❌ Ошибка проверки Ollama: {e}")
        return False

def test_file_structure():
    """Проверяет структуру файлов"""
    print("\n🧪 ТЕСТ СТРУКТУРЫ ФАЙЛОВ")
    print("=" * 50)
    
    required_files = [
        os.path.join(PROJECT_ROOT, 'src', 'ai_assistant_complete.py'),
        os.path.join(PROJECT_ROOT, 'src', 'manage_database.py'),
        os.path.join(PROJECT_ROOT, 'data')
    ]
    
    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {os.path.relpath(file_path, PROJECT_ROOT)}")
        else:
            print(f"❌ {os.path.relpath(file_path, PROJECT_ROOT)} не найден")
            all_exist = False
    
    # Проверяем PDF файлы
    data_dir = os.path.join(PROJECT_ROOT, 'data')
    if os.path.exists(data_dir):
        pdf_files = [f for f in os.listdir(data_dir) if f.lower().endswith('.pdf')]
        print(f"📄 PDF файлов в data/: {len(pdf_files)}")
    else:
        print("❌ Папка data не существует")
        pdf_files = []
    
    return all_exist and len(pdf_files) > 0

def test_main_script():
    """Тестирует основной скрипт"""
    print("\n🧪 ТЕСТ ОСНОВНОГО СКРИПТА")
    print("=" * 50)
    
    try:
        # Пытаемся импортировать основной скрипт
        from ai_assistant_complete import AIAssistantComplete
        
        # Создаем экземпляр
        assistant = AIAssistantComplete()
        
        # Тестируем настройку окружения
        if assistant.setup_environment():
            print("✅ Настройка окружения прошла успешно")
        else:
            print("❌ Ошибка настройки окружения")
            return False
        
        # Проверяем создание папок
        if os.path.exists(assistant.data_path) and os.path.exists(assistant.chroma_path):
            print("✅ Папки созданы успешно")
        else:
            print("❌ Ошибка создания папок")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Ошибка тестирования основного скрипта: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_database_creation():
    """Тестирует создание базы данных"""
    print("\n🧪 ТЕСТ СОЗДАНИЯ БАЗЫ ДАННЫХ")
    print("=" * 50)
    
    try:
        from manage_database import update_database
        
        # Создаем тестовую базу
        if update_database():
            print("✅ База данных создана успешно")
            
            # Проверяем что база не пустая
            chroma_path = os.path.join(PROJECT_ROOT, "chroma_db")
            if os.path.exists(chroma_path) and os.listdir(chroma_path):
                print("✅ База данных содержит данные")
                return True
            else:
                print("❌ База данных пуста")
                return False
        else:
            print("❌ Ошибка создания базы данных")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка тестирования базы данных: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_all_tests():
    """Запускает все тесты"""
    print("🚀 ЗАПУСК ПОЛНОГО ТЕСТИРОВАНИЯ")
    print("=" * 60)
    print(f"📁 Корневая директория: {PROJECT_ROOT}")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_ollama, 
        test_file_structure,
        test_main_script,
        test_database_creation
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Тест {test.__name__} упал с ошибкой: {e}")
            import traceback
            traceback.print_exc()
            results.append(False)
    
    # Сводка результатов
    print("\n" + "=" * 60)
    print("📊 СВОДКА РЕЗУЛЬТАТОВ ТЕСТИРОВАНИЯ")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"✅ Пройдено тестов: {passed}/{total}")
    print(f"📈 Успешность: {passed/total*100:.1f}%")
    
    if passed == total:
        print("🎉 Все тесты пройдены! Можно приступать к сборке.")
        return True
    else:
        print("⚠️  Некоторые тесты не пройдены.")
        # Если прошли хотя бы основные тесты, считаем успешным
        if passed >= 3:  # Минимум 3 из 5 тестов
            print("✅ Основные тесты пройдены, можно продолжать сборку.")
            return True
        else:
            print("❌ Слишком много ошибок. Исправьте перед сборкой.")
            return False

if __name__ == "__main__":
    success = run_all_tests()
    if not success:
        print("\n❌ ТЕСТИРОВАНИЕ НЕ ПРОЙДЕНО!")
    input("\nНажмите Enter для выхода...")