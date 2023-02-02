# Car-Searcher-3000
This program runs through a predetermined car filter on supported websites.

## Dependencies
```console
pip install bs4
pip install selenium
pip install webdriver-manager
```

## Setup
* Do not touch Car.py or geckodriver.log
1. In the main function of Scrape.py, comment out/in the OS you use between lines 165-172 and lines 185-192
2. Go online to any supported website (AutoTrader.com, CarGurus.com, AutoTempest.com, Edmunds.com)
3. Create a search for a car you like. Be sure to include any filters you require
4. Copy the URL
5. In urls.txt, you can add the URL in this format: WebsiteName`URL - See examples in urls.txt
* Be sure there are no extra lines in urls.txt, only lines containing your sites

## How to Run
Run it using the following command:
```console
python3 Scrape.py
```

1. Give the scraper a second to check the sites. It's faster for some than others
2. Some sites will pop up a window. Do NOT touch the window, it will close soon enough
3. If there are cars available, it will give you a list of cars in the terminal and pop up windows with all the listings
* The order of cars in the terminal is the same order as the cars that popped up in the windows
* You will be prompted with an option to blacklist an item from the list of cars. Type the number of the listing if you want this
* If you don't want to blacklist any cars, you can press the "N" key
* The program will automatically end if you blacklist every car
4. If there are no cars available, pug

## The Blacklist
* The blacklist contains cars that you are not interested in
* It will prevent these cars from popping up in future executions of the program
* You can remove a car from the blacklist by opening blacklists.txt and manually deleting the line