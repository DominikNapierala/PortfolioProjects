# Price Tracker and Visualizer for Online Items
### Description:
The **Price Tracker and Visualizer for Online Items** tool was designed to help track prices of items found online. The program allows the user to add an item through user provided link, remove an item, update prices of all previously added items and visualize the trend of item prices. By storing item prices we can make better shopping decisions, find best deals and identify price trends.
### User guide:
Since most e-commerce retailing websites do not allow web scraping, this program was built to use alongside a dummy web scraping friendly website- "Books To Scrape" (url: https://books.toscrape.com/index.html). **This program was designed to work only when provided links from this web scraping friendly website.** The creator of this program does not encourage any action that's against any online retailer's terms of service.

Before using the program, you have to install several non-standard python libraries. Before running the program, please type in your console and execute each of these lines one by one:
1. pip install tabulate
2. pip install requests
3. pip install bs4
4. pip install matplotlib
### Program structure
The core functionality is organized within the main() function, which serves as the program's entry point. It utilizes a while loop to repeatedly display a menu of options until a valid choice is made by the user. This function ensures that if user's choice is outside of possible options (1, 2, 3, 4, 5), the user will be prompted with a correcting message: "Please choose an appropriate option". The chosen option then directs the program to specific tasks such as:
1. adding an item
2. removing an item
3. updating prices
4. visualizing price trends
5. exiting the program
There are four helper functions that perform specific subtasks:
1. menu()- The purpose of this function is to display an easy to read, user friendly menu of available options. It became feasible through the use of the `tabulate` python module.
2. scrape_me(i)- The purpose of this function is to scrape crucial information from a provided link to a correct webpage. This function accepts one parameter: `i` (webpage link), and returns a list of two values: product name and product price. The function uses two non-standard python libraries: `requests` and `BeautifulSoup`. `requests` library fetches web page content and `BeautifulSoup` extracts relevant information: item name and item price. This function uses two try-except blocks that ensure the user provides an appropriate link. If the user provides a link without the `http://` or `https://` scheme, such as "test.com", he will receive an error message: "Invalid URL 'test.com': No scheme supplied. Perhaps you meant \https://test.com?" and the program will exit through `SystemExit`. If the user provides a link with appropriate scheme but the function is unable to find html tags with item name and item price, he will receive an error message: "Invalid address. Please provide an item from this website: \https://books.toscrape.com/index.html".
3. item_list()- The purpose of this function is to return a list of item names of all previously added items. This function uses the `csv` python standard module to create a reader object and retrieve all item names from the `item_info.csv` file. It then appends all these names to a list and returns it. Through the usage of a try-except block, this function catches the `FileNotFoundError` and prints a message if the `item_info.csv` file doesn't exist: "Firstly add your items".
4. table_of_items(i)- This function accepts one parameter: `i`. Through the usage of the `tabulate` python library, it prints a menu with a header row and as many rows as `i` represents. The table is split in two columns: one for `i` and one for indices.
The term "helper" emphasizes that these functions play a supportive role in the overall functionality of the program, helping to modularize and organize code.
#### Adding Items
The action of adding an item is performed by the `add_item()` function.
This function is invoked when the user enters '1' in the console after being prompted by the menu.
The function asks the user for an input- a URL. It then passes the user provided URL to the `scrape_me()` function and creates two objects: `item_name` and `item_price`. Once these objects are created, the function executes a try-except block, trying to open the `item_info.csv` file.
* If the file doesn't exist, the function catches it throught the `FileNotFound` error and creates the file with a header row and writes a row with `item_name` and `link`, separated by the pipe delimiter ('|'). 
* If the file exists, the function opens the file and checks if `item_name` already exists inside the file.
	* If it does- the function executes the `pass` statement.
	* If it doesn't- the function writes a row with just `item_name` and `link`, without the header row.
The function then opens or creates the `item_prices.csv` file.
* If the file exists but is empty, the function writes a header row and a row with `item_name`, `item_price` and `date`, separated by the pipe delimiter.
* If the file isn't empty, the function writes a row with `item_name`, `item_price`, `date`, separated by the pipe delimiter.

`item_info.csv`- the purpose of this file is to store **distinct** names of items and links to these items. That's why the `add_item()` function checks if `item_name` already exists in the `item_info.csv` file- not to add duplicates.
`item_prices.csv`- the purpose of this file is to store names and prices of items and the date when the item was added to the file. This file accepts multiple entries of a single item because the user might want to add the price of an item on another date, instead of updating prices of all items stored in the `item_info.csv` file through the usage of the `Update Prices` option from the menu.
#### Removing Items
The action of removing an item is performed by the `remove_item()` function.
This function is invoked when the user enters '2' in the console after being prompted by the menu.
This function, through the usage of the `table_of_items()` and the `item_list()` function, prints the menu of all available items found in the `item_info.csv` file and asks the user for an input: "Which item would you like to remove?". Through the usage of a try-except block, the function ensures the user provides an appropriate index. The function then creates temporary files: `temp_item_info.csv` and `temp_item_prices.csv` **without** the item specified by the user. After this step, during code executement, there are two options:
1. The `temp_item_prices.csv` file consists of only one row- the header row. In this case the program removes all fours files (`itemp_item_prices.csv`, `item_prices.csv`, `temp_item_info.csv`, `item_info.csv`), through the usage of the `os` python module, because we do not want to store "empty" files (with header rows only).
2. The `temp_item_prices.csv` file consists of multiple rows- the header row plus one or more rows for items. In this case the program simultaneously replaces `item_prices.csv` with `temp_item_prices.csv` and `item_info.csv` with `temp_item_info.csv`, changing file names back to `item_info.csv` and `item_prices.csv`.
#### Updating Prices
The action of updating item prices is performed by the `update_prices()` function.
This function reads the `item_info.csv` file through the usage of the `csv` module's reader object, skips the header row and performs a 'for' loop for each item in the file. Inside the loop, the function calls the `scrape_me()` function while passing item's `link` to it during each iteration. Still inside the loop, the function opens the `item_prices.csv` file in append mode and writes a row with item name, current item price and current date. All of this happens inside of a try-except block that catches the `FileNotFoundError` and raises `SystemExit` with a message "Firstly add your items" if the file doesn't exst.
#### Visualizing price trends
The action of visualizing price trends is performed by the `visualize_prices()` function.
This function's purpose is to read both `item_prices.csv` and `item_info.csv` files and, through the usage of the `matplotlib` python non-standard library, visualize a line chart with dates on x-axis, item price on y-axis and separate line marks for all items in the files.
This function performs a loop for each item found in the `item_info.csv` file. The loop skips the header row, creates 'prices' and 'dates' lists for each item and appends the prices and dates from the `item_prices.csv` file to these lists. Still inside the loop, the function calls the `plot()` function from the `matplotlib` library and plots values from the 'dates' list for x axis and values from the 'prices' list for y axis. The function also performs several less important operations, such as adding price as text above each mark on the graph or formatting labels.
![ProjectGraph](https://github.com/DominikNapierala/PortfolioProjects/assets/112898686/06d5c12c-f546-4ccd-9927-faffffa00566)
