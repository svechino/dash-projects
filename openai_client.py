import openai
import os
from dotenv import load_dotenv

# Загружаем API-ключ из .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Получаем список доступных моделей (НОВЫЙ СПОСОБ)
models = openai.models.list()

# Выводим названия моделей
for model in models.data:
    print(model.id)
