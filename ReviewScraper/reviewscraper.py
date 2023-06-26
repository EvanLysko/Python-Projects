from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time

PATH = "/Users/evanlysko/Desktop/ReviewScraper/chromedriver"
driver = webdriver.Chrome(PATH)


def sort_newest():
    filter = driver.find_element_by_xpath("/html/body/jsl/div[3]/div[9]/div[8]/div/div[1]/div/div/div[2]/div[7]/div[2]/div/button")
    filter.click()
    time.sleep(4)
    newest = driver.find_element_by_xpath("/html/body/jsl/div[3]/div[4]/div[1]/ul/li[2]")
    newest.click()


def scroll():
    scrollable_div = driver.find_element_by_css_selector('div.section-layout.section-scrollbox.scrollable-y.scrollable-show')
    times = driver.find_element_by_xpath("/html/body/jsl/div[3]/div[9]/div[8]/div/div[1]/div/div/div[2]/div[2]/div/div[2]/div[2]").text
    times = [int(s) for s in times.split() if s.isdigit()]
    times = times[0]/8
    count = 0
    while count < times:
        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_div)
        time.sleep(2)
        count += 1


def expand_revs():
    mores = driver.find_elements_by_class_name("section-expand-review blue-link")
    for more in mores:
        more.click()
        time.sleep(2)


def get_usernames():
    username_elements = driver.find_elements_by_class_name("section-review-title")
    usernames = []
    for i in username_elements:
        if i.text not in usernames:
            usernames.append(i.text)
    return usernames


def get_reviews_and_responses():
    response_dates = []
    responses = []
    for i in driver.find_elements_by_class_name("section-review-owner-response"):
        response_dates.append(i.text.splitlines()[0])
        responses.append(i.text.splitlines()[1])

    reviews_class = driver.find_elements_by_class_name("section-review-text")
    temp_reviews = {}
    count = 0
    for i in range(len(reviews_class)):
        temp = reviews_class[i].text
        if i < (len(reviews_class)-1):
            if temp in responses:
                temp_reviews[i-1] = [reviews_class[i-1].text, response_dates[count], responses[count]]
                count += 1
            if temp not in responses and reviews_class[i+1].text not in responses:
                temp_reviews[i] = [temp, "no response"]
        else:
            if temp in responses:
                temp_reviews[i-1] = [reviews_class[i-1].text, response_dates[count], responses[count]]
                count += 1
            if temp not in responses:
                temp_reviews[i] = [temp, "no response"]
    count = 0
    reviews = {}
    for key in temp_reviews:
        reviews[count] = temp_reviews[key]
        count += 1
    return reviews


def get_ratings():
    rating_class = driver.find_elements_by_class_name("section-review-stars")
    ratings = []
    for i in rating_class:
        ratings.append(i.get_attribute("aria-label"))
    return ratings


def get_times():
    time_class = driver.find_elements_by_class_name("section-review-publish-date")
    times = []
    for i in time_class:
        times.append(i.text)
    return times


def main(link):
    driver.get(link)

    driver.implicitly_wait(5)

    sort_newest()
    time.sleep(2)
    scroll()
    expand_revs()
    ratings = get_ratings()
    times = get_times()
    usernames = get_usernames()
    reviews = get_reviews_and_responses()

    return usernames, times, ratings, reviews

clay_place = "https://www.google.com/maps/place/Katie's+Clay+Studio/@40.555427,-79.9597367,17z/data=!3m1!4b1!4m7!3m6!1s0x0:0xef9e061aede73d9b!8m2!3d40.555427!4d-79.957548!9m1!1b1"
pma_tattoo = "https://www.google.com/maps/place/PMA+Tattoo/@40.4715683,-80.0747515,17z/data=!3m1!4b1!4m7!3m6!1s0x0:0xa705736aa5fa6fbd!8m2!3d40.4715683!4d-80.0725628!9m1!1b1"


usernames, times, ratings, reviews= main(pma_tattoo)

print(len(usernames), len(times), len(ratings), len(reviews))
print(reviews)

with open('pma_tattoo.txt', 'w') as f:
    for i in range(len(reviews)):
        if len(reviews[i]) == 2:
            f.write("%s\n%s\n%s\nReview: %s\n%s\n\n" % (usernames[i], times[i], ratings[i], reviews[i][0], reviews[i][1]))
        else:
            f.write("%s\n%s\n%s\nReview: %s\n%s\n%s\n\n" % (usernames[i], times[i], ratings[i], reviews[i][0], reviews[i][1], reviews[i][2]))
