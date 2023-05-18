'''
    THIS IS THE CLASS A TEACHER IS INSTANTIATED FROM
    will contain, name, school, department, would_take_again, difficulty, rating, comments
'''

class Teacher:
    def __init__(self, code, name, school, department, would_take_again, difficulty, rating):
        self.name = name
        self.code = code
        self.school = school
        self.department = department
        self.would_take_again = would_take_again
        self.difficulty = difficulty
        self.rating = rating
        self.comments = []

    def __str__(self):
        return f"Name: {self.name}\nSchool: {self.school}\nDepartment: {self.department}\nWould Take Again: {self.would_take_again}\nDifficulty: {self.difficulty}\nRating: {self.rating}\nComments: {self.comments}\n"

    def __repr__(self):
        return f"Name: {self.name}\nSchool: {self.school}\nDepartment: {self.department}\nWould Take Again: {self.would_take_again}\nDifficulty: {self.difficulty}\nRating: {self.rating}\nComments: {self.comments}\n"