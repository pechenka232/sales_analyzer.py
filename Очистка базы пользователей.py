import pandas as pd           #Работа с таблицами Excel и CSV
import numpy as np            #Генерация тестовых данных
from openpyxl import Workbook #Работа с Excel
import json                   # Если нужно сохранить промежуточную статистику


#Генерация тестовых данных

def generate_user_data(filename="users.xlsx"):
    # Имена и фамилии
    first_names = ["Иван", "Мария", "Пётр", "Елена", "Алексей"]
    last_names = ["Иванов", "Петрова", "Сидоров", "Кузнецова", "Смирнов"]

    # Генерация 20 записей
    data = {
        "Имя": np.random.choice(first_names, 20),
        "Фамилия": np.random.choice(last_names, 20),
        "Email": [f"user{i}@example.com" for i in range(15)] + [f"user{i}@example.com" for i in range(5)], #дубликаты
        "Возраст": np.random.randint(18, 60, 20)
    }

    #Добавляем пропуски случайно
    for col in ["Имя", "Фамилия", "Email", "Возраст"]:
        for _ in range(2):  # 2пропуска на колонку
            idx = np.random.randint(0, 20)
            data[col][idx] = np.nan

    # Создаём DataFrame
    df = pd.DataFrame(data)

    # Сохраняем в Excel
    df.to_excel(filename, index=False)
    print(f"Excel-файл '{filename}' с тестовыми данными создан.")



def load_and_clean(filename="users.xlsx", output_filename="users_cleaned.xlsx"):
    #Загружаем Excel
    df = pd.read_excel(filename)

    # Удаляем дубликаты по Email
    df = df.drop_duplicates(subset=["Email"])

    #Заменяем пропуски на "N/A"
    df = df.fillna("N/A")

    # Маскировка email
    def mask_email(email):
        if email == "N/A":
            return email
        parts = email.split("@")
        local = parts[0]
        if len(local) > 1:
            masked_local = local[0] + "*" * (len(local) - 1)
        else:
            masked_local = "*"
        return masked_local + "@" + parts[1]

    df["Email"] = df["Email"].apply(mask_email)

    #Сохраняем очищенные данные в новый Excel
    df.to_excel(output_filename, index=False)
    print(f"Очищенные данные сохранены в '{output_filename}'.")

    return df


def main():
    generate_user_data()                  #Генерация тестовых данных
    df_cleaned = load_and_clean()         # Очистка и маскировка email

    # Вывод результатов для проверки
    print("\nПример очищенных данных:")
    print(df_cleaned.head())


if __name__ == "__main__":
    main()
