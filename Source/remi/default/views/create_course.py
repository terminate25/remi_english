# -*- coding: utf-8 -*-
"""
Account Manage Module
"""
from django.db import IntegrityError, transaction
from default.logic.create_course_logic import *
from django.shortcuts import render
from default.config.config_menu import *
from default.logic.log_logic import *
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

    # For get lesson and level option
    if request.method == "POST":

        params = request.POST
        ret = dict()
        is_level_select = params.get('is_level_select','')
        if is_level_select == 'true':
            ret['is_error'] = "false"
            course_id = params.get('course_select','')
            if course_id != '':
                course_id = int(params.get('course_select',''))
            else:
                course_id = 0
            level_select = list()
            level_object = Level.objects.filter(course_id=course_id)
            if level_object.count() == 0:
                ret['is_error'] = "true"
                current_course_name = Course.objects.filter(
                    pk=course_id).first().name
                ret['message'] = 'Please create level for course "' + \
                                 current_course_name + '" in Master'
                #Add new remove course which not contain level
                # new_course_object = Course.objects.exclude(pk=course_id)
                # course_select = list()
                # for course_idx in range(0, new_course_object.count()):
                #     course_dict = dict()
                #     course_dict["id"] = new_course_object[course_idx].id
                #     course_dict["name"] = new_course_object[course_idx].name
                #     course_select.append(course_dict)
                # ret['new_course_list'] = course_select
            for i in range(0, level_object.count()):
                level_dict = dict()
                level_dict["id"] = level_object[i].id
                level_dict["name"] = level_object[i].name
                level_select.append(level_dict)
            ret['level_select'] = level_select
            return JsonResponse(ret, safe=False)
        is_lesson_select = params.get('is_lesson_select')
        if is_lesson_select == 'true':
            ret['is_error'] = "false"
            level_id = params.get('level_select', '')
            if level_id != '':
                level_id = int(params.get('level_select', ''))
            else:
                level_id = 0

            course_id = params.get('course_select', '')
            if course_id != '':
                course_id = int(course_id)
            else:
                course_id = 0

            lesson_select = list()
            lesson_object = Lesson.objects.filter(level_id=level_id)
            #Add new for validate
            if lesson_object.count() == 0:
                ret['is_error'] = "true"
                current_level_name = Level.objects\
                    .filter(pk=level_id).first().name
                current_course_name = Course.objects\
                    .filter(pk=course_id).first().name
                ret['message'] = 'Please create lesson for level "' \
                                 + current_level_name + '" , course "' \
                                 + current_course_name + '" in Master'
                # Add new remove level which not contain lesson
                new_level_object = Level.objects.exclude(pk=level_id)\
                    .filter(course_id=course_id)
                level_select = list()
                for level_idx in range(0, new_level_object.count()):
                    course_dict = dict()
                    course_dict["id"] = new_level_object[level_idx].id
                    course_dict["name"] = new_level_object[level_idx].name
                    level_select.append(course_dict)
                ret['new_level_list'] = level_select
            for i in range(0, lesson_object.count()):
                lesson_dict = dict()
                lesson_dict["id"] = lesson_object[i].id
                lesson_dict["name"] = lesson_object[i].name
                lesson_select.append(lesson_dict)
            ret['lesson_select'] = lesson_select
            return JsonResponse(ret, safe=False)

    # For insert
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
            question = keu_form.render_question_content(
                type_choose, current_question, current_test_id
            )
            # if type_choose == QuestionType.Type1.code:
            #     question = keu_form.render_question_content(
            # type_choose, current_question, current_test_id)
            # elif type_choose == QuestionType.Type2.code:
            #     question = keu_form.render_question_content(
            # type_choose, current_question, current_test_id)
            # elif type_choose == QuestionType.Type3.code:
            #     question = keu_form.render_question_content(
            # type_choose, current_question, current_test_id)
            # elif type_choose == QuestionType.Type4.code:
            #     question = keu_form.render_question_content(
            # type_choose, current_question, current_test_id)
            # elif type_choose == QuestionType.Type5.code:
            #     question = keu_form.render_question_content(
            # type_choose, current_question, current_test_id)
            # elif type_choose == QuestionType.Type6.code:
            #     question = keu_form.render_question_content(
            # type_choose, current_question, current_test_id)
            # elif type_choose == QuestionType.Type7.code:
            #     question = keu_form.render_question_content(
            # type_choose, current_question, current_test_id)
            # elif type_choose == QuestionType.Type8.code:
            #     question = keu_form.render_question_content(
            # type_choose, current_question, current_test_id)
            ret['question_form'] = question
            ret['current_question'] = 0
            return JsonResponse(ret, safe=False)
    if is_finished == 'true':
        result = CreateCourseLogic.store_lesson_data(request)
        ret = dict()
        ret['result'] = result
        message = "Submit Failed!"
        if result:
            message = "Submit success!!"
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
