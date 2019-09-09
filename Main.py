class Assignment:
    def __init__(self, description, score, total):
        self.description = str(description)
        self.score = float(score)
        self.total = float(total)

    def getDescription(self) -> str:
        return self.description

    def getScore(self) -> float:
        return self.score

    def getTotal(self) -> float:
        return self.total

    def changeScore(self, score: float):
        self.score = score


class CategoryAssignment(Assignment):
    def __init__(self, description, category, score, total):
        super().__init__(description, score, total)  # need this for subclass of the parent class
        #         Assignment.__init__(self, description, score, total) ##Same as line 5
        self.category = category

    def getCategory(self) -> str:
        return self.category


class Student:
    def __init__(self, student_id: int):
        self.student_id = int(student_id)
        self.assignment_list = []  # accessed by the below functions

    def getId(self) -> int:
        return self.student_id

    def getScore(self, assignmentName: str) -> float:
        for assignment in self.assignment_list:
            if assignmentName in assignment.getDescription():
                return assignment.getScore()

    def getScores(self):
        return self.assignment_list

    def addAssignment(self, score: Assignment):  # Adding the Assignment, not the "score"
        self.assignment_list.append(score)

    def hasAssignment(self, description):  # I added this helper function
        for assignment in self.assignment_list:
            if assignment.getDescription() == description:
                return True
        return False

    def changeScore(self, assignmentName: str, score: float):
        for assignment in self.assignment_list:
            if assignmentName in assignment.getDescription():
                assignment.changeScore(score)

    def removeScore(self, assignmentName: str):
        for assignment in self.assignment_list:
            if assignmentName in assignment.getDescription():
                self.assignment_list.remove(assignment)


class Gradebook:
    def __init__(self):
        self.student_set = set()

    def displaySet(self):  # I added this helper function just to see, you do not really need this one
        return self.student_set

    def addStudent(self, student: Student):
        self.student_set.add(student)

    def dropStudent(self, id: int):
        for student in self.student_set.copy():
            if student.getId() == id:
                self.student_set.discard(student)

    def search(self, id: int) -> Student:
        for student in self.student_set:
            if student.getId() == id:
                return student

    def addAssignment(self, id: int, score: Assignment):  # Check
        for student in self.student_set:
            if student.getId() == id:
                if student.hasAssignment(score.getDescription()):
                    student.changeScore(score.getDescription(), score.getScore())
                else:
                    student.addAssignment(score)


class TotalPointsGradebook(Gradebook):
    def __init__(self):  # initialize
        super().__init__()

    def writeGradebookRecord(self, id: int, fileName: str):
        count = 0
        file_to_return = open(fileName, 'w')
        for student in self.student_set:
            if student.getId() == id:
                count += 1
                file_to_return.write(str(id) + '\n')
                points_earned = 0
                points_total = 0
                for assignment in student.getScores():
                    file_to_return.write(
                        assignment.getDescription() + '\n' + str(int(assignment.getScore())) + '/' + str(
                            int(assignment.getTotal())) + '\n')
                    points_earned += assignment.getScore()
                    points_total += assignment.getTotal()
            file_to_return.write('Total: ' + str(int(points_earned)) + '/' + str(int(points_total)) + '\n')
            file_to_return.write('Percentage: ' + str((points_earned / points_total) * 100))

    if count == 0:
        file_to_return.write("Student Not Found")
    file_to_return.close()


def classAverage(self):
    student_percentages = []
    for student in self.student_set.copy():
        points_earned = 0
        points_total = 0
        for assignment in student.getScores():
            points_earned += assignment.getScore()
            points_total += assignment.getTotal()
        student_percentages.append(points_earned / points_total)
    return (sum(student_percentages) / len(student_percentages)) * 100


class CategoryGradebook(Gradebook):
    def __init__(self):
        super().__init__()
        self.category_dict = {}

    def addCategory(self, description: str, weight: float):
        self.category_dict[description] = weight

    def isBalanced(self) -> bool:
        return sum(self.category_dict.values()) == 100

    def writeGradebookRecord(self, id: int, fileName: str):
        count = 0
        file_to_return = open(fileName, 'w')
        for student in self.student_set:
            if student.getId() == id:
                count += 1
                file_to_return.write(str(id) + '\n')
                for assignment in student.getScores():
                    file_to_return.write(assignment.getCategory() + ': ' + assignment.getDescription() + '\n' + str(
                        int(assignment.getScore())) + '/' + str(int(assignment.getTotal())) + '\n')

                for category, weight in self.category_dict.items():
                    category_points = 0
                    category_total = 0

                    for assignment in student.getScores():
                        if assignment.getCategory() == category:
                            category_points += assignment.getScore()
                            category_total += assignment.getTotal()
                    file_to_return.write(category + ': ' + str((category_points / category_total) * 100) + '\n')
                file_to_return.write('Percentage: ' + str(self.classAverage()))

        if count == 0:
            file_to_return.write("Student Not Found")
        file_to_return.close()

    def classAverage(self):
        class_percentages = []
        for student in self.student_set:
            stud_perf = []

            for category, weight in self.category_dict.items():
                category_points = 0
                category_total = 0

                for assignment in student.getScores():
                    if assignment.getCategory() == category:
                        category_points += assignment.getScore()
                        category_total += assignment.getTotal()

                stud_perf.append(weight * (category_points / category_total))

            class_percentages.append(sum(stud_perf))
        if len(class_percentages) == 0:
            return 0
        return sum(class_percentages) / len(class_percentages)


