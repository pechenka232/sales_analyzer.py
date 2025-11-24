import pandas as pd  # для работы с таблицами
import numpy as np   # для генерации случайных данных
from sklearn.preprocessing import LabelEncoder, MinMaxScaler  # для кодирования и масштабирования
import matplotlib.pyplot as plt  # для визуализации

def generate_transactions(filename="transactions.csv", records=50):
    # создаём тестовый набор транзакций
    types = ["Покупка", "Перевод", "Снятие"]
    categories = ["Продукты", "Электроника", "Одежда", "Развлечения"]

    data = {
        "Тип операции": np.random.choice(types, records),
        "Категория": np.random.choice(categories, records),
        "Сумма": np.round(np.random.uniform(100, 5000, records), 2),
        "Количество": np.random.randint(1, 20, records)
    }

    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)  # сохраняем CSV
    print(f"CSV-файл '{filename}' с тестовыми транзакциями создан")

def encode_and_scale(filename="transactions.csv", output_file="transactions_processed.csv"):
    # загружаем данные
    df = pd.read_csv(filename)

    # кодируем категориальные признаки
    le_type = LabelEncoder()
    le_category = LabelEncoder()
    df["Тип операции"] = le_type.fit_transform(df["Тип операции"])
    df["Категория"] = le_category.fit_transform(df["Категория"])

    # сохраняем таблицу соответствий для категорий
    mapping = {
        "Тип операции": dict(zip(le_type.classes_, le_type.transform(le_type.classes_))),
        "Категория": dict(zip(le_category.classes_, le_category.transform(le_category.classes_)))
    }
    print("Таблица соответствий категорий:", mapping)

    # масштабируем числовые признаки
    scaler = MinMaxScaler()
    df[["Сумма", "Количество"]] = scaler.fit_transform(df[["Сумма", "Количество"]])

    # проверка пропусков
    if df.isnull().sum().sum() == 0:
        print("Пропусков в данных нет")  # хорошо
    else:
        print("Есть пропуски!")  # предупреждение

    # визуализация распределения после преобразования
    df[["Сумма", "Количество"]].hist(bins=10, figsize=(8,4))
    plt.tight_layout()
    plt.show()

    # сохраняем обработанный датасет
    df.to_csv(output_file, index=False)
    print(f"Обработанный датасет сохранён в '{output_file}'")
    return df

def main():
    generate_transactions()  # создаём тестовые данные
    df_processed = encode_and_scale()  # кодируем и масштабируем
    print("\nПример обработанных данных:")
    print(df_processed.head())  # выводим несколько строк

if __name__ == "__main__":
    main()  # запуск проекта
