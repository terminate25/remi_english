# -*- coding: utf-8 -*-
"""
Account Manage Module
"""
from django.db import IntegrityError, transaction
from default.logic.createcourselogic import *
from django.shortcuts import render
from default.config.config_menu import *
from default.logic.loglogic import *
from .authen import check_login
from helper.lagform import *
from django.http import JsonResponse


@check_login
@transaction.atomic(using=DatabaseRouter.data_database)
def create_course(request):

    """
    The function to render user view
    - Show user list
    - Create/Update/Delete the user information
    @param request:
    """

    logging_user = LoginUser.get_login_user()

    # For edit
    if request.method == "GET":

        lesson_id = request.GET.get("lesson_id")
        action_type = request.GET.get("action_type")
        if action_type == "1":
            result = CreateCourseLogic.edit_lesson(lesson_id)
            edit_form = LagForm()
            edit_form.set_form_name('create_course_form')
            edit_form.set_action('/create_course/')
            edit_form.set_title("Edit Course")
            edit_form.set_lesson_update(True)
            edit_form.set_lesson_update_data(result['lesson_list'])
            edit_form.set_test_update_data(result['test_list'])
            edit_form.set_question_update_data(result['question_list'])
            context = {
                'user': logging_user,
                'keuForm': edit_form,
                'screen_name': ScreenName.CreateCourse,
                'is_edit': 1,
                'lesson_id': lesson_id,
                # 'test_list': result["test_list"],
                'lesson_list': result["lesson_list"],
                'question_list': result["question_list"]
            }
            # ret = dict()
            # ret["test_info"] = result["test_list"]
            # ret["lesson_info"] = result["lesson_list"]
            return render(request, 'create_course.html', context)
            # return JsonResponse(ret, safe=False)

    #for get lesson and level option
    if request.method == "POST":
        params = request.POST
        ret = dict()
        is_level_select = params.get('is_level_select','')
        if is_level_select == 'true':
            course_id = params.get('course_select','')
            if course_id != '':
                course_id = int(params.get('course_select',''))
            else:
                course_id = 0
            level_select = list()
            level_object = Level.objects.filter(course_id=course_id)
            for i in range(0, level_object.count()):
                level_dict = dict()
                level_dict["id"] = level_object[i].id
                level_dict["name"] = level_object[i].name
                level_select.append(level_dict)
            ret['level_select'] = level_select
            return JsonResponse(ret, safe=False)
        is_lesson_select = params.get('is_lesson_select')
        if is_lesson_select == 'true':
            level_id = params.get('level_select', '')
            if level_id != '':
                level_id = int(params.get('level_select', ''))
            else:
                level_id = 0
            lesson_select = list()
            lesson_object = Lesson.objects.filter(level_id=level_id)
            for i in range(0, lesson_object.count()):
                lesson_dict = dict()
                lesson_dict["id"] = lesson_object[i].id
                lesson_dict["name"] = lesson_object[i].name
                lesson_select.append(lesson_dict)
            ret['lesson_select'] = lesson_select
            return JsonResponse(ret, safe=False)

    #for insert
    params = request.POST
    type_choose = params.get('type', '0')
    type_choose = int(type_choose)
    current_question = params.get('current_question', '')
    # current_question = Question.objects.last().id + 1

    file_list = params.get('file', '')

    # if current_question == 'None' or current_question == '':
    #     current_question = 0
    # else:
    #    current_question = int(current_question)
    auth_type = None
    type_form = GacoiForm("typeForm", "/create_course/", "POST")
    type_form.set_view("id,level,name,content,type")
    type_form.set_key("id")

    if logging_user.is_delete_right():
        type_form.set_option_deletable(True)

    keu_form = LagForm()
    keu_form.set_form_name('create_course_form')
    keu_form.set_action('/create_course/')
    keu_form.set_title("Course List")
    keu_form.set_test_id(1)


    create_current_state = 0
    is_add_question = params.get('is_add_question', '')
    add_test = params.get('add_test', '')
    is_finished = params.get('is_finished', '')

    if is_add_question == 'true':
        current_test_id = params.get('current_test', '')
        current_test_id = int(current_test_id)
        keu_form.set_test_id(current_test_id)
        #current_question = params.get('current_question', '')
        current_test_id = params.get('current_test', '')
        if current_test_id != '':
            current_test_id = int(current_test_id)
        if current_question != '':
            current_question = int(current_question)
        if add_test == 'true':
            ret = dict()
            keu_form.set_question_id(current_question)
            test_type = keu_form.render_test_type(current_test_id, type_choose)
            ret['current_test'] = current_test_id + 1
            ret['question_form'] = test_type
            return JsonResponse(ret, safe=False)
        else:
            ret = dict()
            question = None
            keu_form.set_question_id(current_question)
            question = keu_form.render_question_content(type_choose, current_question, current_test_id)
            # if type_choose == QuestionType.Type1.code:
            #     question = keu_form.render_question_content(type_choose, current_question, current_test_id)
            # elif type_choose == QuestionType.Type2.code:
            #     question = keu_form.render_question_content(type_choose, current_question, current_test_id)
            # elif type_choose == QuestionType.Type3.code:
            #     question = keu_form.render_question_content(type_choose, current_question, current_test_id)
            # elif type_choose == QuestionType.Type4.code:
            #     question = keu_form.render_question_content(type_choose, current_question, current_test_id)
            # elif type_choose == QuestionType.Type5.code:
            #     question = keu_form.render_question_content(type_choose, current_question, current_test_id)
            # elif type_choose == QuestionType.Type6.code:
            #     question = keu_form.render_question_content(type_choose, current_question, current_test_id)
            # elif type_choose == QuestionType.Type7.code:
            #     question = keu_form.render_question_content(type_choose, current_question, current_test_id)
            # elif type_choose == QuestionType.Type8.code:
            #     question = keu_form.render_question_content(type_choose, current_question, current_test_id)


            ret['question_form'] = question
            ret['current_question'] = 0
            return JsonResponse(ret, safe=False)
    if is_finished == 'true':
        result = CreateCourseLogic.store_lesson_data(request)
        ret = dict()
        ret['result'] = result
        message = "Submit Failed!"
        if result:
            message = "Submit successed!!"
        ret['message'] = message
        return JsonResponse(ret, safe=False)

    context = {
        'authType': auth_type,
        'user': logging_user,
        'typeForm': type_form,
        'keuForm': keu_form,
        'screen_name': ScreenName.CreateCourse,
        'create_current_state': create_current_state,
        'typechoose': type_choose,
        'current_question': current_question,
    }

    return render(request, 'create_course.html', context)


def list_course(request):
    context = {}
    params = request.POST

    return render(request, 'create_course.html', context)