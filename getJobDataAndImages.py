
from os import mkdir
from xml.etree.ElementTree import tostring
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
import time


class cssRemoved(object):
    def __init__(self, locator, css_class):
        self.locator = locator
        self.css_class = css_class

    def __call__(self, driver):
        element = self.locator  # Finding the referenced element
        if self.css_class in element.get_attribute("class"):
            return False
        else:
            return element


def toastRemover(driver):
    driver.execute_script("""
    var element = document.querySelector("#toasts");
    if (element)
        element.parentNode.removeChild(element);
    """)


def waitLocateWithClass(wait, name):
    print("wait locating", name)
    try:
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, name)))
        return True
    except TimeoutException:
        return False


def waitLocatedWithId(wait, name):
    print("wait locating", name)
    try:
        wait.until(EC.presence_of_element_located((By.ID, name)))
        return True
    except TimeoutException:
        return False


def waitCssRemoved(wait, item, name):
    print("wait remove tag", name)
    try:
        wait.until(cssRemoved(item, name))
        return True
    except TimeoutException:
        return False
    except:
        time.sleep(1)


def cFinderM(driver, name):
    print("find","class M", name)
    return driver.find_elements(By.CLASS_NAME, name)


def iFinderM(driver, name):
    print("find","id M", name)
    return driver.find_elements(By.ID, name)


def cFinder(driver, name):
    print("find","class", name)
    return driver.find_element(By.CLASS_NAME, name)


def iFinder(driver, name):
    print("find","id", name)
    return driver.find_element(By.ID, name)


def waitFind(driver, wait, waiter, finder, name):
    waiter(wait, name)
    return finder(driver, name)


def scroll(driver, item):
    x = item.location['x']
    y = item.location['y']
    scroll_by_coord = 'window.scrollTo(%s,%s);' % (x, y)
    scroll_nav_out_of_way = 'window.scrollBy(0, -120);'
    driver.execute_script(scroll_by_coord)
    driver.execute_script(scroll_nav_out_of_way)


def scroller(driver, item):
    try:
        scroll(driver, item)
        actions = ActionChains(driver)
        actions.move_to_element(item)
        actions.click()
        return True
    except:
        return False


def clicker(driver, item):
    try:
        if (scroller(driver, item)):
            item.click()
            return True
        else:
            False
    except:
        return False


def setup(loginUrl, mail, password):
    driver = webdriver.Firefox()
    driver.get(loginUrl)
    mailInput = driver.find_element(By.NAME, "session_key")
    mailInput.clear()
    mailInput.send_keys(mail)
    passInput = driver.find_element(By.NAME, "session_password")
    passInput.clear()
    passInput.send_keys(password)
    passInput.send_keys(Keys.ENTER)
    wait = WebDriverWait(driver, 50)
    waitLocateWithClass(wait, "search-global-typeahead__input")
    return driver


def runner(driver, logFile, dataFile, pageStart=0, counter=0):
    base = [driver, logFile, dataFile, pageStart, counter]
    print("runner Entered")
    try:
        driver.get(
            "https://www.linkedin.com/jobs/search/?keywords=Metaverse&location=Worldwide&start=" + str(pageStart))
        wait = WebDriverWait(driver, 10)
        print("runner Entered")
        waitLocateWithClass(wait, "scaffold-layout__list-container")
        toastRemover(driver)
        s = cFinder(driver, "global-footer-compact")
        driver.execute_script("arguments[0].scrollIntoView(true);", s)
        itemList = cFinderM(driver, "jobs-search-results__list-item")
        print(pageStart + counter + 1, "->", 1, ":", len(itemList),
              "Data Found at Land", file=logFile, flush=True)
        while counter < len(itemList):
            itemList = cFinderM(driver, "jobs-search-results__list-item")
            item = itemList[counter]
            print(pageStart+counter+1, "->", counter+1, ":",
                  len(itemList), item, file=logFile, flush=True)
            driver.execute_script("arguments[0].scrollIntoView(true);", item)
            clickItem = cFinder(item, "artdeco-entity-lockup__title")
            clicker(driver, clickItem)
            logText = "{} -> {} : {}".format(pageStart +
                                             counter+1, counter+1, len(itemList))
            if dataWriter(driver, item, logFile, dataFile, pageStart + counter, logText) == False:
                print(pageStart+counter+1, "->", counter+1, ":", len(itemList),
                      "Reloaded - Data Not Load", file=logFile, flush=True)
                return pageStart, counter
            counter += 1
        print(pageStart+counter, "->", counter, ":", len(itemList),
              "Loop Ended", file=logFile, flush=True)
        return pageStart + counter, 0
    except:
        print(pageStart+counter, "->", counter, ":", len(itemList),
              "Reloaded - Page Not load", file=logFile, flush=True)
        return base[3], counter



def dataWriter(driver, item, logFile, dataFile, counter, logText):
    driver.save_screenshot(f'imgs/{counter}b.png')
    wait = WebDriverWait(driver, 10)
    salary = waitFind(driver, wait, waitLocatedWithId, iFinder, "SALARY")
    driver.execute_script("arguments[0].scrollIntoView(true);", salary)
    if waitCssRemoved(wait, salary, "jobs-box--generic-occludable-area-large"):
        print("waitCssRemoved" "returned true")
        driver.save_screenshot(f'imgs/{counter}e.png')
        print(counter, "-->", cFinder(item, "job-card-list__title").text,
              file=dataFile, flush=True)
        print(cFinder(item, "job-card-container__primary-description").text,
              file=dataFile, flush=True)
        print(cFinder(item, "job-card-container__metadata-item").text,
              file=dataFile, flush=True)
        print("Name Part Endned")
        mainLabel = iFinder(driver, "job-details")
        for t in mainLabel.find_elements(By.XPATH, "./*"):
            if t.text != "":
                print(t.text, file=dataFile, flush=True)
        print("\n--------------------------------------\n",
              file=dataFile, flush=True)
        print(logText, "write successful", file=logFile, flush=True)
        print("write" "ended")
        return True
    else:
        print("waitCssRemoved" "returned false")
        return False


loginUrl = "https://www.linkedin.com/"
mail = ""
password = ""
searchUrl = "https://www.linkedin.com/jobs/search/?keywords=metaverse&location=Worldwide&refresh=true&start="

[logFile, dataFile] = [open("./log.txt", "w"), open("./data/data.txt", "w")]
driver = setup(loginUrl, mail, password)
pageStart, counter = 0, 0
while True:
    try:
        pageStart, counter = runner(
            driver, logFile, dataFile, pageStart, counter)
    except:
        pageStart, counter = runner(
            driver, logFile, dataFile, pageStart, counter)
    print(pageStart, counter)
