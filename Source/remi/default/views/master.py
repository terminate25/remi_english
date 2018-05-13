# -*- coding: utf-8 -*-
from django.shortcuts import redirect, render
from helper.util import *
from helper.lagform import *
from default.views.authen import check_login
from default.config.config_menu import ScreenName
from default.config.config_role import ModuleName, UserRightType
from default.config.common_config import *
from default.logic.userlogic import *
from default.logic.testcontentlogic import *


@check_login
def master(request):

    # check view privilege
    logging_user = LoginUser.get_login_user(request)

    if request.method == 'POST':
        params = request.POST
    else:
        params = request.GET

    course_id = params.get('course_id', '')
    if course_id and course_id.isdigit():
        course_id = int(course_id)
    else:
        course_id = -1
    level_id = params.get('level_id', '')
    if level_id and level_id.isdigit():
        level_id = int(level_id)
    else:
        level_id = -1

    type_form = GacoiForm('master', '/master/', 'POST')
    keu_form = LagForm()
    keu_form.set_title("Master")
    type_form.set_view("id,name,order,updated_datetime")
    type_form.set_key("id")
    type_form.set_required('name, content')
    type_form.set_type('updated_datetime', GacoiFormFieldType.DateTime)
    # type_form.set_hidden('course_id', course_id)
    type_form.get_field('id').set_link('?course_id=[id]&tab_index=1')
    type_form.set_search('name, content')
    type_form.set_order('id,name, content,order,updated_datetime')
    type_form.set_update('name, content')
    type_form.set_insert('name, content')
    type_form.set_option_deletable(True)
    type_form.init(request)
    # data = Course.objects.all().values_list('id',flat=False)
    data = Course.objects.all()

    # Order
    if type_form.order_field:
        if type_form.order_type == 'desc':
            data = data.order_by("-" + type_form.order_field)
        else:
            data = data.order_by(type_form.order_field)

    # Search user_name,login_name
    search = type_form.get_field("name").get_search_value()
    if search is not None and search != '':
        data = data.filter(name__contains=search)

    type_form.set_form_data(data)
    # type_form.set_form_model(Course)
    type_form.set_caption(["id,name,order,updated_datetime",
                           "ID,Course Name,Order,Updated Datetime"])

    period_form = None
    fiscal_term = None
    if type_form.is_action(GacoiFormAction.DeleteDone):
        delete_course = Course.objects.get(pk=type_form.get_key_value("id"))
        delete_course.delete()

    elif type_form.is_action(GacoiFormAction.InsertDone):
        new_course = Course()
        new_course.name = type_form.get_field('name').get_value_blank2none()
        new_course.updated_datetime = datetime.datetime.today()
        new_course.created_datetime = datetime.datetime.today()
        course_orders = TestContentLogic.get_course_order()
        new_course_order = 1
        if len(course_orders) != 0:
            new_course_order = course_orders[len(course_orders)-1] + 1
        new_course.order = new_course_order
        new_course.save()
    elif type_form.is_action(GacoiFormAction.UpdateDone):
        update_course = Course.objects.get(pk=type_form.get_key_value("id"))
        update_course.name = type_form.get_field('name').get_value_blank2none()
        update_course.updated_datetime = datetime.datetime.today()
        update_course.save()

    tab_index = params.get("tab_index", '')
    tab_active1 = 'active'
    tab_active2 = ''
    tab_active3 = ''
    if tab_index == '1':
        tab_active2 = 'active'
        tab_active1 = ''
        tab_active3 = ''
    if tab_index == '2':
        tab_active2 = ''
        tab_active1 = ''
        tab_active3 = 'active'

    level_form = None
    if course_id > 0:
        try:
            fiscal_term = Course.objects.get(id=course_id)
        except ObjectDoesNotExist:
            fiscal_term = None
        level_form = GacoiForm('manage_statisticalxxx', '/master/', 'POST')
        level_form.set_view("id,name,order,updated_datetime")
        level_form.set_key("id")

        level_form.set_required('name')
        level_form.set_type('updated_datetime', GacoiFormFieldType.DateTime)
        level_form.set_type('created_datetime', GacoiFormFieldType.DateTime)
        level_form.set_hidden('course_id', course_id)
        level_form.get_field('id').set_link('?course_id={0}&level_id=[id]&tab_index=2'.format(course_id))
        level_form.set_search('name')
        level_form.set_order('id,user_name')
        level_form.set_update('name')
        level_form.set_insert('name')
        level_form.set_option_deletable(True)
        level_form.init(request)
        if level_form.is_action(GacoiFormAction.DeleteDone):
            delete_level = Level.objects.get(pk=level_form.get_key_value("id"))
            delete_level.delete()

        elif level_form.is_action(GacoiFormAction.InsertDone):
            new_level = Level()
            new_level.name = level_form.get_field('name').get_value_blank2none()
            new_level.updated_datetime = datetime.datetime.today()
            new_level.created_datetime = datetime.datetime.today()
            new_level.course = Course.objects.get(pk=course_id)
            level_orders = TestContentLogic.get_level_order(course_id)
            new_level_order = 1
            if len(level_orders) != 0:
                new_level_order = level_orders[len(level_orders) - 1] + 1
            new_level.order = new_level_order
            new_level.save()

        elif level_form.is_action(GacoiFormAction.UpdateDone):
            update_level = Level.objects.get(pk=level_form.get_key_value("id"))
            update_level.name = level_form.get_field('name').get_value_blank2none()
            update_level.updated_datetime = datetime.datetime.today()
            update_level.save()
        # data = Level.objects.filter(course_id=course_id).values_list('id',flat=False)
        data = Level.objects.filter(course_id=course_id)

        if level_form.order_field:
            if level_form.order_type == 'desc':
                data = data.order_by("-" + level_form.order_field)
            else:
                data = data.order_by(level_form.order_field)

                # Search user_name,login_name
        search = level_form.get_field("name").get_search_value()
        if search is not None and search != '':
            data = data.filter(name__contains=search)
        level_form.set_form_data(data)
        # level_form.set_form_model(Level)
        level_form.set_caption(["id,name,order,updated_datetime",
                               "ID,Level Name,Order,Updated Datetime"])

        level_form.set_form_data(data)
        tab_active2 = 'active'
        tab_active3 = ''
        tab_active1 = ''

    level = None
    lesson_form = None
    if level_id > 0:
        try:
            level = Level.objects.get(id=level_id)
        except ObjectDoesNotExist:
            level = None
        lesson_form = GacoiForm('manage_statisticalxx', '/master/', 'POST')
        lesson_form.set_view("id,name,order,updated_datetime")
        lesson_form.set_key("id")

        lesson_form.set_required('name')
        lesson_form.set_type('updated_datetime', GacoiFormFieldType.DateTime)
        lesson_form.set_type('created_datetime', GacoiFormFieldType.DateTime)

        lesson_form.set_hidden('level_id', level_id)
        lesson_form.set_hidden('course_id', course_id)
        lesson_form.set_search('name')
        lesson_form.set_order('id,user_name')
        lesson_form.set_update('name')
        lesson_form.set_insert('name')
        lesson_form.set_option_deletable(True)
        lesson_form.init(request)

        if lesson_form.is_action(GacoiFormAction.DeleteDone):
            delete_level = Lesson.objects.get(pk=lesson_form.get_key_value("id"))
            delete_level.delete()

        elif lesson_form.is_action(GacoiFormAction.InsertDone):
            new_lesson = Lesson()
            new_lesson.name = lesson_form.get_field('name').get_value_blank2none()
            new_lesson.updated_datetime = datetime.datetime.today()
            new_lesson.created_datetime = datetime.datetime.today()
            new_lesson.level = Level.objects.get(pk=level_id)

            level_orders = TestContentLogic.get_lesson_order(level_id)
            new_lesson_order = 1
            if len(level_orders) != 0:
                new_lesson_order = level_orders[len(level_orders) - 1] + 1
            new_lesson.order = new_lesson_order
            new_lesson.save()

        elif lesson_form.is_action(GacoiFormAction.UpdateDone):
            update_lesson = Lesson.objects.get(pk=lesson_form.get_key_value("id"))
            update_lesson.name = lesson_form.get_field('name').get_value_blank2none()
            update_lesson.updated_datetime = datetime.datetime.today()
            update_lesson.save()

        # data = Lesson.objects.filter(level_id=level_id).values_list('id',flat=False)
        data = Lesson.objects.filter(level_id=level_id)
        if lesson_form.order_field:
            if lesson_form.order_type == 'desc':
                data = data.order_by("-" + lesson_form.order_field)
            else:
                data = data.order_by(lesson_form.order_field)

                # Search user_name,login_name
        search = lesson_form.get_field("name").get_search_value()
        if search is not None and search != '':
            data = data.filter(name__contains=search)

        lesson_form.set_form_data(data)
        # lesson_form.set_form_model(Lesson)
        lesson_form.set_caption(["id,name,order,updated_datetime",
                               "ID,Lesson Name,Order,Updated Datetime"])

        lesson_form.set_form_data(data)
        tab_active2 = ''
        tab_active3 = 'active'
        tab_active1 = ''


    context = {
        'user': logging_user,
        'screen_name': ScreenName.Master,
        'fiscal_term': fiscal_term,
        'term_form': type_form,
        'period_form': level_form,
        'lesson_form': lesson_form,
        'level': level,
        'tab1': tab_active1,
        'tab2': tab_active2,
        'tab3': tab_active3,
    }

    return render(request, 'master.html', context)
