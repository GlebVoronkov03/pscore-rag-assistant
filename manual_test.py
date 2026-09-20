# manual_test.py
import os
import sys
sys.path.insert(0, 'src')

def test_assistant_manually():
    """Ручное тестирование ассистента"""
    print("🔍 РУЧНОЕ ТЕСТИРОВАНИЕ")
    
    try:
        from ai_assistant_complete import AIAssistantComplete
        
        # Создаем ассистента
        assistant = AIAssistantComplete()
        
        # Тест 1: Настройка окружения
        print("1. Тестируем настройку окружения...")
        assistant.setup_environment()
        
        # Тест 2: Проверка Ollama
        print("2. Проверяем Ollama...")
        if assistant.check_ollama():
            print("   ✅ Ollama работает")
        else:
            print("   ⚠️  Ollama не настроена (но это нормально для теста)")
        
        # Тест 3: Проверка базы данных
        print("3. Проверяем базу данных...")
        if assistant.check_database_exists():
            print("   ✅ База данных существует")
        else:
            print("   ℹ️  База данных не создана (создадим позже)")
        
        # Тест 4: Создание базы знаний
        print("4. Тестируем создание базы знаний...")
        if assistant.create_database():
            print("   ✅ База знаний создана успешно")
        else:
            print("   ❌ Ошибка создания базы знаний")
        
        print("\n🎉 Ручное тестирование завершено!")
        
    except Exception as e:
        print(f"❌ Ошибка при ручном тестировании: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_assistant_manually()
    input("Нажмите Enter для выхода...")