import pandas as pd  # работа с таблицами
import numpy as np   # для генерации случайных данных
import matplotlib.pyplot as plt  # графики
import seaborn as sns  # красивые графики

def generate_incident_data(filename="cyber_incidents.csv", records=50):
    # создаём данные по кибер-инцидентам
    types = ["Вирус", "Фишинг", "DDoS", "Шпионское ПО"]  # типы атак
    severity = ["Низкий", "Средний", "Высокий"]  # уровни серьёзности

    # случайные записи
    data = {
        "Тип атаки": np.random.choice(types, records),
        "Уровень серьёзности": np.random.choice(severity, records),
        "Дата": pd.date_range(start="2024-01-01", periods=records)  # даты
    }

    df = pd.DataFrame(data)  # создаём таблицу
    df.to_csv(filename, index=False)  # сохраняем CSV
    print(f"CSV-файл '{filename}' с тестовыми инцидентами создан")  # сообщение

def load_and_prepare(filename="cyber_incidents.csv"):
    # загружаем CSV
    df = pd.read_csv(filename)

    # делаем категории для удобной работы
    df["Тип атаки"] = df["Тип атаки"].astype("category")
    df["Уровень серьёзности"] = df["Уровень серьёзности"].astype("category")

    # считаем процент по типам атак
    type_counts = df["Тип атаки"].value_counts(normalize=True) * 100
    type_counts = type_counts.round(2)  # округляем

    return df, type_counts  # возвращаем таблицу и проценты

def visualize_incidents(df, type_counts):
    # стиль seaborn чтобы красиво
    sns.set(style="whitegrid")

    # круговая диаграмма по типам
    plt.figure(figsize=(6,6))
    plt.pie(type_counts, labels=type_counts.index, autopct="%1.1f%%", colors=sns.color_palette("Set2"))
    plt.title("Распределение типов кибер-атак")
    plt.tight_layout()
    plt.savefig("types_pie.png", dpi=150)  # сохраняем
    plt.show()  # показываем

    # столбчатая диаграмма по уровням серьёзности
    plt.figure(figsize=(8,5))
    sns.countplot(x="Уровень серьёзности", data=df, palette="Set1", order=["Низкий","Средний","Высокий"])
    plt.title("Количество инцидентов по уровням серьёзности")
    plt.ylabel("Количество")
    plt.xlabel("Уровень серьёзности")
    plt.tight_layout()
    plt.savefig("severity_bar.png", dpi=150)  # сохраняем график
    plt.show()

def create_summary_table(df):
    # создаём сводную таблицу по типам и уровням
    pivot = pd.pivot_table(df, index="Тип атаки", columns="Уровень серьёзности", aggfunc="size", fill_value=0)
    pivot["Всего"] = pivot.sum(axis=1)  # всего по строкам
    pivot.loc["Итого"] = pivot.sum()    # всего по всем

    pivot.to_csv("summary_table.csv")  # сохраняем CSV
    print("Сводная таблица сохранена в 'summary_table.csv'")
    return pivot  # возвращаем таблицу

def main():
    generate_incident_data()  # создаём тестовые данные
    df, type_counts = load_and_prepare()  # загружаем и считаем проценты
    visualize_incidents(df, type_counts)  # строим графики
    summary = create_summary_table(df)  # создаём таблицу
    print("\nПример сводной таблицы:")
    print(summary)  # выводим пример

if __name__ == "__main__":
    main()  # запускаем проект
