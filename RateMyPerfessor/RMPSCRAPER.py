from selenium.webdriver.common.by import By
from selenium import webdriver
import threading
from teacherClass import Teacher

def get_university_teacher_list(university_id):
    '''
         THIS GETS THE LIST OF TEACHERS FROM THE UNIVERSITY PAGE, AND DUMPS THE HTML TO A FILE
    '''

    counter = 0
    '''
    option = webdriver.EdgeOptions()
    option.add_argument("--headless")
    option.add_argument("log-level=3")
    option.add_argument("--disable-extensions")
    option.add_argument("--no-sandbox")
    option.add_argument("--disable-gpu")
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

    driver.get(f"https://www.ratemyprofessors.com/search/teachers?query=*&sid={university_id}")

    print("got page")

    buttons = driver.find_elements(By.TAG_NAME, "button")
    for button in buttons:
        if button.text == "Close":
            button.click()
            break

    print("closed cookie warning")

    while True:
        buttons = driver.find_elements(By.TAG_NAME, "button")
        found_button = False  # Flag to track if a matching button was found

        for button in buttons:
            if button.text == "Show More":
                # scroll so button is at center of screen
                driver.execute_script(
                    "arguments[0].scrollIntoView({behavior: 'auto', block: 'center', inline: 'center'});",
                    button)
                button.click()
                counter += 1
                print(counter)
                '''
                                        TESTING PURPOSES
                '''
                if counter == 1:
                    break

                found_button = True  # Set the flag to indicate a matching button was found
        if not found_button:
            break  # Break out of the while loop if no matching button was found

    print("finished loading page")

    # find every <a> that has "TeacherCard" in the class name
    a_elements = driver.find_elements(By.TAG_NAME, "a")
    teacher_list = []

    for teacher_element in a_elements:
        if "TeacherCard" in teacher_element.get_attribute("class"):
            print(teacher_element.get_attribute("href"))

            t = teacher_element.text.split("\n")
            teacher_list.append((teacher_element.get_attribute("href"), t))
            '''
             TESTING PURPOSES
            '''
            if(len(teacher_list) == 6):
                break

    tl = [] # the return list with teacher objects
    for teacher in teacher_list:
        n = Teacher(code=teacher[0], name=teacher[1][3], school=teacher[1][5], department=teacher[1][4],
                    rating=teacher[1][1], difficulty=teacher[1][8], would_take_again=teacher[1][6])
        tl.append(n)

    driver.close()
    return tl

def get_teacher_reviews(teacher: Teacher, driver):

    print("getting page for", teacher.code)

    driver.get(teacher.code)

    print("got page for", teacher.code)

    #close the cookie warning
    buttons = driver.find_elements(By.TAG_NAME, "button")
    for button in buttons:
        if button.text == "Close":
            button.click()
            break

    print("closed cookie warning")

    # find the "Load More Ratings" button, click it until it stops appearing
    while True:
        buttons = driver.find_elements(By.TAG_NAME, "button")
        found_button = False  # Flag to track if a matching button was found

        for button in buttons:
            if button.text == "Load More Ratings":
                # scroll so button is at center of screen
                driver.execute_script(
                    "arguments[0].scrollIntoView({behavior: 'auto', block: 'center', inline: 'center'});",
                    button)
                button.click()
                found_button = True  # Set the flag to indicate a matching button was found

        if not found_button:
            break  # Break out of the while loop if no matching button was found

    print("finished hitting load more ratings")

    ratings_element = driver.find_element(By.ID, "ratingsList")
    review_list = (ratings_element.find_elements(By.CSS_SELECTOR, "li"))

    # remove empty elements
    for list_element in review_list:
        if list_element.text == "":
            review_list.remove(list_element)

    comments = []

    # for each list_element in review_list, split the text by '/n' and then add it to the dict
    for list_element in review_list:
        # split the text by '/n'
        text = list_element.text.split('\n')
        # create a dict, may need to rework this
        # try catch
        try:
            temp_comment = {'class': text[4], 'date': text[7], 'comment': text[8], 'quality': text[1],
                            'difficulty': text[3], 'would_take_again': text[5], 'grade': text[9], 'tags': text[10]}
        except IndexError:
            temp_comment = {}
        # add the dict to the list
        comments.append(temp_comment)
        # probaly clean this up a bit
    teacher.comments = comments
    
    #driver.close()

def process_teachers(teachers): # teachers, a list of teacher objects
    '''
    option = webdriver.EdgeOptions()
    option.add_argument("--headless")
    option.add_argument("log-level=3")
    option.add_argument("--disable-extensions")
    option.add_argument("--no-sandbox")
    option.add_argument("--disable-gpu")
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

    try:
        for teacher in teachers:
            reviews = get_teacher_reviews(teacher, driver)
            # Do something with the reviews, such as write them to a file
    finally:
        driver.quit()



if __name__ == '__main__':
    # this is working correctly i think, somtimes the page hangs and throws things off tho
    test_list = get_university_teacher_list(1596)

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
