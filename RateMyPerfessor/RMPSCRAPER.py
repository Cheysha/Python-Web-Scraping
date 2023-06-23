import time
import numpy as np
import pandas as pd
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium import webdriver
import threading

teacher_dataframes = pd.DataFrame(columns=[
    "link", "name", "school", "department", "rating", "difficulty", "would_take_again"])
review_dataframes = pd.DataFrame(columns=['ID', 'Quality', 'Difficulty', 'Class_Name', 'Date_Taken', 'textbook',
                                          'attendence', 'grade', 'take_again', 'credit', 'Tags', 'Comment'])


def make_driver():
    # Create driver options
    option = webdriver.FirefoxOptions()
    option.add_argument("--headless")
    option.add_argument("--disable-extensions")
    # option.page_load_strategy = "eager"
    option.add_argument("--no-sandbox")
    option.add_argument("--disable-gpu")

    # Create Driver, install uBlock Origin, and return
    driver = webdriver.Firefox(options=option)
    driver.install_addon('uBlock.xpi', temporary=True)
    return driver

def process_teachers(chunk):
    # Create Driver
    driver = make_driver()
    print("driver created, getting page")

    # loop through the teachers, and get their reviews, reusing the driver
    try:
        for index, row in chunk.iterrows():
            teacher = row['link']
            print("getting reviews for", teacher)
            try:
                get_teacher_reviews(teacher, review_dataframes, driver)
            except Exception as e:
                print("error getting reviews for", teacher, e)
    finally:
        driver.close()

def get_university_teacher_list(university_id):
    # Create Driver and setup
    driver = make_driver()
    counter = 0
    max_page_count = 70
    max_teacher_count = 300

    # Get page
    url = f"https://www.ratemyprofessors.com/search/professors/{university_id}?q=*"
    print("getting page " + url)
    driver.get(url)
    print("got page + " + url)

    # Close cookie warning if it exists
    try:
        driver.find_element(By.XPATH, "/html/body/div[5]/div/div/button").click()
        print("closed cookie warning")
    except NoSuchElementException:
        print("no cookie warning found")

    # Click show more button until there are no more pages, or until the max page count is reached
    while True:
        try:
            button = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[4]/div[1]/div[1]/div[4]/button")
            # scroll unitl the button is in the middle of the screen
            driver.execute_script("arguments[0].scrollIntoView({ block: 'center', inline: 'center'})", button)
            button.click()
            time.sleep(1)
            counter += 1
            print("clicked show more button " + str(counter))

            # safe way out
            if (counter >= max_page_count):
                break
        except NoSuchElementException:
            break

    # reassure the user everything is all right
    print("finished loading page")

    # now that we've loaded all teachers on page, Scrape the page for teachers
    a_elements = driver.find_elements(By.TAG_NAME, "a")
    teacher_list_elements = []
    for teacher_element in a_elements:
        if "TeacherCard" in teacher_element.get_attribute("class"):
            t = teacher_element.text.split("\n")
            teacher_list_elements.append((teacher_element.get_attribute("href"), t))

            # safe way out of loop
            if (len(teacher_list_elements) >= max_teacher_count):
                break

    # Create dataframe from teacher list
    for teacher in teacher_list_elements:
        teacher_dataframes.loc[len(teacher_dataframes)] = [teacher[0], teacher[1][3], teacher[1][5], teacher[1][4],
                                                           teacher[1][1], teacher[1][8], teacher[1][6]]
    # Close driver, on to part 2!
    driver.close()

def get_teacher_reviews(teacher_url, review_frame, driver):
    # get page
    print("getting page for", teacher_url)
    driver.get(teacher_url)
    print("got page for", teacher_url)

    # Close cookie warning if it exists
    if len(driver.find_elements(By.XPATH, "/html/body/div[5]/div/div/button")) > 0:
        driver.find_element(By.XPATH, "/html/body/div[5]/div/div/button").click()
        print("closed cookie warning")
    else:
        print("no cookie warning found")

    # Click load more button until there are no more reviews
    while True:
        try:
            load_more_button = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[3]/div[4]/div/div/button")
            # scroll unitl the button is in the middle of the screen
            driver.execute_script("arguments[0].scrollIntoView({ block: 'center', inline: 'center'})", load_more_button)
            load_more_button.click()
            time.sleep(2)
            print("clicked load more button")
        except NoSuchElementException:
            break

    print("finished hitting load more ratings")

    # try scraping the page for reviews
    try:
        ratings_element = driver.find_element(By.XPATH, "//*[@id='ratingsList']")
        review_list = (ratings_element.find_elements(By.CSS_SELECTOR, "li"))
        print("finished getting reviews for", teacher_url)
    except NoSuchElementException:
        review_list = []
        print("no reviews found for", teacher_url)

    # words to ignore while were looping
    exclude_words = ['QUALITY', 'DIFFICULTY', 'ANY', 'ALL']

    # loop through the reviews, and add them to the dataframe
    for list_element in review_list:
        if list_element.text == "":
            review_list.remove(list_element)
            continue
        text = list_element.text.split('\n')
        tags = []
        review_string = ""
        quality = text[1]
        difficulty = text[3]
        class_name = text[4]
        date = text[5]
        url = teacher_url.split("/")
        url = url[len(url) - 1]

        # loop through the text to find the things we need
        textbook, attendance, grade, would_take_again, for_credit = "", "", "", "", ""
        for string in text:
            if len(string) > len(review_string):
                review_string = string
            if "Textbook:" in string:
                textbook = string.split(":")[1]
            if "Attendance:" in string:
                attendance = string.split(":")[1]
            if "Grade:" in string:
                grade = string.split(":")[1]
            if "Would Take Again:" in string:
                would_take_again = string.split(":")[1]
            if "For Credit:" in string:
                for_credit = string.split(":")[1]
            if string.isupper() and not any(word in string for word in exclude_words) and not string == class_name:
                tags.append(string)

        # create the dataframe from the data we've collected
        review_dataframes.loc[len(review_dataframes)] = [url, quality, difficulty, class_name, date, textbook,
                                                         attendance,
                                                         grade, would_take_again, for_credit, tags,
                                                         review_string]


if __name__ == '__main__':
    # get the initial teacher dataframes that we will need to pass into the threads, pass the school id
    school_id = 2932
    teacher_ratings = get_university_teacher_list(school_id)
    print(teacher_dataframes.to_string())
    print("got teacher list ", len(teacher_dataframes), " gettting reviews")

    # split the teacher dataframes into n chunks
    n = 4
    chunks = np.array_split(teacher_dataframes, n)

    # create the threads
    threads = []
    for i in range(n):
        threads.append(threading.Thread(target=process_teachers, args=(chunks[i],)))

    # start the threads
    for thread in threads:
        thread.start()

    # wait for the threads to finish
    for thread in threads:
        thread.join()

    # reassure the user that everything is okay
    print("finished getting reviews")

    # print the dataframes
    print(review_dataframes.to_string())

    # Exporting the dataframes collected to csv
    teacher_dataframes.to_csv(f'./Data/{school_id}teacher_dataframes.csv', index=False)
    review_dataframes.to_csv(f'./Data/{school_id}review_dataframes.csv', index=False)
