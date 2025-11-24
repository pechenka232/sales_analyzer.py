import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


def generate_crypto_data(filename="bitcoin_prices.json", days=50):

    base_price = 30000  # стартовая цена BTC
    dates = [datetime.today() - timedelta(days=x) for x in range(days)][::-1]  # список дат от старой к новой

    # Генерация цен с трендом и случайной волатильностью
    prices = []
    price = base_price
    for _ in range(days):
        change = np.random.normal(loc=0.001, scale=0.02)  # небольшой тренд + шум
        price = max(0, price * (1 + change))  # цена не может быть отрицательной
        prices.append(round(price, 2))

    # Формируем список словарей для JSON
    data = [{"Дата": d.strftime("%Y-%m-%d"), "Цена": p} for d, p in zip(dates, prices)]

    # Сохраняем в JSON
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"JSON-файл '{filename}' с историей цен создан.")



#Загрузка и обработка данных

def load_and_process(filename="bitcoin_prices.json"):

    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Превращаем в DataFrame
    df = pd.DataFrame(data)

    #Преобразуем даты в datetime
    df["Дата"] = pd.to_datetime(df["Дата"], errors="coerce")

    #преобразуем цену в число
    df["Цена"] = pd.to_numeric(df["Цена"], errors="coerce")

    # Вычисляем скользящее среднее за 5 дней
    df["Скользящее_среднее"] = df["Цена"].rolling(window=5, min_periods=1).mean().round(2)

    #Средняя цена по всему периоду
    avg_price = round(df["Цена"].mean(), 2)

    return df, avg_price


#визyализация
def plot_crypto(df, avg_price, output_file="bitcoin_plot.png"):

    plt.figure(figsize=(10, 6))
    plt.plot(df["Дата"], df["Цена"], label="Цена BTC", color="blue", linewidth=2)
    plt.plot(df["Дата"], df["Скользящее_среднее"], label="Скользящее среднее", color="orange", linestyle="--")
    plt.axhline(y=avg_price, color="red", linestyle=":", label=f"Средняя цена = {avg_price}")

    # Подписи и оформление
    plt.title("Динамика цен Bitcoin")
    plt.xlabel("Дата")
    plt.ylabel("Цена (USD)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    # Сохраняем график
    plt.savefig(output_file, dpi=150)
    plt.show()
    print(f"График сохранён в '{output_file}'.")



def main():
    generate_crypto_data()                 #Генерация JSON с тестовыми данными
    df, avg_price = load_and_process()     # Загрузка и обработка данных
    plot_crypto(df, avg_price)             #визуализация и сохранение графика


if __name__ == "__main__":
    main()
