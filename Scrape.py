import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from Car import Car
import re
import webbrowser


def CarGurus(url):              # Scrapes CarGurus with extra comments
    lst = []
    page = requests.get(url)                                                        #
    soup = BeautifulSoup(page.content, "html.parser")                               # Gets all html code and turns it into
    results = soup.find(id="cargurus-listing-search")                               # a readable format
    car_elements = results.find_all("div", class_="cardBodyPadding cardBody")       #

    for car in car_elements:             # Searches each car's html code
        price = car.find("span", class_="price")
        price = price.text.lstrip().rstrip()
        title = car.find("h4", class_="titleText")
        title = title.text.lstrip().rstrip()
        mileage = car.find("div", class_="mileage")
        mileage = mileage.text.lstrip().rstrip()
        miles = mileage[0:6]
        
        distance = car.find("p", class_="distanceAndLocationText")
        distance = distance.text.lstrip().rstrip().split(' ')[1]
        if distance != "NC":
            distance = 10000
        else:
            distance = 0
        website2 = car.find("a")
        website = url+website2['href']
        
        counter = 0
        price1 = ""
        while counter < 7:
            price1 += price[counter]
            counter += 1

        vehicle = Car(price1, title, miles, distance, website)     # initializes car object
        if isBlackListed(vehicle):              # determines if car should show up on todays list
            continue
        else:
            lst.append(vehicle)

    return lst


def AutoTrader(url):            # Scrapes AutoTrader
    lst = []
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="mountNode")
    car_elements = results.find_all("div", class_="col-xs-8 item-card-content display-flex flex-column justify-content-between")

    for car in car_elements:
        price = car.find("span", class_="first-price")
        price = price.text
        title = car.find("h2", class_="text-bold text-size-400 text-size-sm-500 link-unstyled")
        mileage = car.find("ul", class_="list list-inline display-inline margin-bottom-0 pipe-delimited text-gray text-size-300")
        mileage = mileage.text
        miles = mileage[0:6]
        distance = car.find("span", class_="text-normal padding-left-1")
        website1 = car.find("div", class_="display-flex justify-content-between")
        website2 = website1.find("a")
        website = "https://autotrader.com"+website2['href']
        
        counter = 0
        price1 = "$"
        while counter < 6:
            price1 += price[counter]
            counter += 1

        vehicle = Car(price1, title.text, miles, re.findall(r'\d+\.\d+', distance.text.strip())[0], website)
        if isBlackListed(vehicle):
            continue
        else:
            lst.append(vehicle)

    return lst


def Edmunds(url):               # Scrapes Edmunds
    lst = []
    service = Service(executable_path=ChromeDriverManager().install())
    browser = webdriver.Chrome(service=service)
    browser.get(url)
    browser.implicitly_wait(2)
    soup = BeautifulSoup(browser.page_source, "html.parser")
    browser.close()
    results = soup.find(id="main-content")
    car_elements = results.find_all("div", class_="vehicle-info d-flex flex-column px-1 pt-1 pb-0_5")

    for car in car_elements:
        price = car.find("span", class_="heading-3")
        price = price.text
        title = car.find("div", class_="size-16 font-weight-bold mb-0_5 text-primary-darker")
        mileage = car.find("div", class_="key-point size-14 d-flex align-items-baseline mt-0_5 col-12")
        mileage = mileage.text
        miles = mileage[0:6]
        distance = car.find("span", class_="text-gray-dark")
        website1 = car.find("a", class_="usurp-inventory-card-vdp-link")
        website = "https://edmunds.com"+website1['href']
        
        counter = 0
        price1 = ""
        while counter < 7:
            price1 += price[counter]
            counter += 1

        vehicle = Car(price1, title, miles, re.findall(r'\d', distance.text.strip())[0], website)
        if isBlackListed(vehicle):
            continue
        else:
            lst.append(vehicle)

    return lst


def CarsForSale(url):           # Scrapes CarsForSale
    lst = []
    service = Service(executable_path=ChromeDriverManager().install())
    browser = webdriver.Chrome(service=service)
    browser.get(url)
    browser.implicitly_wait(2)
    soup = BeautifulSoup(browser.page_source, "html.parser")
    browser.close()
    results = soup.find(id="on-canvas-results")
    car_elements = results.find_all("li", class_="snapshot")

    for car in car_elements:
        price = car.find("li", class_="snapshot__details-price")
        price = price.text
        title = car.find("a", class_="snapshot__title")
        mileage = car.find("li", class_="snapshot__details-miles")
        mileage = mileage.text
        miles = mileage[0:6]
        distance = 0
        website1 = car.find("a", class_="snapshot__title")
        website = "https://carsforsale.com"+website1['href']
        
        counter = 0
        price1 = ""
        while counter < 7:
            price1 += price[counter]
            counter += 1

        vehicle = Car(price1, title.text, miles, distance, website)
        if isBlackListed(vehicle):
            continue
        else:
            lst.append(vehicle)

    return lst


def AutoTempest(url):           # Scrapes AutoTempest
    lst = []
    service = Service(executable_path=ChromeDriverManager().install())
    browser = webdriver.Chrome(service=service)
    browser.get(url)
    soup = BeautifulSoup(browser.page_source, "html.parser")
    browser.close()
    results = soup.find(id="results-body")
    car_elements = results.find_all("li", class_="result-list-item")

    for car in car_elements:
        price = car.find("div", class_="badge__label label--price")
        price = price.text
        title = car.find("span", class_="title-wrap listing-title")
        mileage = car.find("span", class_="mileage")
        mileage = mileage.text
        miles = mileage[0:6]
        website1 = car.find("span", class_="title-wrap listing-title")
        website2 = website1.find("a")
        website = website2['href']

        counter = 0
        price1 = ""
        while counter < 7:
            price1 += price[counter]
            counter += 1

        vehicle = Car(price1, title.text.rstrip().lstrip(), miles, "10", website)
        if isBlackListed(vehicle):
            continue
        else:
            lst.append(vehicle)

    return lst


def isBlackListed(car):         # Checks if car is blacklisted by car id
    f = open('Blacklist.txt','r')
    blackList = [i.strip('\n') for i in f.readlines()]
    if car.getId() in blackList:
        return True
    else:
        if car.getDistance() > 150.0:
            setBlackListed(car)
            f.close()
            return True
        else:
            f.close()
            return False


def setBlackListed(car):        # Adds a car's id to blacklist
    f = open('Blacklist.txt', 'a')
    f.write(car.getId()+'\n')
    print("A Car Has Been Blacklisted")
    f.close()


def main():
    f = open('urls.txt', 'r')
    siteList = [i.split("`") for i in f.readlines()]    # getting all websites in urls.txt
    todaysList = []

    for i in siteList:               # filters urls by website name, initializes their scraper
        url = i[1].strip('\n')
        if i[0] == 'AutoTrader':
            todaysList += AutoTrader(url)
        elif i[0] == 'AutoTempest':
            todaysList += AutoTempest(url)
        elif i[0] == 'Edmunds':
            todaysList += Edmunds(url)
        elif i[0] == 'CarGurus':
            todaysList += CarGurus(url)
        elif i[0] == 'CarsForSale':
            todaysList += CarsForSale(url)
        else:
            print("Error in urls.txt")
            return
    
    t1 = [i.getId() for i in todaysList]        # destroys duplicates
    t2 = []
    for i in range(len(todaysList)):
        if t1.count(todaysList[i].getId()) > 1:
            t1.remove(todaysList[i].getId())
        else:
            t2.append(todaysList[i])
    
    todaysList = t2

    if len(todaysList) == 0:            # checks if there are no new cars
        url = "https://puginarug.com/"

        # MacOS
        chrome_path = 'open -a /Applications/Google\ Chrome.app %s'

        # Windows
        # chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'

        # Linux
        # chrome_path = '/usr/bin/google-chrome %s'

        webbrowser.get(chrome_path).open(url)

        return
    else:
        for i in todaysList:            # opens each new car listing
            carNum = todaysList.index(i)+1
            print("Car "+str(carNum))
            print(i)

            url = str(i.getWebsite())

            # MacOS
            # chrome_path = 'open -a /Applications/Google\ Chrome.app %s'

            # Windows
            chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'

            # Linux
            # chrome_path = '/usr/bin/google-chrome %s'

            webbrowser.get(chrome_path).open(url)

        blackList = True
        blackListCount = 0
        while blackList:                # lets user choose which cars to blacklist
            if blackListCount >= len(todaysList):
                print("You have blacklisted everything! No more cars for today")
                break
            else:
                result = input("Want to blacklist a car? Type the number. If not, type 'N'. ")
                result.lower()
                if not result.isdigit() and result != 'n':
                    print("Not a valid input. Try again.")
                    continue
                elif result.isdigit() and (int(result) > len(todaysList) or int(result) < 1):
                    print("Not a valid input. Try again.")
                    continue
                elif result.isdigit():
                    setBlackListed(todaysList[int(result)-1])
                    blackListCount += 1
                    continue
                else:
                    break


main()
