import time
import numpy as np
import pandas as pd
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium import webdriver
import threading

'''
    get_university_teacher_list; returns a dataframe of teachers from a university, can be called by itself
    process_teachers; takes a dataframe of teachers and returns a dataframe of reviews for each teacher, can be called by itself
    get_teacher_reviews; returns a dataframe of reviews for a teacher, must be called by process_teachers
'''


def make_driver():
    #option = webdriver.ChromeOptions()
    option = webdriver.FirefoxOptions()
    #option.add_argument("--headless")
    #option.add_argument("log-level=3")
    option.add_argument("--disable-extensions")
    #option.page_load_strategy = "eager"
    option.add_argument("--no-sandbox")
    option.add_argument("--disable-gpu")

    #driver = webdriver.Chrome(options=option)
    driver = webdriver.Firefox(options=option)
    driver.install_addon('uBlock.xpi', temporary=True)

    return driver
def get_university_teacher_list(university_id):
    counter = 0
    max_page_count = 1
    max_teacher_count = 5

    teacher_dataframes = pd.DataFrame(columns=[
        "link", "name", "school", "department", "rating", "difficulty", "would_take_again"])

    driver = make_driver()
    print("driver created, getting page")

    '''
        THIS GETS THE PAGE
    '''
    url = f"https://www.ratemyprofessors.com/search/professors/{university_id}?q=*"
    driver.get(url)
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
        try:
            button = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[4]/div[1]/div[1]/div[4]/button")
        except NoSuchElementException:
            button = None

        if (button != None):
            # scroll unitl the button is in the middle of the screen
            driver.execute_script("arguments[0].scrollIntoView({ block: 'center', inline: 'center'})", button)
            #driver.set_window_position()

            button.click()
            time.sleep(1)
            counter += 1
            print("clicked show more button " + str(counter))
            if (counter >= max_page_count): # TESTING BREAK
                break

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
            t = teacher_element.text.split("\n")
            teacher_list_elements.append((teacher_element.get_attribute("href"), t))

            if(len(teacher_list_elements) >= max_teacher_count): # TESTING BREAK
                break

    '''
        THIS CREATES A LIST OF TEACHER OBJECTS FROM THE LIST OF TEACHERS
    '''
    ############################################# CREATING DATAFRAMES #############################################

    for teacher in teacher_list_elements:
        data = {"link": teacher[0], "name": teacher[1][3], "school": teacher[1][5], "department": teacher[1][4], "rating": teacher[1][1], "difficulty": teacher[1][8], "would_take_again": teacher[1][6]}
        t = pd.DataFrame(data, index=[0])
        teacher_dataframes.loc[len(teacher_dataframes)] = [teacher[0], teacher[1][3], teacher[1][5], teacher[1][4], teacher[1][1], teacher[1][8], teacher[1][6]]

    '''
        THIS CLOSES THE DRIVER, END OF FUNCTION
    '''
    driver.close()
    return teacher_dataframes
def get_teacher_reviews(teacher_url, review_frame ,driver):
    '''
        THIS GETS THE REVIEWS FOR EACH TEACHER
    '''


    driver.get(teacher_url)
    print("got page for", teacher_url)

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
            #driver.execute_script("arguments[0].scrollIntoView({ block: 'center', inline: 'center'})", load_more_button) # scroll unitl the button is in the middle of the screen
            load_more_button[0].click()
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
        print("finished getting reviews for", teacher_url)
    except NoSuchElementException:
        review_list = []
        print("no reviews found for", teacher_url)

    # remove empty elements
    for list_element in review_list:
        if list_element.text == "":
            review_list.remove(list_element)

    exclude_words = ['QUALITY', 'DIFFICULTY', 'ENGL', 'ANY', 'ALL', 'HIST', 'HISTORY', 'VARIOUS']

    '''
        THIS GETS THE TEXT FROM EACH REVIEW, WILL ADD EACH COMMENT TO A DATAFRAME, AND WILL BE TAGGED WITH THE TEACHER CODE
    '''
    ############################################# CREATING DATAFRAMES #############################################
    for list_element in review_list:
        # add the comment to the comment_dataframe
        text = list_element.text.split('\n')

        tags = []
        review_string = ""

        # get stuf we know for sure
        quality = text[1]
        difficulty = text[3]
        class_name = text[4]
        date = text[5]

        # loop through the text to find the things we need
        for string in text:
            if len(string) > len(review_string):
                review_string = string
            # if the string contains "Textbook" store it to variable
            if "Textbook" in string:
                textbook = string
            else:
                textbook = ""
            # if the string contains "Attendance" store it to variable
            if "Attendance" in string:
                attendance = string
            else:
                attendance = ""
            # if the string contains "Grade" store it to variable
            if "Grade" in string:
                grade = string
            else:
                grade = ""
            # if the string contains "Would Take Again" store it to variable
            if "Would Take Again" in string:
                would_take_again = string
            else:
                would_take_again = ""
            # if the string is in all caps and does not contain numbers, and is not in the exclude_words list, add it to the tags list
            if string.isupper() and not any(char.isdigit() for char in string ) and not any(word in string for word in exclude_words):
                tags.append(string)
            # if the string contains "For Credit" store it to variable
            if "For Credit" in string:
                for_credit = string
            else:
                for_credit = ""

        debug.append(text)




        url = teacher_url.split("/")
        url = url[len(url) - 1]

        review_frame.loc[len(review_frame)] = [url, quality, difficulty, class_name,date,textbook,attendance,
                                                         grade,would_take_again,for_credit, tags, review_string] # add after daate
def process_teachers(data): # teachers, a list of teacher objects
    review_dataframes = pd.DataFrame(columns=['ID', 'Quality', 'Difficulty', 'Class_Name', 'Date_Taken', 'textbook',
                                              'attendence', 'grade', 'take_again', 'credit', 'Tags', 'Comment'])

    driver = make_driver()
    print("driver created, getting page")

    try:
        for index, row in data.iterrows():
            teacher = row['link']
            print("getting reviews for", teacher)
            try:
                get_teacher_reviews(teacher, review_dataframes ,driver)
            except Exception as e:
                print("error getting reviews for", teacher, e)
    finally:
        driver.close()
        review_dataframes.to_csv('./Data/review_dataframes.csv', index=False)
        return review_dataframes


if __name__ == '__main__':
    '''
        running the program
    '''
    teacher_ratings = get_university_teacher_list(1596)
    print(teacher_ratings.to_string())

    print("got teacher list ", len(teacher_ratings) , " gettting reviews")

    #review_list = process_teachers(teacher_ratings)

    '''
            THREADING
    '''
    # split the dataframe into n chunks
    n = 4
    chunks = np.array_split(teacher_ratings, n)

    threads = []
    for i in range(n):
        threads.append(threading.Thread(target=process_teachers, args=(chunks[i],)))

    # start the threads
    for thread in threads:
        thread.start()

    # wait for the threads to finish
    for thread in threads:
        thread.join()

    print("finished getting reviews")

    '''
        EXPORTING DATAFRAMES
    '''
    #print(review_list.to_string())

    teacher_ratings.to_csv('./Data/teacher_dataframes.csv', index=False)
    # rocess_teachers exports its own dataframe, beacause it is threaded
