# RateMyPerfessor Scraper

This module provides functions for scraping data from the RateMyProfessors website.

the RateMyProfessors website. It uses the Selenium WebDriver to navigate to the teacher's page on the website, and then clicks the "Load More Ratings" button repeatedly until all reviews have been loaded. The function takes two parameters: `teacher`, which is a `Teacher` object representing the teacher to retrieve reviews for, and `driver`, which is a Selenium WebDriver instance.


it also ustilizes threading to speed up the process of scraping reviews, and to prevent the script from timing out.
## Usage

To use this module, you will need to have the Selenium WebDriver installed for your preferred browser (Firefox or Edge). You can then import the module and call the `get_university_teacher_list` and `get_teacher_reviews` functions as needed.

Example usage:

```python
from RMPSCRAPER import get_university_teacher_list, get_teacher_reviews

# Get the list of teachers for a specific university
get_university_teacher_list("12345")

# Create a list of Teacher objects
teachers = [...]

# Create a webdriver instance
option = webdriver.FirefoxOptions()
option.add_argument("--headless")
option.add_argument("log-level=3")
option.add_argument("--disable-extensions")
option.add_argument("--disable-gpu")
driver = webdriver.Firefox(options=option)

# Retrieve the reviews for each teacher in the list
for teacher in teachers:
    get_teacher_reviews(teacher, driver)

# Close the webdriver instance
driver.quit()
```

Note that you will need to replace the `university_id` and `teachers` variables with appropriate values for your use case. Additionally, you may need to modify the `option` variable to use the appropriate browser and options for your system.