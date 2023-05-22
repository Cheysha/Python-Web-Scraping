# RateMyPerfessor Scraper

This module provides functions for scraping data from the RateMyProfessors website.

the RateMyProfessors website. It uses the Selenium WebDriver to navigate to the teacher's page on the website, and then clicks the "Load More Ratings" button repeatedly until all reviews have been loaded. The function takes two parameters: `teacher`, which is a `Teacher` object representing the teacher to retrieve reviews for, and `driver`, which is a Selenium WebDriver instance.


it also ustilizes threading to speed up the process of scraping reviews, and to prevent the script from timing out.
## Usage

To use this module, you will need to have the Selenium WebDriver installed for your preferred browser (Firefox or Edge). You can then import the module and call the `get_university_teacher_list` and `get_teacher_reviews` functions as needed.

Example usage:

script comes loaded with a test school id, running script will get all teachers associated with that school, and then gett all of the teacher reveiws
