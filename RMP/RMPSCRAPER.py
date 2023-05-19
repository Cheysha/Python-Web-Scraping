from selenium.webdriver.common.by import By
from selenium import webdriver
from teacher import Teacher

'''
    there are test conditions that cap at 3
'''


def get_university_teacher_list(university_id):
    '''
         THIS GETS THE LIST OF TEACHERS FROM THE UNIVERSITY PAGE, AND DUMPS THE HTML TO A FILE
    '''

    counter = 0
    option = webdriver.FirefoxOptions()
    option.add_argument("--headless")
    driver = webdriver.Firefox(options=option)

    driver.get(f"https://www.ratemyprofessors.com/search/teachers?query=*&sid={university_id}")
    #driver.implicitly_wait(500)
    ## HERE

    # the site spams a cookie warning, so we need to close it
    # find the div with "fyxlwo" in the class name
    buttons = driver.find_elements(By.TAG_NAME, "button")
    for button in buttons:
        if button.text == "Close":
            button.click()
            break

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
                if counter == 3:
                    break

                found_button = True  # Set the flag to indicate a matching button was found

        if not found_button:
            break  # Break out of the while loop if no matching button was found
    '''
    # write the page to file
    with open(f"{university_id}", "w", encoding="utf-8") as file:
        file.write(driver.page_source)
    '''

    # find every <a> that has "TeacherCard" in the class name
    a = driver.find_elements(By.TAG_NAME, "a")
    teacher_list = []

    for i in a:
        if "TeacherCard" in i.get_attribute("class"):
            print(i.get_attribute("href"))
            t = i.text.split("\n")

            teacher_list.append((i.get_attribute("href"), t))
            '''
             TESTING PURPOSES
            '''
            if(len(teacher_list) == 3):
                break


    tl = []

    for teacher in teacher_list:
        n = Teacher(code=teacher[0], name=teacher[1][3], school=teacher[1][5], department=teacher[1][4],
                    rating=teacher[1][1], difficulty=teacher[1][8], would_take_again=teacher[1][6])
        tl.append(n)
        #print(teacher)
        #print("\n")

    driver.close()
    return tl

def get_teacher_reviews(*args):
    option = webdriver.FirefoxOptions()
    option.add_argument("--headless")
    driver = webdriver.Firefox(options=option)


    for teacher in args[0]: # get the comments
        driver.get(teacher)

        #close the cookie warning
        buttons = driver.find_elements(By.TAG_NAME, "button")
        for button in buttons:
            if button.text == "Close":
                button.click()
                break

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

        r = driver.find_element(By.ID, "ratingsList")
        c = (r.find_elements(By.CSS_SELECTOR, "li"))


        for t in c:
            if t.text == "":
                c.remove(t)

        comments = []

        # for each entry in c, split the text by '/n' and then add it to the dict
        for entry in c:
            # split the text by '/n'
            text = entry.text.split('\n')
            # create a dict
            comment = {}
            # add the text to the dict
            comment['class'] = text[4]
            comment['date'] = text[7]
            comment['comment'] = text[8]
            comment['quality'] = text[1]
            comment['difficulty'] = text[3]
            comment['would_take_again'] = text[5]
            comment['grade'] = text[9]
            comment['tags'] = text[10]
            # add the dict to the list
            comments.append(comment)
            # probaly clean this up a bit

    driver.close()


if __name__ == '__main__':

    #test = 946
    #test_list = get_university_teacher_list(946)
    test_list = ("https://www.ratemyprofessors.com/professor/132940",
                "https://www.ratemyprofessors.com/professor/138265"
                "https://www.ratemyprofessors.com/professor/163241")

    get_teacher_reviews(test_list)
    breakpoint()

