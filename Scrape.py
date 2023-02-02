import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from Car import Car
import re
import webbrowser


def AutoTrader(url):
    lst = []
    page = requests.get(url)
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
        website = "https://autotrader.com"+website2['href']

        vehicle = Car("$"+price.text, title.text, mileage.text, re.findall(r'\d+\.\d+', distance.text.strip())[0], website)
        if isBlackListed(vehicle):
            continue
        else:
            lst.append(vehicle)

    return lst


def Edmunds(url):
    lst = []
    browser = webdriver.Chrome(executable_path=ChromeDriverManager().install())
    browser.get(url)
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
        website = "https://edmunds.com"+website1['href']

        vehicle = Car(price.text, title.text, mileage.text, re.findall(r'\d', distance.text.strip())[0], website)
        if isBlackListed(vehicle):
            continue
        else:
            lst.append(vehicle)

    return lst


def AutoTempest(url):
    lst = []
    browser = webdriver.Chrome(executable_path=ChromeDriverManager().install())
    browser.get(url)
    soup = BeautifulSoup(browser.page_source, "html.parser")
    browser.close()
    results = soup.find(id="results-body")
    car_elements = results.find_all("li", class_="result-list-item")

    for car in car_elements:
        price = car.find("div", class_="badge__label label--price")
        title = car.find("span", class_="title-wrap listing-title")
        mileage = car.find("span", class_="mileage")
        website1 = car.find("span", class_="title-wrap listing-title")
        website2 = website1.find("a")
        website = website2['href']

        vehicle = Car(price.text, title.text.rstrip().lstrip(), mileage.text, "10", website)
        if isBlackListed(vehicle):
            continue
        else:
            lst.append(vehicle)

    return lst


def isBlackListed(car):
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


def setBlackListed(car):
    f = open('Blacklist.txt', 'a')
    f.write(car.getId()+'\n')
    print("A Car Has Been Blacklisted")
    f.close()


def main():
    f = open('urls.txt', 'r')
    siteList = [i.split("`") for i in f.readlines()]
    todaysList = []
    for i in siteList:
        url = i[1].strip('\n')
        if i[0] == 'AutoTrader':
            todaysList += AutoTrader(url)
        elif i[0] == 'AutoTempest':
            todaysList += AutoTempest(url)
        elif i[0] == 'Edmunds':
            todaysList += Edmunds(url)
        else:
            print("Error in urls.txt")
            return

    if len(todaysList) == 0:
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

        for i in todaysList:
            carNum = todaysList.index(i)+1
            print("Car "+str(carNum))
            print(i)

            url = str(i.getWebsite())

            # MacOS
            chrome_path = 'open -a /Applications/Google\ Chrome.app %s'

            # Windows
            # chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'

            # Linux
            # chrome_path = '/usr/bin/google-chrome %s'

            webbrowser.get(chrome_path).open(url)

        blackList = True
        while blackList:
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
                continue
            else:
                break

main()
