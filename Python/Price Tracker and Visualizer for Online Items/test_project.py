from final_project import scrape_me, menu, table_of_items
from tabulate import tabulate
import pytest

def main():
    test_scrape_me()
    test_menu()
    test_table_of_items()

def test_scrape_me():
    with pytest.raises(SystemExit):
        scrape_me("test.com")
    with pytest.raises(SystemExit):
        scrape_me("test")
    with pytest.raises(SystemExit):
        scrape_me("https://www.google.com")
    with pytest.raises(SystemExit):
        scrape_me("http://www.google.com")
    assert isinstance(scrape_me("https://books.toscrape.com/catalogue/the-black-maria_991/index.html"), list)
    assert scrape_me("https://books.toscrape.com/catalogue/the-black-maria_991/index.html") == ["The Black Maria", "52.15"]

def test_menu(capsys):
    menu()
    captured_output = capsys.readouterr()
    expected_output = tabulate([
        ["Add Item", 1],
        ["Remove Item", 2],
        ["Update Prices", 3],
        ["Show Me Price Trend", 4],
        ["Exit", 5]
], headers = ["Press"], tablefmt = "fancy_grid")
    
    assert captured_output.out.strip() == expected_output.strip()

def test_table_of_items(capsys):
    test_list = [
        "test_item_1",
        "test_item_2",
        "test_item_3",
        "test_item_4",
        "test_item_5"
    ]
    table_of_items(test_list)
    captured_output = capsys.readouterr()
    expected_output = tabulate([
        ["test_item_1", 1],
        ["test_item_2", 2],
        ["test_item_3", 3],
        ["test_item_4", 4],
        ["test_item_5", 5]
], headers = ["Press"], tablefmt = "fancy_grid")
    
    assert captured_output.out.strip() == expected_output.strip()

if __name__ == "__main__":
    main()
