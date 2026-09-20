@echo off
chcp 65001
echo ========================================
echo    🚀 СБОРКА AI-АССИСТЕНТА HUAWEI
echo ========================================
echo.

echo 📦 Проверка окружения...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python не найден! Убедитесь, что Python установлен и добавлен в PATH
    pause
    exit /b 1
)

echo 🔧 Установка PyInstaller...
pip install pyinstaller

echo 🛠️  Сборка основной программы...
pyinstaller --onefile --console ^
  --name "AI_Assistant_Huawei" ^
  --hidden-import=langchain ^
  --hidden-import=langchain_community ^
  --hidden-import=langchain_core ^
  --hidden-import=chromadb ^
  --hidden-import=sentence_transformers ^
  --hidden-import=pypdf ^
  --hidden-import=tiktoken ^
  --hidden-import=torch ^
  --hidden-import=numpy ^
  --hidden-import=transformers ^
  --hidden-import=langchain_community.document_loaders ^
  --hidden-import=langchain_community.vectorstores ^
  --hidden-import=langchain_community.embeddings ^
  --hidden-import=langchain_community.chat_models ^
  --collect-all=langchain ^
  --collect-all=langchain_community ^
  --collect-all=chromadb ^
  src/ai_assistant_complete.py

if errorlevel 1 (
    echo ❌ Ошибка сборки основной программы!
    echo 🔧 Пробуем альтернативный метод...
    
    pyinstaller --onedir --console ^
      --name "AI_Assistant_Huawei" ^
      --hidden-import=langchain_community ^
      --hidden-import=chromadb ^
      --hidden-import=sentence_transformers ^
      src/ai_assistant_complete.py
)

echo.
echo 📦 Сборка утилиты управления базой данных...
pyinstaller --onefile --console ^
  --name "Manage_Database" ^
  --hidden-import=langchain_community ^
  --hidden-import=chromadb ^
  --hidden-import=sentence_transformers ^
  --hidden-import=pypdf ^
  src/manage_database.py

echo.
echo ========================================
echo 📊 РЕЗУЛЬТАТЫ СБОРКИ:
echo ========================================

if exist "dist\AI_Assistant_Huawei.exe" (
    echo ✅ Основная программа: dist\AI_Assistant_Huawei.exe
    for %%I in ("dist\AI_Assistant_Huawei.exe") do echo    Размер: %%~zI байт
) else (
    echo ❌ Основная программа не собрана
)

if exist "dist\Manage_Database.exe" (
    echo ✅ Утилита управления: dist\Manage_Database.exe
    for %%I in ("dist\Manage_Database.exe") do echo    Размер: %%~zI байт
) else (
    echo ❌ Утилита управления не собрана
)

echo.
echo 🎯 ИНСТРУКЦИЯ ПО РАСПРОСТРАНЕНИЮ:
echo.
echo 1. Создайте папку для распространения
echo 2. Скопируйте в нее:
echo    - AI_Assistant_Huawei.exe
echo    - Manage_Database.exe (опционально)
echo 3. Запустите AI_Assistant_Huawei.exe
echo 4. Программа автоматически создаст папки data и chroma_db
echo 5. Добавьте PDF-файлы в папку data
echo 6. Используйте программу для создания базы знаний и работы
echo.
echo ⚠️  ПРИМЕЧАНИЕ: Пользователям нужно установить Ollama и модель qwen2.5:7b
echo.

pause