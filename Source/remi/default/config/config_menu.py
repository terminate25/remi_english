# -*- coding: utf-8 -*-

from enum import Enum
from .config_role import RoleName


class ScreenName(Enum):
    """
    Screen name define
    """
    CreateCourse = 2
    Course = 3
    User = 4
    Statistical = 5
    Master = 6
    ManagerStastical = 7

"""
    Screen name and role name mapping
"""
config_menus_roles = {
    ScreenName.CreateCourse: [RoleName.Admin],
    ScreenName.User: [RoleName.Admin],
    ScreenName.Master: [RoleName.Admin],
    ScreenName.Course: [RoleName.Admin, RoleName.Teacher, RoleName.Student],
    ScreenName.Statistical: [RoleName.Admin, RoleName.Teacher],
    ScreenName.ManagerStastical: [RoleName.Admin, RoleName.Manager]

}


"""
Menu define
"""
config_menus = [
        {'icon': "fa-caret-right", "name": "Master", "url": "/master", "screen_name": ScreenName.Master},
        {'icon': "fa-caret-right", "name": "User", "url": "/user", "screen_name": ScreenName.User},
        {'icon': "fa-caret-right", "name": "Create course", "url": "/list_courses", "screen_name": ScreenName.CreateCourse},
        {'icon': "fa-caret-right", "name": "Statistical", "url": "/statistical", "screen_name": ScreenName.Statistical},
        {'icon': "fa-caret-right", "name": "Manager Stastical", "url": "/manage_statistical",
         "screen_name": ScreenName.ManagerStastical},
        {'icon': "fa-caret-right", "name": "Courses", "url": "/course_list", "screen_name": ScreenName.Course},
]
