# -*- coding: utf-8 -*-

from enum import Enum
"""
Define role and right of user
"""


class UserRightType(Enum):
    View = 1
    Update = 2
    Delete = 4
    Insert = 8
    All = 15


class RoleName(Enum):
    Admin = 1
    Student = 2
    Teacher = 3
    Manager = 4
    Other = 0


class ModuleName(Enum):
    User = 1
    CreateCourse = 2
    Test = 3
    Statistical = 4
    ListCourse = 5

    Master = 6
    ManagerStatistical = 7


"""
Define view belong to which module
"""
config_view_module_mapping = {
    "index": None,
    "user": ModuleName.User.value,
    "course_list": ModuleName.Test.value,
    "create_course": ModuleName.CreateCourse.value,
    "statistical": ModuleName.Statistical.value,
    "list_courses": ModuleName.ListCourse.value,
    "master": ModuleName.Master.value,
    "manage_statistical": ModuleName.ManagerStatistical.value,

}


"""
Define which module user can access
"""
config_roles = {
    ModuleName.User: {
        RoleName.Admin: {'right': UserRightType.All.value, 'filter':  None},

    },
    ModuleName.ListCourse: {
        RoleName.Admin: {'right': UserRightType.All.value, 'filter':  None},

    },
    ModuleName.Statistical: {
        RoleName.Admin: {'right': UserRightType.All.value, 'filter':  None},
        RoleName.Teacher: {'right': UserRightType.All.value, 'filter': None}

    },
    ModuleName.Master: {
        RoleName.Admin: {'right': UserRightType.All.value, 'filter':  None},
    },
    ModuleName.ManagerStatistical: {
        RoleName.Admin: {'right': UserRightType.All.value, 'filter':  None},
        RoleName.Manager: {'right': UserRightType.All.value, 'filter':  None},
    },


    ModuleName.CreateCourse: {
        RoleName.Admin: {'right': UserRightType.All.value, 'filter':  None},
    },

    ModuleName.Test: {
        RoleName.Admin: {'right': UserRightType.All.value, 'filter': None},
        RoleName.Student: {'right': UserRightType.All.value, 'filter': None},
        RoleName.Teacher: {'right': UserRightType.All.value, 'filter': None},

    },
}
