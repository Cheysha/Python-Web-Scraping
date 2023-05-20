from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait


from teacher import Teacher


def get_university_teacher_list(university_id):
    '''
         THIS GETS THE LIST OF TEACHERS FROM THE UNIVERSITY PAGE, AND DUMPS THE HTML TO A FILE
    '''

    counter = 0
    option = webdriver.EdgeOptions()
    option.add_argument("--headless")
    option.add_argument("log-level=3")
    option.add_argument("--disable-extensions")
    option.add_argument("--no-sandbox")
    driver = webdriver.Edge(options=option)

    print("driver created, getting page")

    driver.get(f"https://www.ratemyprofessors.com/search/teachers?query=*&sid={university_id}")

    print("got page")

    buttons = driver.find_elements(By.TAG_NAME, "button")
    for button in buttons:
        if button.text == "Close":
            button.click()
            break

    print("closed cookie warning")

    # after we do that, lets look for the "Show More" button
    # cant click because somthing obstructs it, need to scroll down, need to keep button in view

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
            if(len(teacher_list) == 3):
                break

    tl = [] # the return list with teacher objects
    for teacher in teacher_list:
        n = Teacher(code=teacher[0], name=teacher[1][3], school=teacher[1][5], department=teacher[1][4],
                    rating=teacher[1][1], difficulty=teacher[1][8], would_take_again=teacher[1][6])
        tl.append(n)

    driver.close()
    return tl

def get_teacher_reviews(teacher: Teacher):
    option = webdriver.FirefoxOptions()
    option.add_argument("--headless")
    option.add_argument("log-level=3")
    option.add_argument("--disable-extensions")
    option.add_argument("--no-sandbox")
    driver = webdriver.Firefox(options=option)

    print("driver created")
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
        # create a dict
        temp_comment = {'class': text[4], 'date': text[7], 'comment': text[8], 'quality': text[1],
                        'difficulty': text[3], 'would_take_again': text[5], 'grade': text[9], 'tags': text[10]}
        # add the dict to the list
        comments.append(temp_comment)
        # probaly clean this up a bit
        teacher.comments = comments
    
    driver.close()
    




if __name__ == '__main__':
    test_list = get_university_teacher_list(946)

    print("got teacher list ", len(test_list), " gettting reviews")


    #TODO: use a thread pool to get reviews for each teacher

    

    get_teacher_reviews(test_list[1])

    print("got reviews")


    for comment in test_list[1].comments:
        print(comment['comment'])




