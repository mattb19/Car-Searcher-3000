import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from Car import Car
import re


def AutoTrader():
    lst = []
    URL = "https://www.autotrader.com/cars-for-sale/all-cars/cars-under-30000/audi/q5/raleigh-nc-27615?requestId=1819194850&maxMileage=60000&searchRadius=100&startYear=2018&endYear=2019&marketExtension=off&isNewSearch=true&showAccelerateBanner=false&sortBy=derivedpriceASC&numRecords=25"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="mountNode")
    car_elements = results.find_all("div", class_="col-xs-8 item-card-content display-flex flex-column justify-content-between")

    for car in car_elements:
        price = car.find("span", class_="first-price")
        title = car.find("h2", class_="text-bold text-size-400 text-size-sm-500 link-unstyled")
        mileage = car.find("ul", class_="list list-inline display-inline margin-bottom-0 pipe-delimited text-gray text-size-300")
        distance = car.find("span", class_="text-normal padding-left-1")
        website1 = car.find("div", class_="display-flex justify-content-between")
        website2 = website1.find("a")
        website = "autotrader.com"+website2['href']

        vehicle = Car(price.text, title.text, mileage.text, re.findall(r'\d+\.\d+', distance.text.strip())[0], website)
        if isBlackListed(vehicle):
            continue
        else:
            lst.append(website)

    return lst


def Edmunds():
    lst = []
    URL = "https://www.edmunds.com/inventory/srp.html?deliverytype=local&make=audi&mileage=22000-60000&model=q5&radius=100&year=2018-2019&wz=45&price=26000-30000"
    browser = webdriver.Chrome(executable_path=ChromeDriverManager().install())
    browser.get(URL)
    soup = BeautifulSoup(browser.page_source, "html.parser")
    browser.close()
    results = soup.find(id="main-content")
    car_elements = results.find_all("div", class_="vehicle-info d-flex flex-column px-1 pt-1 pb-0_5")

    for car in car_elements:
        price = car.find("span", class_="heading-3")
        title = car.find("div", class_="size-16 font-weight-bold mb-0_5 text-primary-darker")
        mileage = car.find("div", class_="key-point size-14 d-flex align-items-baseline mt-0_5 col-12")
        distance = car.find("span", class_="text-gray-dark")
        website1 = car.find("a", class_="usurp-inventory-card-vdp-link")
        website = "edmunds.com"+website1['href']

        vehicle = Car(price.text, title.text, mileage.text, re.findall(r'\d', distance.text.strip())[0], website)
        if isBlackListed(vehicle):
            continue
        else:
            lst.append(website)

    return lst


def isBlackListed(car):
    f = open('Blacklist.txt','r')
    blackList = f.readlines()
    if car.getId() in blackList:
        return True
    else:
        if car.getDistance() > 150.0:
            setBlackListed(car)
            return True
        else:
            return False


def setBlackListed(car):
    f = open('Blacklist.txt', 'w')
    f.write(car.getId()+'\n')
    f.write()
    print("A Car Has Been Blacklisted")


def main():
    todaysList = Edmunds()+AutoTrader()
    for i in todaysList:
        print(i)


main()
