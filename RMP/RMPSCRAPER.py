from selenium.webdriver.common.by import By
from selenium import webdriver

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
                found_button = True  # Set the flag to indicate a matching button was found

        if not found_button:
            break  # Break out of the while loop if no matching button was found

    # write the page to file
    with open(f"{university_id}", "w", encoding="utf-8") as file:
        file.write(driver.page_source)


if __name__ == '__main__':
    pass
