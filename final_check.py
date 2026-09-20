# final_check.py
import os
import sys

def check_ready_for_build():
    """Финальная проверка перед сборкой"""
    print("🔍 ФИНАЛЬНАЯ ПРОВЕРКА ПЕРЕД СБОРКОЙ")
    print("=" * 60)
    
    checks = []
    
    # Проверка 1: Основные файлы
    required_files = [
        'src/ai_assistant_complete.py',
        'src/manage_database.py', 
        'tests/test_basic.py',
        'build_fixed.py',
        'build_complete_fixed.bat'
    ]
    
    print("📁 Проверка файлов...")
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"  ✅ {file_path}")
            checks.append(True)
        else:
            print(f"  ❌ {file_path} - ОТСУТСТВУЕТ!")
            checks.append(False)
    
    # Проверка 2: Данные
    print("\n📊 Проверка данных...")
    if os.path.exists('data'):
        pdf_files = [f for f in os.listdir('data') if f.lower().endswith('.pdf')]
        print(f"  ✅ Папка data существует, PDF файлов: {len(pdf_files)}")
        checks.append(True)
    else:
        print("  ❌ Папка data отсутствует!")
        checks.append(False)
    
    # Проверка 3: База данных (опционально)
    print("\n💾 Проверка базы данных...")
    if os.path.exists('chroma_db') and os.listdir('chroma_db'):
        print("  ✅ База данных существует и не пуста")
    else:
        print("  ⚠️  База данных отсутствует или пуста (будет создана)")
    
    # Проверка 4: Импорты
    print("\n🐍 Проверка основных импортов...")
    try:
        from src.ai_assistant_complete import AIAssistantComplete
        print("  ✅ ai_assistant_complete.py импортируется")
        checks.append(True)
    except Exception as e:
        print(f"  ❌ Ошибка импорта: {e}")
        checks.append(False)
    
    try:
        from src.manage_database import update_database
        print("  ✅ manage_database.py импортируется")
        checks.append(True)
    except Exception as e:
        print(f"  ❌ Ошибка импорта: {e}")
        checks.append(False)
    
    # Итог
    print("\n" + "=" * 60)
    print("📊 РЕЗУЛЬТАТ ПРОВЕРКИ:")
    
    passed = sum(checks)
    total = len(checks)
    
    print(f"✅ Пройдено проверок: {passed}/{total}")
    
    if passed == total:
        print("🎉 ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ! МОЖНО ПРИСТУПАТЬ К СБОРКЕ!")
        return True
    else:
        print("❌ Есть проблемы. Исправьте перед сборкой.")
        return False

if __name__ == "__main__":
    if check_ready_for_build():
        print("\n🎯 Дальнейшие действия:")
        print("1. Запустите: build_complete_fixed.bat")
        print("2. EXE файл будет в папке dist/")
        print("3. Протестируйте EXE в чистой папке")
    else:
        print("\n⚠️  Исправьте отмеченные проблемы перед сборкой.")
    
    input("\nНажмите Enter для выхода...")