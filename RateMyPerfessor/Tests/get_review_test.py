import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from ..teacherClass import Teacher
from ..RMPSCRAPER import get_teacher_reviews


class TestGetTeacherReviews(unittest.TestCase):


    def setUp(self):
        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.quit()

    def test_get_teacher_reviews(self):
        teacher = Teacher("John Doe","https://www.ratemyprofessors.com/professor/1275044")
        driver = self.driver
        get_teacher_reviews(teacher, driver)
        self.assertGreater(len(teacher.comments), 0)

if __name__ == '__main__':
    unittest.main()