# build_simple.py
import os
import sys
import subprocess
import shutil

def run_command(cmd, description):
    """Выполняет команду и выводит результат"""
    print(f"▶ {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True, encoding='utf-8')
        print("  ✅ Успешно")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  ❌ Ошибка: {e}")
        print(f"  Вывод: {e.stdout}")
        print(f"  Ошибка: {e.stderr}")
        return False

def main():
    print("=" * 60)
    print("           СБОРКА AI-АССИСТЕНТА HUAWEI")
    print("=" * 60)
    
    # Проверяем PyInstaller
    try:
        import PyInstaller
        print("✅ PyInstaller доступен")
    except ImportError:
        print("❌ PyInstaller не установлен. Устанавливаем...")
        run_command(f'"{sys.executable}" -m pip install pyinstaller', "Установка PyInstaller")
    
    # Создаем команду для сборки с ВСЕМИ необходимыми импортами
    hidden_imports = [
        'langchain', 'langchain_community', 'langchain_core', 'langchain_text_splitters',
        'chromadb', 'chromadb.db', 'chromadb.api', 'chromadb.config', 'chromadb.telemetry',
        'chromadb.db.impl.sqlite', 'chromadb.db.impl.grpc', 'chromadb.db.base',
        'sentence_transformers', 'sentence_transformers.models', 'sentence_transformers.util',
        'pypdf', 'pypdf._utils', 'pypdf.generic', 'pypdf.pagerange',
        'tiktoken', 'torch', 'numpy', 'transformers',
        'langchain_community.document_loaders', 'langchain_community.vectorstores',
        'langchain_community.embeddings', 'langchain_community.chat_models',
        'langchain_community.llms', 'langchain_community.retrievers',
        'huggingface_hub', 'tokenizers', 'requests', 'urllib3', 'charset_normalizer',
        'filelock', 'packaging', 'yaml'
    ]
    
    # Формируем команду
    cmd_parts = [
        'pyinstaller',
        '--onefile',
        '--console',
        '--name', '"AI_Assistant_Huawei"',
        '--add-data', '"src;src"',
        '--add-data', '"data;data"',
    ]
    
    # Добавляем все скрытые импорты
    for imp in hidden_imports:
        cmd_parts.extend(['--hidden-import', f'"{imp}"'])
    
    # Добавляем collect-all для основных пакетов
    cmd_parts.extend([
        '--collect-all', '"langchain"',
        '--collect-all', '"langchain_community"',
        '--collect-all', '"chromadb"',
        '--collect-all', '"sentence_transformers"',
        'src/ai_assistant_complete.py'
    ])
    
    command = ' '.join(cmd_parts)
    
    print("\n🚀 Запуск сборки...")
    print(f"Команда: {command[:200]}...")  # Показываем только начало команды
    
    success = run_command(command, "Сборка основной программы")
    
    if success:
        print("\n" + "=" * 60)
        print("✅ СБОРКА ЗАВЕРШЕНА УСПЕШНО!")
        print("=" * 60)
        
        # Проверяем результат
        exe_path = "dist/AI_Assistant_Huawei.exe"
        if os.path.exists(exe_path):
            size = os.path.getsize(exe_path)
            print(f"📦 Файл: {exe_path}")
            print(f"📊 Размер: {size:,} байт ({size/1024/1024:.1f} МБ)")
            
            print("\n🎯 ИНСТРУКЦИЯ ПО ТЕСТИРОВАНИЮ:")
            print("1. Создайте новую папку")
            print("2. Скопируйте туда AI_Assistant_Huawei.exe")
            print("3. Запустите EXE файл")
            print("4. Убедитесь, что создаются папки data и chroma_db")
            print("5. Добавьте PDF файлы в папку data")
            print("6. Протестируйте создание базы знаний")
        else:
            print("❌ EXE файл не найден!")
    else:
        print("\n❌ Сборка не удалась!")
        print("Попробуйте альтернативный метод...")
        
        # Альтернативная команда
        alt_command = (
            'pyinstaller --onedir --console '
            '--name "AI_Assistant_Huawei" '
            '--add-data "src;src" '
            '--hidden-import=langchain_community '
            '--hidden-import=chromadb '
            '--hidden-import=sentence_transformers '
            '--collect-all=langchain_community '
            'src/ai_assistant_complete.py'
        )
        run_command(alt_command, "Альтернативная сборка")
    
    input("\nНажмите Enter для выхода...")

if __name__ == "__main__":
    main()