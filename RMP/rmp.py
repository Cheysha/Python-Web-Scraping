#import requests
import bs4
#import selenium
from selenium.webdriver.common.by import By
from selenium import webdriver
#from selenium.webdriver.support.wait import WebDriverWait

'''
     THIS GETS THE LIST OF TEACHERS FROM THE UNIVERSITY PAGE, AND DUMPS THE HTML TO A FILE
'''

counter = 0

driver = webdriver.Firefox()
driver.get("https://www.ratemyprofessors.com/search/teachers?query=*&sid=946")
driver.implicitly_wait(500)

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
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'auto', block: 'center', inline: 'center'});",
                                  button)
            button.click()
            counter += 1
            print(counter)
            found_button = True  # Set the flag to indicate a matching button was found

    if not found_button:
        break  # Break out of the while loop if no matching button was found

#write the page to file
with open("RMP.html", "w", encoding="utf-8") as file:
    file.write(driver.page_source)


#  maybe once the page is fully populated, save to a file
#  then we can parse the file

