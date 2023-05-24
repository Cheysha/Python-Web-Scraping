import unittest
from ..RMPSCRAPER import get_university_teacher_list

class TestGetUniversityTeacherList(unittest.TestCase):

    def test_get_university_teacher_list(self):
        university_id = "12345" # replace with a valid university ID
        teacher_list = get_university_teacher_list(university_id)

if __name__ == '__main__':
    unittest.main()