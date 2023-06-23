# Balabin 2023

## Для запуска тестов
- Добавить переменные окружения в файл `.env`, см. `env.template`
- Установить зависимости `python -r requirements.txt`
- Загрузить нужную версию браузера с зависимостями, выполнив команду:
    ```
    playwright install --with-deps chromium
    ``` 
- Запустить тесты `pytest -s -v`
***
