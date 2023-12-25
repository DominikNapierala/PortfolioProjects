from tabulate import tabulate
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import csv
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def main():
    while True:
        try:
            menu()
            option = int(input("Option: "))
            if option in [1, 2, 3, 4, 5]:
                break
            else:
                print("Please choose an appropriate option")
        except ValueError:
            print("Please choose an appropriate option")
    if option == 1:
        add_item()
    elif option == 2:
        remove_item()
    elif option == 3:
        update_prices()
    elif option == 4:
        visualize_prices()
    elif option == 5:
        exit("See you later")

def menu():
    print(tabulate([
    ["Add Item", 1],
    ["Remove Item", 2],
    ["Update Prices", 3],
    ["Show Me Price Trend", 4],
    ["Exit", 5]
], headers = ["Press"], tablefmt = "fancy_grid"))

def scrape_me(i) -> list:
    try:
        web_page = requests.get(i)
        web_page.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

    try:
        soup = BeautifulSoup(web_page.content, 'html.parser')
        return [
            soup.find("h1").get_text(strip=True),
            soup.find("p", class_="price_color").get_text(strip=True).strip("£")
    ]
    except AttributeError:
        raise SystemExit("Invalid address. Please provide an item from this website: https://books.toscrape.com/index.html")

def add_item():
    link = input("Link to item: ")
    print("Adding Item")
    item_name = scrape_me(link)[0]
    item_price = scrape_me(link)[1]

    try:
        with open("item_info.csv", "r") as item_info:
            if item_name in item_info.read() or link in item_info.read():
                pass
            else:
                with open("item_info.csv", "a", encoding='utf-8', newline = '') as item_info:
                    writer = csv.writer(item_info, delimiter = '|')
                    writer.writerow([item_name, link])
    except FileNotFoundError:
        with open("item_info.csv", "a", encoding='utf-8', newline = '') as item_info:
            writer = csv.writer(item_info, delimiter = '|')
            writer.writerow(["item_name","link"])
            writer.writerow([item_name,link])
    with open("item_prices.csv", "a", encoding='utf-8', newline = '') as item_prices:
        writer = csv.writer(item_prices, delimiter = '|')
        if item_prices.tell() == 0:
            writer.writerow(["item_name","item_price","date"])
        writer.writerow([item_name, item_price, datetime.now().strftime("%d/%m/%Y %H:%M:%S")])

def update_prices():
    try:
        with open("item_info.csv", "r") as item_info:
            reader = csv.reader(item_info, delimiter = '|')
            next(reader)
            for name, link in reader:
                item_price = scrape_me(link)[1]
                with open("item_prices.csv", "a", encoding='utf-8', newline = '') as item_prices:
                    writer = csv.writer(item_prices, delimiter = '|')
                    writer.writerow([name, item_price, datetime.now().strftime("%d/%m/%Y %H:%M:%S")])
    except FileNotFoundError:
        raise SystemExit("Firstly add your items")
    print("Updating Prices")

def remove_item():
    table_of_items(item_list())
    try:
        choice = int(input("Which item would you like to remove? "))
        if choice < 1 or choice > len(item_list()):
            print("Wrong item")
        else:
            print("Removing Item")
            with open("item_info.csv", "r", encoding='utf-8', newline = '') as item_info, open("temp_item_info.csv", "w", encoding='utf-8', newline = '') as temp_item_info:
                reader = csv.reader(item_info, delimiter = '|')
                writer = csv.writer(temp_item_info, delimiter = '|')
                rows = []
                for row in reader:
                    if row[0] != item_list()[choice - 1]:
                        rows.append(row)
                writer.writerows(rows)
            with open("item_prices.csv", "r", encoding='utf-8', newline = '') as item_prices, open("temp_item_prices.csv", "w", encoding='utf-8', newline = '') as temp_item_prices:
                reader = csv.reader(item_prices, delimiter = '|')
                writer = csv.writer(temp_item_prices, delimiter = '|')
                rows = []
                for row in reader:
                    if row[0] != item_list()[choice - 1]:
                        rows.append(row)
                writer.writerows(rows)
            with open("temp_item_prices.csv", "r", encoding='utf-8', newline = '') as temp_item_prices:
                reader = csv.reader(temp_item_prices, delimiter = '|')
                rows = list(reader)
            if len(rows) == 1:
                os.remove("temp_item_prices.csv")
                os.remove("item_prices.csv")
                os.remove("temp_item_info.csv")
                os.remove("item_info.csv")
            else:
                os.replace("temp_item_prices.csv", "item_prices.csv")
                os.replace("temp_item_info.csv", "item_info.csv")
    except ValueError:
        raise SystemExit("Item doesn't exist")

def item_list():
    item_names = []
    try:
        with open("item_info.csv", "r", encoding='utf-8', newline = '') as item_info:
            reader = csv.reader(item_info, delimiter = '|')
            next(reader)
            for row in reader:
                item_names.append(row[0])
        return item_names
    except FileNotFoundError:
        raise SystemExit("Firstly add your items")

def table_of_items(i):
    print(tabulate([[item, index + 1] for index, item in enumerate(i)], headers = ["Press"], tablefmt = "fancy_grid"))

def visualize_prices():
    try:
        with open("item_prices.csv", "r", encoding='utf-8', newline = '') as item_prices, open("item_info.csv", "r", encoding='utf-8', newline = '') as item_info:
            reader_prices = list(csv.reader(item_prices, delimiter = '|'))
            reader_info = csv.reader(item_info, delimiter = '|')
            for item_name, link in reader_info:
                if item_name == 'item_name':
                    continue
                else:
                    prices = []
                    dates = []
                    for price_row, item_price, item_date in reader_prices:
                        if item_name == price_row:
                            prices.append(float(item_price))
                            dates.append(item_date)
                    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%d/%m/%Y %H:%M:%S"))
                    plt.gca().xaxis.set_major_locator(mdates.DayLocator())
                    dates = [datetime.strptime(date, '%d/%m/%Y %H:%M:%S') for date in dates]
                    plt.plot(dates, prices, marker='o', linestyle='-', label=item_name)
                    for i, j in zip(dates, prices):
                        plt.text(i, j, str(j), ha = 'center', va = 'bottom')
            for price_row, item_price, item_date in reader_prices:
                if item_date != 'date':
                    dates = []
                    dates.append(item_date)
                    dates = [datetime.strptime(date, '%d/%m/%Y %H:%M:%S') for date in dates]
                    plt.xticks(dates, rotation = 45)
            plt.xlabel('Date')
            plt.ylabel('Item Price')
            plt.title('Item Price Over Time')
            plt.legend()
            plt.show()
    except FileNotFoundError:
        raise SystemExit("Firstly add your items")

if __name__ == "__main__":
    main()
