from enum import Enum


class CommonState(Enum):
    Success = (1, "Success")
    Locked = (3, "Locked")
    Unlocked = (2, "Unlocked")

    def __init__(self, code, title):
        self.code = code
        self.title = title


class BaseUserRowState(Enum):
    Unlock = (0, "Unlock")
    Passed = (1, "Passed")

    def __init__(self, code, title):
        self.code = code
        self.title = title


class MasterType(Enum):
    Master = (1, "Master")
    LessonLevel = (2, "Lesson level")
    QuestionType = (3, "Question type")
    Gender = (4, "Gender question")
    Roles = (5, "User roles")

    def __init__(self, code, title):
        self.code = code
        self.title = title


class UserRoles(Enum):
    Admin = (1, "Admin")
    Student = (2, "Student")
    Teacher = (3, "Teacher")

    def __init__(self, code, title):
        self.code = code
        self.title = title


class CourseActionState(Enum):
    Insert = (1, "Insert")
    Delete = (2, "Delete")
    Edit = (3, "Edit")

    def __init__(self, code, title):
        self.code = code
        self.title = title


class IsDone:
    Unlocked = 0
    Passed = 1

    def __init__(self, code, title):
        self.code = code
        self.title = title


class QuestionType(Enum):
    Type1 = (1, " Type 1")
    Type2 = (2, " Type 2")
    Type3 = (3, " Type 3")
    Type4 = (4, " Type 4")
    Type5 = (5, " Type 5")
    Type6 = (6, " Type 6")
    Type7 = (7, " Type 7")
    Type8 = (8, " Type 8")

    def __init__(self, code, title):
        self.code = code
        self.title = title


class LessonItemList:
    id = None
    title = None
    content = None
    percent = None
    state = None
    level = None

    def __init__(self, id, title, content, state, percent, level):
        self.id = id
        self.title = title
        self.content = content
        self.percent = percent
        self.state = state
        self.level = level


class CommonConfig:
    NumberOfAnswer = 4
    NumberAnswerOptions = [4, 6]


class CreateCourseStep(Enum):
    Step1 = (1, "Video - Course")
    Step2 = (2, "Create Summary")
    Step3 = (3, "Create Question")
    Step4 = (4, "Result")

    def __init__(self, code, title):
        self.code = code
        self.title = title


class CourseListField:
    Id = (1, "id")
    Name = (2, "name")
    Level = (3, "level")
    UpdateDate = (4, "update")

    def __init__(self, code, title):
        self.code = code
        self.title = title


class LevelType(Enum):
    Course = 1
    Level = 2
    Lesson = 3
    Part = 4
    Step = 5
