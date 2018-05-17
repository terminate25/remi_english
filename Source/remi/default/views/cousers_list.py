# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from default.config.config_menu import ScreenName
from default.logic.user_logic import LoginUser
from default.views.authen import check_login
from default.logic.test_content_logic import (TestContentLogic,
                                              CourseListLogic)


@check_login
def courses_list(request):

    user = LoginUser.get_login_user(request)
    if request.method == 'POST':
        params = request.POST
    else:
        params = request.GET

    TestContentLogic.check_lesson_status(user.id)
    course_id = params.get('course_id', '')
    if course_id != '':
        course_id = int(course_id)
    levels = None
    courses = None
    if course_id != '':
        levels = CourseListLogic.get_course_content(user.id, course_id)
    else:
        user_courses_id = CourseListLogic.get_user_courses_ids(user.id)
        courses = CourseListLogic.get_user_courses_dict(user.id)

    context = {
        'user': user,
        'screen_name': ScreenName.Course,
        'levels': levels,
        'courses': courses,
    }

    return render(request, 'courses_list.html', context)
