
# RMPSCRAPER.py

This module provides functions for scraping data from the RateMyProfessors website.

## Functions

### `get_university_teacher_list(university_id: str) -> None`

This function retrieves a list of teachers from a specific university based on the `university_id` provided. It uses the Selenium WebDriver to navigate to the university's page on the RateMyProfessors website, and then dumps the HTML to a file. The function takes a single parameter, `university_id`, which is a string representing the ID of the university to retrieve the teacher list for.

### `get_teacher_reviews(teacher: Teacher, driver) -> None`

This function retrieves the reviews for a specific teacher on the RateMyProfessors website. It uses the Selenium WebDriver to navigate to the teacher's page on the website, and then clicks the "Load More Ratings" button repeatedly until all reviews have been loaded. The function takes two parameters: `teacher`, which is a `Teacher` object representing the teacher to retrieve reviews for, and `driver`, which is a Selenium WebDriver instance.

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