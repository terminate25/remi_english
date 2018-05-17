# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import JsonResponse

from default.config.config_menu import ScreenName
from default.logic.user_logic import LoginUser
from default.views.authen import check_login
from helper.lagform import *
from default.logic.course_list_logic import *
from default.logic.test_content_logic import *

checkbox_values = []
his_info_id = None


@check_login
def courses(request):
    """
    Global variable:
        1. checkbox_values: used to store source meta_type records
        2. his_info_id: load info_form after merging
    Create form:
        1. type_form [main_tab]: meta_type table
        2. info_form [detail_tab]: meta_info table
        3. merge_form: merging meta_type
    Form action:
        1. Insert/Update/Delete: using QuerySet
        2. Merge: using QuerySet
    Return:
        Context format (JSON)
    @param request:
    @return:
    """

    user = LoginUser.get_login_user(request)

    if request.method == 'POST':
        params = request.POST
    else:
        params = request.GET

    meta_type_id = params.get('meta_type_id', '')

    course_video = 'https://www.youtube.com/embed/m6TXPNybrmk'
    course_title = 'Kodaline - Brother'
    keu_form = LagForm()
    keu_form.set_image_course(course_video, course_title)

    is_json = params.get("is_json", '')
    current_lesson = params.get("current_lesson", '')
    next_question = params.get("next_question", '')
    correct_question = params.get("correct_question", '')
    state = params.get("state", '')
    # total_question = 11 Helper.get_total_question(current_lesson)
    total_question = 11
    if is_json == "true":
        ret = dict()
        if int(next_question) > total_question:
            if int(state) == 1:
                correct_question = str(int(correct_question) + 1)
            ret['error'] = True
            if int(correct_question) < 1:
                question = 'question'
            else:
                question = 'questions'
            ret['error_message'] = "You are correct {0}/{1} {2}! "\
                .format(correct_question, total_question, question)
            return JsonResponse(ret, safe=False)

        ret = dict()
        ret['error'] = False
        ret['error_message'] = "a hihi"
        if int(state) == 1:
            ret['correct_question'] = int(correct_question) + 1
        else:
            ret['correct_question'] = int(correct_question)

        # ret['images'] = Helper.create_image_urls(current_lesson, next_question, 6)
        # ret['audio_url'] = Helper.create_audio_url(current_lesson, next_question)
        ret['current_lesson'] = int(current_lesson)
        ret['next_question'] = int(next_question) + 1
        return JsonResponse(ret, safe=False)

    part = int(params.get("part", ""))
    video_done = params.get("video_done", "")
    if video_done == "true":
        base_user_part = BaseUserPart.objects.get(Q(part=part) & Q(user_id=user.id))
        base_user_part.video = TestResult.Done.code
        base_user_part.save()
        TestContentLogic.check_lesson_status(user.id, part)

    part_content_dict = CourseListLogic.get_part_content_dict(part, user.id)
    lesson_id = Part.objects.get(pk=part).lesson_id
    level_id = Lesson.objects.get(pk=lesson_id).level_id
    course_id = Level.objects.get(pk=level_id).course_id

    context = {
        'user': user,
        'current_lesson': 1,
        'next_question': 1,
        'correct_question': 0,
        'keu_form': keu_form,
        'screen_name': ScreenName.Course,
        'total_question': total_question,
        'lesson_contents': part_content_dict,
        'course_id': course_id,
    }
    return render(request, 'courses.html', context)
