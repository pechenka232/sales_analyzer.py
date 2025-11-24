import pandas as pd       # Импортируем библиотеку для работы с таблицами CSV и обработки данных
import numpy as np        # Импортируем библиотеку для генерации чисел и массивов
import json               # Импортируем библиотеку для сохранения данных в JSON
import matplotlib.pyplot as plt  # Импортируем библиотеку для визуализации графиков




def generate_csv(filename="sales.csv"):
    # Создаем диапазон дат (50 дней с 01.01.2024)
    dates = pd.date_range(start="2024-01-01", periods=50)
    
    # Список товаров
    products = ["Телефон", "Ноутбук", "Планшет", "Наушники"]

    # Генерируем данные: случайно выбираем даты и товары, количество и цену
    data = {
        "Дата": np.random.choice(dates, 50),                     # случайная дата из списка
        "Товар": np.random.choice(products, 50),                # случайный товар
        "Количество": np.random.randint(1, 10, 50),             # случайное количество от 1 до 9
        "Цена": np.round(np.random.uniform(5000, 150000, 50), 2) # случайная цена от 5000 до 150000, округляем до 2 знаков
    }

    # Превращаем данные в DataFrame (табличная структура Pandas)
    df = pd.DataFrame(data)
    
    # Сохраняем DataFrame в CSV-файл без индексов
    df.to_csv(filename, index=False)
    
    # Сообщение о создании файла
    print(f"CSV-файл '{filename}' успешно создан.")


#Обработка csv
def load_and_process(filename="sales.csv"):
    # Загружаем CSV-файл в DataFrame
    df = pd.read_csv(filename)
    
    # Преобразуем колонку "Дата" в тип datetime, ошибки превращаем в NaT
    df["Дата"] = pd.to_datetime(df["Дата"], errors="coerce")
    
    # Преобразуем колонку "Количество" в числовой тип
    df["Количество"] = pd.to_numeric(df["Количество"], errors="coerce")
    
    # Преобразуем колонку "Цена" в числовой тип
    df["Цена"] = pd.to_numeric(df["Цена"], errors="coerce")
    
    # Удаляем строки, где отсутствуют данные в колонках "Количество" или "Цена"
    df = df.dropna(subset=["Количество", "Цена"])
    
    # Возвращаем обработанный DataFrame
    return df



# Функция расчета статистики
def calculate_stats(df):
    # Создаем новую колонку "Выручка" = Количество * Цена, округляем до 2 знаков
    df["Выручка"] = (df["Количество"] * df["Цена"]).round(2)
    
    # Суммируем все значения выручки для общей суммы
    total_revenue = round(df["Выручка"].sum(), 2)
    
    # Вычисляем среднюю цену товаров
    avg_price = round(df["Цена"].mean(), 2)
    
    # Возвращаем общую выручку и среднюю цену
    return total_revenue, avg_price



# Функция сохранения статистики в JSON

def save_stats_to_json(total_revenue, avg_price, filename="stats.json"):
    # Формируем словарь со статистикой
    stats = {
        "total_revenue": total_revenue,
        "average_price": avg_price
    }
    
    # Открываем файл на запись в кодировке utf-8
    with open(filename, "w", encoding="utf-8") as f:
        # Сохраняем словарь в JSON с отступами
        json.dump(stats, f, indent=4, ensure_ascii=False)
    
    # Сообщение о сохранении файла
    print(f"JSON-файл '{filename}' успешно сохранён.")





def plot_revenue(df, avg_price):
    # Группируем данные по товарам и суммируем выручку, затем сортируем
    revenue_per_product = df.groupby("Товар")["Выручка"].sum().sort_values()
    
    # Создаем фигуру и задаем размер
    plt.figure(figsize=(8,6))
    
    # Рисуем столбчатую диаграмму
    bars = plt.bar(revenue_per_product.index, revenue_per_product.values, color='skyblue')
    
    # Добавляем горизонтальную линию средней цены * 5 (для наглядности)
    plt.axhline(y=avg_price*5, color='red', linestyle='--', label=f"Средняя цена * 5 = {avg_price*5:.2f}")
    
    # Добавляем подписи на каждом столбце
    for bar in bars:
        yval = bar.get_height()  # высота столбца
        plt.text(bar.get_x() + bar.get_width()/2, yval + 1000, f'{yval:.0f}', ha='center', va='bottom')
    
    # Подписи и заголовок графика
    plt.title("Выручка по товарам")
    plt.ylabel("Выручка")
    plt.xlabel("Товар")
    plt.legend()
    plt.tight_layout()  # чтобы элементы не обрезались
    plt.show()         # показать график



def main():
    generate_csv()                      # Генерация CSV-файла
    df = load_and_process()              # Загрузка и обработка данных
    total_revenue, avg_price = calculate_stats(df)  # Расчет статистики
    save_stats_to_json(total_revenue, avg_price)    # Сохранение статистики в JSON
    
    # Вывод результатов в консоль
    print("\nГотово!")
    print(f"Общая выручка: {total_revenue}")
    print(f"Средняя цена: {avg_price}")
    
    plot_revenue(df, avg_price)          # Визуализация данных



if __name__ == "__main__":
    main()  # Старт 
