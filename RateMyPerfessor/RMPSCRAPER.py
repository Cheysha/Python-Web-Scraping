import time
import pandas as pd

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium import webdriver
import threading
from teacherClass import Teacher

def get_university_teacher_list(university_id):
    counter = 0

    option = webdriver.EdgeOptions()
    option.add_argument("--headless")
    option.add_argument("log-level=3")
    option.add_argument("--disable-extensions")
    option.add_argument("--no-sandbox")
    option.add_argument("--disable-gpu")
    option.page_load_strategy = "eager"
    driver = webdriver.Edge(options=option)
    '''
    option = webdriver.FirefoxOptions()
    option.add_argument("--headless")
    option.add_argument("log-level=3")
    option.add_argument("--disable-extensions")
    #option.page_load_strategy = "eager"
    #option.add_argument("--no-sandbox")
    option.add_argument("--disable-gpu")
    driver = webdriver.Firefox(options=option)
    print("driver created, getting page")
    '''

    '''
        THIS GETS THE PAGE
    '''
    driver.get(f"https://www.ratemyprofessors.com/search/teachers?query=*&sid={university_id}")

    print("got page")

    '''
        THIS CLOSES THE COOKIE WARNING IF IT EXISTS
    '''
    if len(driver.find_elements(By.XPATH, "/html/body/div[5]/div/div/button")) > 0:
        print("closed cookie warning")
        driver.find_element(By.XPATH, "/html/body/div[5]/div/div/button").click()
    else:
        print("no cookie warning found")

    '''
        THIS CLICKS THE SHOW MORE BUTTON UNTIL THERE ARE NO MORE TEACHERS TO LOAD
    '''
    while True:
        button = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[4]/div[1]/div[1]/div[4]/button")

        if (button != None):
            button.click()
            time.sleep(2)
            counter += 1
            print("clicked show more button " + str(counter))
        else:
            break

    print("finished loading page")

    '''
        THIS GETS THE LIST OF TEACHERS FROM THE PAGE
    '''
    # find every <a> that has "TeacherCard" in the class name
    a_elements = driver.find_elements(By.TAG_NAME, "a")
    teacher_list_elements = []

    for teacher_element in a_elements:
        if "TeacherCard" in teacher_element.get_attribute("class"):
            print(teacher_element.get_attribute("href"))

            t = teacher_element.text.split("\n")
            teacher_list_elements.append((teacher_element.get_attribute("href"), t))

            if(len(teacher_list_elements) == 6): # TESTING BREAK
                break
    '''
        THIS CREATES A LIST OF TEACHER OBJECTS FROM THE LIST OF TEACHERS
    '''
    teacher_list = [] # the return list with teacher objects
    for teacher in teacher_list_elements:
        n = Teacher(code=teacher[0], name=teacher[1][3], school=teacher[1][5], department=teacher[1][4],
                    rating=teacher[1][1], difficulty=teacher[1][8], would_take_again=teacher[1][6])
        teacher_list.append(n)



    driver.close()
    return teacher_list

def get_teacher_reviews(teacher: Teacher, driver):

    print("getting page for", teacher.code)

    '''
        THIS GETS THE REVIEWS FOR EACH TEACHER
    '''
    driver.get(teacher.code)

    print("got page for", teacher.code)

    '''
        THIS CLOSES THE COOKIE WARNING IF IT EXISTS
    '''
    if len(driver.find_elements(By.XPATH, "/html/body/div[5]/div/div/button")) > 0:
        driver.find_element(By.XPATH, "/html/body/div[5]/div/div/button").click()
        print("closed cookie warning")
    else:
        print("no cookie warning found")

    '''
        THIS CLICKS THE LOAD MORE BUTTON UNTIL THERE ARE NO MORE REVIEWS TO LOAD
    '''
    while True:
       load_more_button = driver.find_elements(By.XPATH, "/html/body/div[2]/div/div/div[3]/div[4]/div/div/button")

       if len(load_more_button) > 0:
            load_more_button[0].click()
            # wait one second
            time.sleep(2)
            print("clicked load more button")
       else: break

    print("finished hitting load more ratings")

    '''
        THIS GETS THE LIST OF REVIEWS FROM THE PAGE
    '''
    try:
        ratings_element = driver.find_element(By.XPATH, "//*[@id='ratingsList']")
        review_list = (ratings_element.find_elements(By.CSS_SELECTOR, "li"))
    except NoSuchElementException:
        review_list = []
        print("no reviews found for", teacher.name)

    # remove empty elements
    for list_element in review_list:
        if list_element.text == "":
            review_list.remove(list_element)

    comments = []

    '''
        THIS GETS THE TEXT FROM EACH REVIEW, AND ADDS IT TO THE TEACHER OBJECT
    '''
    for list_element in review_list:
        text = list_element.text.split('\n')
        try:
            temp_comment = {'class': text[4], 'date': text[7], 'comment': text[8], 'quality': text[1],
                            'difficulty': text[3], 'would_take_again': text[5], 'grade': text[9], 'tags': text[10]}
        except IndexError:
            temp_comment = text

        comments.append(temp_comment)

    teacher.comments = comments


def process_teachers(teachers): # teachers, a list of teacher objects
    option = webdriver.EdgeOptions()
    #option.add_argument("--headless")
    option.add_argument("log-level=3")
    option.add_argument("--disable-extensions")
    option.add_argument("--no-sandbox")
    option.add_argument("--disable-gpu")
    #option.page_load_strategy = 'eager'
    driver = webdriver.Edge(options=option)
    '''
    option = webdriver.FirefoxOptions()
    option.add_argument("--headless")
    option.add_argument("log-level=3")
    option.add_argument("--disable-extensions")
    option.add_argument("--no-sandbox")
    option.add_argument("--disable-gpu")
    option.page_load_strategy = 'eager'
    driver = webdriver.Firefox(options=option)
    print("driver created, getting page")
    '''
    try:
        for teacher in teachers:
            reviews = get_teacher_reviews(teacher, driver)
            # Do something with the reviews, such as write them to a file
    finally:
        driver.close()



if __name__ == '__main__':
    test_list = get_university_teacher_list(946)

    print("got teacher list ", len(test_list), " gettting reviews")

    #TODO: use a thread pool to get reviews for each teacher

    # split the list into 2 lists of equal size
    half = len(test_list) // 2
    first_half = test_list[:half]
    second_half = test_list[half:]

    # create a thread for each list
    t1 = threading.Thread(target=process_teachers, args=(first_half,))
    t2 = threading.Thread(target=process_teachers, args=(second_half,))

    # start the threads
    t1.start()
    t2.start()

    # wait for the threads to finish
    t1.join()
    t2.join()

    print("finished getting reviews")

    for teacher in test_list:
        if teacher.comments == None:
            print("failed to get comments for", teacher.name)
        else:
            print("got comments for", teacher.name, len(teacher.comments))
