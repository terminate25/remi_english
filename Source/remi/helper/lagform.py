from helper.util import *
from default.config.common_config import *
from default.models.models import *
from enum import Enum
from django.conf import settings
from django.http import JsonResponse
import  json

import base64
import glob
import os
# import png
class FormType(Enum):
    StudentCourseList = 0
    CreateCourseList = 1
    CreateCourse = 2

class FieldType(Enum):
    TextArea = 0
    Select = 1

class CourseListField(Enum):
    Id = (1, "id")
    Name = (1, "name")
    Level = (2, "level")
    UpdateDate = (3, "update")
    LevelName = (5, "level_name")
    Order = (6,"lesson_order")
    TestNumber = (7,"test_number")

    def __init__(self, code, title):
        self.code = code
        self.title = title

class LagForm:
    # For lesson update
    lesson_update = None
    lesson_update_data = None
    test_update_data = None
    question_update_data = None
    # khac
    submit_success = False
    course_video = None
    course_title = None
    title = None
    fields = []
    sorting_fields = []
    action = None
    form_name = None
    create_course_step = None
    question_id = 0
    # lesson_id = None
    form_type = None
    test_id = None
    list_data = None

    def set_lesson_update(self, data):
        self.lesson_update = data
    def get_lesson_update(self):
        return self.lesson_update

    def set_lesson_update_data(self, data):
        self.lesson_update_data = data

    def get_lesson_update_data(self):
        return self.lesson_update_data

    def set_test_update_data(self, data):
        self.test_update_data = data

    def get_test_update_data(self):
        return self.test_update_data

    def set_question_update_data(self, data):
        self.question_update_data = data

    def get_question_update_data(self):
        return self.question_update_data

    def set_list_course(self, data):
        self.list_data = data

    def get_list_course(self):
        return self.list_data

    def set_test_id(self, test_id):
        self.test_id = test_id

    def get_test_id(self):
        return self.test_id

    def set_action(self, action):
        self.action = action

    def get_action(self):
        return self.action

    def set_content_type(self, form_type):
        self.form_type = form_type

    def get_content_type(self):
        return self.content_type

    def set_form_name(self, form_name):
        self.form_name = form_name



    def __init__(self):
        print("init success xxxxxxxxx")

    # def set_create_course_step(self, current_step):
    #     self.create_course_step = current_step

    # def get_create_course_step(self):
    #     return self.create_course_step

    # def set_lesson_id(self, lesson_id):
    #     self.lesson_id = lesson_id
    #
    # def get_lesson_id(self):
    #     return self.lesson_id

    def set_field_title(self, field_titles):
        fields = []
        for title in field_titles:
            sort = False
            if title in self.sorting_fields:
                sort = True
            field = LagField(title, sort)
            fields.append(field)

    def set_sort_fields(self, sort_fields):
        self.sorting_fields = sort_fields

    def set_image_course(self, course_video, course_title):
        print("init")
        self.course_title = course_title
        self.course_video = course_video

    def set_title(self, title):
        self.title = title

    # Render header view
    def render_grid_content(self):
        sb = StringBuilder()
        return sb

    def set_question_id(self, question_id):
        self.question_id = question_id

    def is_create_course_submit_success(self):
        return self.submit_success

    def set_create_course_submit_success(self, state):
        self.submit_success = state

    def get_current_question(self):
        return self.question_id

    @staticmethod
    def render_list_question():
        sb = StringBuilder()
        return sb

    def render_title(self):
        sb = StringBuilder()
        sb.append('<h3 class ="header smaller lighter blue"> {0} </h3>'.format(self.title))
        return sb


    def render_content(self):
        if self.form_type == FormType.CreateCourseList:
            return self.render_create_course_list()
        if self.form_type == FormType.CreateCourse:
            return self.render_create_course_content()

    def render_end_form(self):
        sb = StringBuilder()
        sb.append('</form>')
        return sb

    def render_course_list(self):
        sb = StringBuilder()
        rowtmp = ''
        rowtmp += '<div id="list-form">'
        rowtmp += '<table id="dynamic-table" class="table table-striped table-bordered table-hover dataTable no-footer" role="grid" aria-describedby="dynamic-table_info">'
        rowtmp += '<thead>'
        rowtmp += '<tr role="row">'
        rowtmp += '     <th class="sorting center" tabindex="0" aria-controls="dynamic-table" rowspan="1" colspan="1" aria-label="Domain: activate to sort column ascending">Part</th>'
        rowtmp += '     <th class="sorting center" tabindex="0" aria-controls="dynamic-table" rowspan="1" colspan="1" aria-label="Domain: activate to sort column ascending">Name</th>'
        rowtmp += '     <th class="sorting center" tabindex="0" aria-controls="dynamic-table" rowspan="1" colspan="1" aria-label="Price: activate to sort column ascending">Lesson</th>'
        rowtmp += '     <th class="sorting center" tabindex="0" aria-controls="dynamic-table" rowspan="1" colspan="1" aria-label="Price: activate to sort column ascending">Order</th>'
        rowtmp += '     <th class="sorting center" tabindex="0" aria-controls="dynamic-table" rowspan="1" colspan="1" aria-label="Price: activate to sort column ascending">Test Number</th>'

        rowtmp += '     <th class="sorting center" tabindex="0" aria-controls="dynamic-table" rowspan="1" colspan="1" aria-label="Update: activate to sort column ascending">'
        rowtmp += '         <i class="ace-icon fa fa-clock-o bigger-110 hidden-480"></i>Update</th>'
        rowtmp += '     <th class="sorting_disabled" rowspan="1" colspan="1" aria-label=""></th>'

        rowtmp += '</tr>'
        rowtmp += '</thead>'
        rowtmp += '<tbody>'
        for i in range(0, len(self.get_list_course())):
            rowtmp += '<tr role="row" class="odd">'
            # rowtmp += '<td class="center"><label class="pos-rel"><input type="checkbox" class="ace"><span class="lbl"></span></label></td>'
            rowtmp += '<input type = "hidden" id = "lesson_id" name = "lesson_id" value = "{0}">'.format(self.list_data[i][CourseListField.Id.title])
            rowtmp += '<td class="center" style="width: 100px;">{0}</td>'.format(i+1)
            rowtmp += '<td class="left">{0}</td>'.format(self.list_data[i][CourseListField.Name.title])
            rowtmp += '<td>{0}</td>'.format(self.list_data[i][CourseListField.LevelName.title])
            rowtmp += '<td class="center">{0}</td>'.format(self.list_data[i][CourseListField.Order.title])
            rowtmp += '<td class="center">{0}</td>'.format(self.list_data[i][CourseListField.TestNumber.title])
            rowtmp += '<td> {0} </td>'.format(self.list_data[i][CourseListField.UpdateDate.title])
            # rowtmp += '<td class=""><span class="label label-sm label-warning">Expiring</span></td>'
            rowtmp += '<td>'
            rowtmp += '   <div class="hidden-sm hidden-xs action-buttons">'
            # rowtmp += '        <a class="green" href="/create_course/state={0}&id={1}">'.format(CourseActionState.Edit.code, 2)
            rowtmp += '        <a class="green" href="/create_course/?lesson_id={0}&action_type={1}">'.format(self.list_data[i][CourseListField.Id.title], 1)
            rowtmp += '            <i class="ace-icon fa fa-pencil bigger-130"></i>'
            rowtmp += '       </a>'
            rowtmp += '        <a class="red" onclick="DeleteLesson({0})">'.format(self.list_data[i][CourseListField.Id.title])
            rowtmp += '            <i class="ace-icon fa fa-trash-o bigger-130"></i>'
            rowtmp += '        </a>'
            rowtmp += '    </div>'
            rowtmp += '   <div class="hidden-md hidden-lg">'
            rowtmp += '        <div class="inline pos-rel">'
            rowtmp += '            <button class="btn btn-minier btn-yellow dropdown-toggle" data-toggle="dropdown" data-position="auto">'
            rowtmp += '               <i class="ace-icon fa fa-caret-down icon-only bigger-120"></i>'
            rowtmp += '           </button>'
            rowtmp += '           <ul class="dropdown-menu dropdown-only-icon dropdown-yellow dropdown-menu-right dropdown-caret dropdown-close">'
            rowtmp += '               <li>'
            rowtmp += '                    <a class="tooltip-success" data-rel="tooltip" title="" data-original-title="Edit" onclick="GotoEdit(this, {0})">'.format(self.list_data[i][CourseListField.Id.title])
            rowtmp += '                       <span class="green">'
            rowtmp += '                           <i class="ace-icon fa fa-pencil-square-o bigger-120"></i>'
            rowtmp += '                        </span>'
            rowtmp += '                    </a>'
            rowtmp += '                </li>'
            rowtmp += '                 <li>'
            rowtmp += '                    <a  class="tooltip-error" data-rel="tooltip" title="" onclick="DeleteLesson({0})" ' \
                      'data-original-title="Delete" >'.format(self.list_data[i][CourseListField.Id.title])
            rowtmp += '                        <span class="red">'
            rowtmp += '                            <i class="ace-icon fa fa-trash-o bigger-120"></i>'
            rowtmp += '                        </span>'
            rowtmp += '                    </a>'
            rowtmp += '                </li>'
            rowtmp += '           </ul>'
            rowtmp += '        </div>'
            rowtmp += '    </div>'
            rowtmp += '</td>'
            rowtmp += '</tr>'
        rowtmp += '</tbody>'
        rowtmp += '</table>'
        rowtmp += '<button class ="btn btn-success btn-next" style="float:right;" type="button" onclick="GotoCreate()"> Insert'
        rowtmp += '</button>'
        rowtmp += '</div>'
        sb.append(rowtmp)
        return sb.__str__()


    def render_start_form(self):
        sb = StringBuilder()
        sb.append("<form enctype='multipart/form-data' method = 'POST' id='{0}' action='{1}' class ='form-horizontal'>\n"
                  .format(self.form_name, self.action))
        return sb.__str__()

    def render_create_course_content(self):
        sb = StringBuilder()
        sb.append('<div class ="widget-box" >\n')
        sb.append('   <div class ="widget-header widget-header-blue widget-header-flat">\n')
        sb.append('      <h4 class ="widget-title lighter" > Create New Course </h4>\n')
        sb.append('   </div>\n')
        sb.append('   <div class ="widget-body">\n')
        sb.append('      <div class ="widget-main"> \n')
        sb.append('          <div id = "fuelux-wizard-container" class ="no-steps-container">\n')
        sb.append('             <div>\n')
        sb.append('                  <ul class="steps" style="margin-left: 0">')
        sb.append('                   <li data-step="1" class="active">')
        sb.append('                        <span class="step">1</span>')
        sb.append('                        <span class="title">Video - Course </span>')
        sb.append('                    </li>')

        sb.append('                   <li data-step="2">')
        sb.append('                       <span class="step">2</span>')
        sb.append('                        <span class="title">Create Summary</span>')
        sb.append('                    </li>')

        sb.append('                    <li data-step="3">')
        sb.append('                        <span class="step">3</span>')
        sb.append('                       <span class="title">Create Questions</span>')
        sb.append('                   </li>')
        sb.append('                </ul>')
        sb.append('             </div>\n')
        sb.append('             <hr>\n')

        if self.get_lesson_update() is not None:
            sb.append(self.render_update_course_step())
        else:
            sb.append(self.render_create_course_step())
        return sb.__str__()
    def render_create_course_step(self):
        sb = StringBuilder()
        sb.append('<div class ="step-content pos-rel">\n')
        # step_1
        sb.append('<div class="step-pane active" data-step="1">')
        sb.append('        <div>')
        sb.append('            <h4 class="widget-title blue smaller">')
        sb.append('			    <i class="ace-icon fa glyphicon-asterisk orange"></i>Please select the course video.')
        sb.append('             </h4>')
        sb.append('             <div class="col-xs-12" id="import-video-form-id">')
        sb.append('                 <label class="ace-file-input">')
        sb.append('                     <input class="course-video" type="file" id="id-input-file-2">')
        sb.append('                 </label>')
        sb.append('             </div>')
        sb.append('         <hr><hr>')
        sb.append('         </div>')

        #select course
        sb.append('         <div>')
        sb.append('             <h4 class="widget-title blue smaller">')
        sb.append('             <i class="ace-icon fa glyphicon-asterisk orange"></i>Select Courses')
        sb.append('             </h4>')
        sb.append('             <select class="form-control course-select">')
        courses = Course.objects.filter()
        for course in courses:
            sb.append('<option value = "{0}" > {1} </option>\n'.format(course.id, course.name))
        sb.append('             </select>')
        sb.append('             <hr>')
        sb.append('         </div>')
        #level
        sb.append('         <div>')
        sb.append('             <h4 class="widget-title blue smaller">')
        sb.append('             <i class="ace-icon fa glyphicon-asterisk orange"></i>Select Levels')
        sb.append('             </h4>')
        sb.append('             <select class="form-control level-select">')
        first_course_id = Course.objects.first().id
        levels = Level.objects.filter(course_id=first_course_id)
        for level in levels:
            sb.append('<option value = "{0}" > {1} </option>\n'.format(level.id, level.name))
        sb.append('             </select>')
        sb.append('             <hr>')
        sb.append('         </div>')
        #select lesson
        sb.append('         <div>')
        sb.append('             <h4 class="widget-title blue smaller">')
        sb.append('             <i class="ace-icon fa glyphicon-asterisk orange"></i>Select Lessons')
        sb.append('             </h4>')
        sb.append('             <select class="form-control lesson-select">')
        first_level_id = levels[0].id

        lessons = Lesson.objects.filter(level_id=first_level_id)
        for lesson in lessons:
            sb.append('<option value = "{0}" > {1} </option>\n'.format(lesson.id, lesson.name))

        sb.append('             </select>')
        sb.append('             <hr>')
        sb.append('         </div>')

        #TO DO course, level, lesson, part

        sb.append('</div>')

        # step2
        sb.append('<div class="step-pane" data-step="2">')
        sb.append('        <div>')
        sb.append('            <h4 class="widget-title blue smaller">')
        sb.append('			    <i class="ace-icon fa glyphicon-asterisk orange"></i>Please select the lesson summary')
        sb.append('             </h4>')
        sb.append('             <div class="col-xs-12" id="import-video-form-id">')
        sb.append('                 <label class="ace-file-input">')
        sb.append('                     <input class="lesson-summary" type="file" id="id-input-file-2">')
        sb.append('                 </label>')
        sb.append('             </div>')
        sb.append('         <hr><hr>')
        sb.append('         </div>')
        sb.append('         <div>')
        sb.append('             <h4 class="widget-title blue smaller">')
        sb.append('             <i class="ace-icon fa glyphicon-asterisk orange"></i>Lesson title</h4>')
        sb.append('             </h4>')
        sb.append('             <textarea class="form-control limited lesson-title" id="form-lesson-title" placeholder="Lesson title" ></textarea>')
        sb.append('         </div>')
        sb.append('         <hr>')
        sb.append('         <div>')
        sb.append('             <h4 class="widget-title blue smaller">')
        sb.append('             <i class="ace-icon fa glyphicon-asterisk orange"></i>Lesson content</h4>')
        sb.append('             </h4>')
        sb.append('             <textarea class="form-control limited lesson-content" id="form-lesson-content" placeholder="Lesson content" ></textarea>')
        sb.append('         </div>')
        sb.append('</div>')

        # step3
        sb.append('<div class="step-pane" data-step="3">')
        # sb.append('<input type = "hidden"  id = "finish_selected" name = "finish_selected" value = "1">\n')
        sb.append('<input type = "hidden"  id = "current_question" name = "current_question" value = "{0}">\n'.format(self.get_current_question()))
        sb.append('<input type = "hidden"  id = "current_test" name = "current_test" value = "{0}">\n'.format(
            self.get_test_id()))

        sb.append('     <div id="question-form">')
        #test and question

        sb.append('<div>\n')
        sb.append('<h4 class ="widget-title blue smaller" >\n')
        sb.append('<i class ="ace-icon fa glyphicon-asterisk orange" > </i> Select question types\n')
        sb.append('</h4>\n')
        sb.append('<select class ="form-control question-type" id="question_type" name="question-type-name" >\n')
        question_types = Master.objects.filter(mastertype=MasterType.QuestionType.code)
        for question_type in question_types:
            sb.append('<option value = "{0}" > {1} </option>\n'.format(question_type.master_id, question_type.name))
        sb.append('</select>\n')
        sb.append('</div>\n')
        sb.append('<hr>\n')
        sb.append('</div>\n')
        sb.append('<hr>\n')
        sb.append('<div class ="wizard-actions" >\n')
        sb.append('<button type = "button" class ="btn btn-success" onclick="AddTest()" > Add Test\n')
        sb.append('<i class ="ace-icon fa fa-arrow-right icon-on-right" > </i>\n')
        sb.append('</button>\n')

        sb.append('     </div>')
        sb.append('</div>')

        # step4
        # sb.append('<div class="step-pane" data-step="4">')
        # sb.append('     <div class="center">')
        # sb.append('         <h3 class="green">Pl</h3>Please press fin')
        # sb.append('     </div>')
        # sb.append('</div>')
        sb.append('</div>')
        sb.append('</div>')
        sb.append('<hr>')

        return sb.__str__()
    def render_update_course_step(self):
        sb = StringBuilder()
        lesson_update_data = self.get_lesson_update_data()
        test_update_data = self.get_test_update_data()
        sb.append('<div class ="step-content pos-rel">\n')
        # step_1
        sb.append('<div class="step-pane active" data-step="1">')
        sb.append('        <div>')
        sb.append('            <h4 class="widget-title blue smaller">')
        sb.append('			    <i class="ace-icon fa glyphicon-asterisk orange"></i>Please select the course video.')
        sb.append('             </h4>')
        sb.append('             <div class="col-xs-12" id="import-video-form-id">')
        sb.append('                 <label class="ace-file-input">')
        sb.append('                     <input class="course-video" type="file" id="id-input-file-2">')
        sb.append('                 </label>')
        sb.append('             </div>')
        sb.append('         <hr><hr>')
        sb.append('         </div>')

        # select course
        sb.append('         <div>')
        sb.append('             <h4 class="widget-title blue smaller">')
        sb.append('             <i class="ace-icon fa glyphicon-asterisk orange"></i>Select Courses')
        sb.append('             </h4>')
        sb.append('             <select class="form-control course-select">')
        courses = Course.objects.filter()
        lesson_id = lesson_update_data['lesson_level']
        level_id = Lesson.objects.filter(id=lesson_id)[0].level_id
        course_id = Level.objects.filter(id=level_id)[0].course_id
        for course in courses:
            if course.id is course_id:
                sb.append('<option value = "{0}" selected> {1} </option>\n'.format(course.id, course.name))
            else:
                sb.append('<option value = "{0}" > {1} </option>\n'.format(course.id, course.name))
        sb.append('             </select>')
        sb.append('             <hr>')
        sb.append('         </div>')
        # level
        sb.append('         <div>')
        sb.append('             <h4 class="widget-title blue smaller">')
        sb.append('             <i class="ace-icon fa glyphicon-asterisk orange"></i>Select Levels')
        sb.append('             </h4>')
        sb.append('             <select class="form-control level-select">')
        # first_course_id = Course.objects.first().id
        # lesson_id = lesson_update_data['lesson_level']
        # level_id = Lesson.objects.filter(id=lesson_id)[0].level_id
        # course_id = Level.objects.filter(id=level_id)[0].course_id
        levels = Level.objects.filter(course_id=course_id)
        level_id = Lesson.objects.filter(id=lesson_id)[0].level_id
        for level in levels:
            if level.id is level_id:
                sb.append('<option value = "{0}" selected> {1} </option>\n'.format(level.id, level.name))
            else:
                sb.append('<option value = "{0}" > {1} </option>\n'.format(level.id, level.name))
        sb.append('             </select>')
        sb.append('             <hr>')
        sb.append('         </div>')
        # select lesson
        sb.append('         <div>')
        sb.append('             <h4 class="widget-title blue smaller">')
        sb.append('             <i class="ace-icon fa glyphicon-asterisk orange"></i>Select Lessons')
        sb.append('             </h4>')
        sb.append('             <select class="form-control lesson-select">')
        # first_level_id = levels[0].id
        # lesson_id = lesson_update_data['lesson_level']
        # level_id = Lesson.objects.filter(id=lesson_id)[0].level_id
        lessons = Lesson.objects.filter(level_id=level_id)
        for lesson in lessons:
            if lesson.id is lesson_update_data['lesson_level']:
                sb.append('<option value = "{0}" selected > {1} </option>\n'.format(lesson.id, lesson.name))
            else:
                sb.append('<option value = "{0}"> {1} </option>\n'.format(lesson.id, lesson.name))
        sb.append('             </select>')
        sb.append('             <hr>')
        sb.append('         </div>')
        
        # sb.append('         <div>')
        # sb.append('             <h4 class="widget-title blue smaller">')
        # sb.append('             <i class="ace-icon fa glyphicon-asterisk orange"></i>Select Levels')
        # sb.append('             </h4>')
        # sb.append('             <select class="form-control course-level" name="select-level-name" id="select-level-id">')
        # 
        # levels = Master.objects.filter(mastertype=MasterType.LessonLevel.code)
        # for level in levels:
        #     if level.master_id is lesson_update_data['lesson_level']:
        #         sb.append('<option value = "{0}" selected > {1} </option>\n'.format(level.master_id, level.name))
        #     else:
        #         sb.append('<option value = "{0}"> {1} </option>\n'.format(level.master_id, level.name))
        # 
        # sb.append('             </select>')
        # sb.append('             <hr>')
        # sb.append('         </div>')


        sb.append('</div>')

        # step2
        sb.append('<div class="step-pane" data-step="2">')
        sb.append('        <div>')
        sb.append('            <h4 class="widget-title blue smaller">')
        sb.append(
            '			    <i class="ace-icon fa glyphicon-asterisk orange"></i>Please select the lesson summary')
        sb.append('             </h4>')
        sb.append('             <div class="col-xs-12" id="import-video-form-id">')
        sb.append('                 <label class="ace-file-input">')
        sb.append('                     <input class="lesson-summary" type="file" id="id-input-file-2">')
        sb.append('                 </label>')
        sb.append('             </div>')
        sb.append('         <hr><hr>')
        sb.append('         </div>')
        sb.append('         <div>')
        sb.append('             <h4 class="widget-title blue smaller">')
        sb.append('             <i class="ace-icon fa glyphicon-asterisk orange"></i>Lesson title</h4>')
        sb.append('             </h4>')
        sb.append('             <textarea class="form-control limited lesson-title" id="form-lesson-title" placeholder="Lesson title" >{0}</textarea>'.format(lesson_update_data['lesson_title']))
        sb.append('         </div>')
        sb.append('         <hr>')
        sb.append('         <div>')
        sb.append('             <h4 class="widget-title blue smaller">')
        sb.append('             <i class="ace-icon fa glyphicon-asterisk orange"></i>Lesson content</h4>')
        sb.append('             </h4>')
        sb.append('             <textarea class="form-control limited lesson-content" id="form-lesson-content" placeholder="Lesson content" >{0}</textarea>'.format(lesson_update_data['lesson_content']))
        sb.append('         </div>')
        sb.append('</div>')

        # step3
        # for item in test_update_data["test_list"]:

        sb.append('<div class="step-pane" data-step="3">')
        sb.append('<input type = "hidden"  id = "current_question" name = "current_question" value = "{0}">\n'.format(
            self.get_current_question()))
        sb.append('<input type = "hidden"  id = "current_test" name = "current_test" value = "{0}">\n'.format(self.get_current_question()))


        sb.append('     <div id="question-form">')
        # test and question

        sb.append('<div>\n')
        sb.append('<h4 class ="widget-title blue smaller" >\n')
        sb.append('<i class ="ace-icon fa glyphicon-asterisk orange" > </i> Select question types\n')
        sb.append('</h4>\n')
        sb.append('<select class ="form-control question-type" id="question_type" name="question-type-name" >\n')
        question_types = Master.objects.filter(mastertype=MasterType.QuestionType.code)
        for question_type in question_types:
            sb.append('<option value = "{0}" > {1} </option>\n'.format(question_type.master_id, question_type.name))
        sb.append('</select>\n')
        sb.append('</div>\n')
        sb.append('<hr>\n')
        sb.append('</div>\n')
        #Add test form here
        for i in range(0, len(test_update_data)):
            sb.append(LagForm.render_update_test_type(self, test_update_data[i]))
        sb.append('<hr>\n')
        sb.append('<div class ="wizard-actions" >\n')
        sb.append('<button type = "button" class ="btn btn-success" onclick="AddTest()" > Add Test\n')
        sb.append('<i class ="ace-icon fa fa-arrow-right icon-on-right" > </i>\n')
        sb.append('</button>\n')

        sb.append('     </div>')
        sb.append('</div>')

        # step4
        # sb.append('<div class="step-pane" data-step="4">')
        # sb.append('     <div class="center">')
        # sb.append('         <h3 class="green">Pl</h3>Please press fin')
        # sb.append('     </div>')
        # sb.append('</div>')
        sb.append('</div>')
        sb.append('</div>')
        sb.append('<hr>')

        return sb.__str__()



    def render_end_create_course(self):
        sb = StringBuilder()

        sb.append('     <button class="btn" type="button" style="float:left;" onclick="BackToList()">')
        sb.append('     <i class="ace-icon fa fa-arrow-left"></i>Exit</button>')

        sb.append('<div class="wizard-actions">')
        sb.append('     <button class="btn btn-prev" type="button" disabled="disabled">')
        sb.append('     <i class="ace-icon fa fa-arrow-left"></i>Prev</button>')
        sb.append('     <button class="btn btn-success btn-next" type="button" data-last="Finish">Next')
        sb.append('     <i class="ace-icon fa fa-arrow-right icon-on-right"></i>')
        sb.append('     </button>')
        sb.append('</div>')
        sb.append('</div>')
        sb.append('</div>')
        sb.append('</div>')
        sb.append('</form>')

        return sb.__str__()


    def render_filed(self, field):
        if field.field_type == FieldType.TextArea:
            sb = " "
        sb = StringBuilder()
        return sb

    # New

    # New
    def render_test_type(self, test_id, question_type):
        sb = StringBuilder()
        rowtmp = ''
        rowtmp += '<div class="row test-form-count" >'
        rowtmp += '   <div class="col-xs-12 col-sm-12">'
        rowtmp += '     <div class="widget-box">'
        rowtmp += '         <div class="widget-header">'
        # rowtmp += '             <h4 class="widget-title">Test {0}</h4>'.format(str(test_id))
        rowtmp += '             <input type="text" class="test-name" placeholder="Test Name" name="test-{0}" style="margin-top:0.5%;margin-bottom:0.5%;"/>'.format(test_id)
        rowtmp += '             <input type="number" class="test-goalnumber"  placeholder="Quantity" name="test-{0}" style="margin:0.5% 0.5% 0.5% 45%;"/>'.format(test_id)
        rowtmp += '             <input type="number" class="test-goalpercent" placeholder="Quality" name="test-{0}" style="margin:0.5% 0.5% 0.5% 0.5%;"/>'.format(test_id)

        rowtmp += '             <div class="widget-toolbar">'
        rowtmp += '                 <a href="#" data-action="collapse">'
        rowtmp += '                     <i class="ace-icon fa fa-chevron-up"></i>'
        rowtmp += '                 </a>'
        rowtmp += '                 <a href="#" data-action="close">'
        rowtmp += '                     <i class="ace-icon fa fa-times" onclick="CloseDetails(this)"></i>'
        rowtmp += '                 </a>'
        rowtmp += '         </div>'
        rowtmp += '         </div>'
        rowtmp += '         <div class="widget-body" style="display: block;">'
        rowtmp += '             <div class="widget-main" name="test-{0}-{1}" id="test-{0}-{1}">'.format(str(question_type), str(test_id))
        rowtmp += '<button type = "button" class ="btn btn-success" onclick="AddQuestion(this,{0},{1}, 1)" > Add Question\n'.format(question_type, test_id)
        rowtmp += '             </div>'
        rowtmp += '         </div>'
        rowtmp += '     </div>'
        rowtmp += '  </div>'
        rowtmp += '</div>'
        sb.append(rowtmp)
        return sb.__str__()

    def render_question_content(self, type, question_id, test_id):
        sb = StringBuilder()
        rowtmp = ''
        rowtmp += '<div class="row">'
        rowtmp += '   <div class="col-xs-12 col-sm-12">'
        rowtmp += '     <div class="widget-box">'
        rowtmp += '         <div class="widget-header">'
        rowtmp += '             <h4 class="widget-title">Question</h4>'
        rowtmp += '             <div class="widget-toolbar">'
        rowtmp += '                 <a href="#" data-action="collapse">'
        rowtmp += '                     <i class="ace-icon fa fa-chevron-up"></i>'
        rowtmp += '                 </a>'
        rowtmp += '                 <a href="#" data-action="close">'
        rowtmp += '                     <i class="ace-icon fa fa-times" onclick="CloseDetails(this)"></i>'
        rowtmp += '                 </a>'
        rowtmp += '         </div>'
        rowtmp += '         </div>'
        rowtmp += '         <div class="widget-body" style="display: block;">'
        rowtmp += '             <div class="widget-main">'
        rowtmp += LagForm.render_question_type(type, question_id, test_id)
        rowtmp += '             </div>'
        rowtmp += '         </div>'
        rowtmp += '     </div>'
        rowtmp += '  </div>'
        rowtmp += '</div>'
        sb.append(rowtmp)
        return sb.__str__()

    def render_question_type(type, question_id, test_id):
        sb = StringBuilder()
        rowtmp = ''
        if type == QuestionType.Type1.code:
            rowtmp += '<div>'
            rowtmp += ' <h4 class="widget-title blue smaller">'
            rowtmp += '   <i class="ace-icon fa glyphicon-asterisk orange"></i>'
            rowtmp += '     Please choose audio'
            rowtmp += ' </h4>'
            rowtmp += ' <div class="col-xs-12" id="audio-select-type1">'
            rowtmp += '    <label class="ace-file-input">'
            rowtmp += '       <input type="file" class="input-file question-option" name="audio-{0}-{1}-{2}" >'.format(str(question_id), str(type), str(test_id))
            rowtmp += '    </label>'
            rowtmp += ' </div>'
            rowtmp += '</div>'
            rowtmp += '<hr>'
            rowtmp += '<div>'
            rowtmp += ' <h4 class="widget-title blue smaller">'
            rowtmp += '    <i class="ace-icon fa glyphicon-asterisk orange"></i>'
            rowtmp += '    Please choose images'
            rowtmp += ' </h4>'
            rowtmp += ' <div class ="col-xs-12">'
            rowtmp += '     <input class="id-input-file-3 question-option" multiple="" type="file" ' \
                      '     id="id-input-file-{0}" name="image-{1}-{2}-{3}">'.format(str(question_id), str(question_id), str(type), str(test_id))
            rowtmp += ' </div>'
            rowtmp += '</div>'
            rowtmp += '<hr>'
            rowtmp += '<div>'
            rowtmp += ' <div> <h4 class ="widget-title blue smaller" >'
            rowtmp += '     <i class ="ace-icon fa glyphicon-asterisk orange"> </i>'
            rowtmp += '        Select answer'
            rowtmp += '       </h4>'
            rowtmp += '     <select class ="form-control answer-option" name="answer-{0}-{1}-{2}">'.format(str(question_id), str(type), str(test_id))
            rowtmp += '     </select>'
            rowtmp += '</div>'
            rowtmp += '</div>'

        elif type == QuestionType.Type2.code or type == QuestionType.Type8.code:
            rowtmp += '<div>'
            rowtmp += ' <h4 class="widget-title blue smaller">'
            rowtmp += '   <i class="ace-icon fa glyphicon-asterisk orange"></i>'
            rowtmp += '     Please choose video'
            rowtmp += ' </h4>'
            rowtmp += ' <div class="col-xs-12" id="audio-select-type1">'
            rowtmp += '    <label class="ace-file-input">'
            rowtmp += '       <input type="file" class="input-file question-option" name="image-{0}-{1}-{2}" >'.format(str(question_id),
                                                                                                       str(type),
                                                                                                       str(test_id))
            rowtmp += '    </label>'
            rowtmp += ' </div>'
            rowtmp += '</div>'
            rowtmp += '<hr>'
            rowtmp += '<div>'
            rowtmp += ' <h4 class="widget-title blue smaller">'
            rowtmp += '    <i class="ace-icon fa glyphicon-asterisk orange"></i>'
            rowtmp += '    Please choose audio files'
            rowtmp += ' </h4>'
            rowtmp += ' <div class ="col-xs-12">'
            rowtmp += '     <input class="id-input-file-3 question-option" multiple="" type="file" ' \
                      '     id="id-input-file-{0}" name="audio-{1}-{2}-{3}">'.format(str(question_id), str(question_id),
                                                                                     str(type), str(test_id))
            rowtmp += ' </div>'
            rowtmp += '</div>'
            rowtmp += '<hr>'
            rowtmp += '<div>'
            rowtmp += ' <div> <h4 class ="widget-title blue smaller" >'
            rowtmp += '     <i class ="ace-icon fa glyphicon-asterisk orange"> </i>'
            rowtmp += '        Select answer'
            rowtmp += '       </h4>'
            rowtmp += '     <select class ="form-control answer-option" name="answer-{0}-{1}-{2}">'.format(str(question_id),
                                                                                             str(type), str(test_id))
            rowtmp += '     </select>'
            rowtmp += '</div>'
            rowtmp += '</div>'

        elif type == QuestionType.Type4.code:
            rowtmp += '<div>'
            rowtmp += '<h4 class="widget-title blue smaller">'
            rowtmp += '   <i class="ace-icon fa glyphicon-asterisk orange"></i>'
            rowtmp += 'Please choose audio'
            rowtmp += '</h4>'
            rowtmp += '<div class="col-xs-12" id="audio-select-type1">'
            rowtmp += '    <label class="ace-file-input">'
            rowtmp += '       <input type="file" class="input-file question-option" name="audio-{0}-{1}-{2}" >'.format(str(question_id),
                                                                                                       str(type),
                                                                                                       str(test_id))
            rowtmp += '    </label>'
            rowtmp += '</div>'
            rowtmp += '</div>'
            rowtmp += ' <hr>'

            rowtmp += '<div>'
            rowtmp += '<h4 class="widget-title blue smaller">'
            rowtmp += '<i class="ace-icon fa glyphicon-asterisk orange"></i>Please type correct word</h4>'
            rowtmp += '<div class="col-xs-12">'
            rowtmp += '<input type="text" placeholder="Correct Word" class="col-xs-3 col-sm-3 answer-option" ' \
                      'name="answer-{0}-{1}-{2}">'.format(str(question_id), str(type), str(test_id))
            rowtmp += '</div><br><br></div>'

        elif type == QuestionType.Type5.code:
            input_name = "question-" + str(question_id) + "-" + str(type) + "-" + str(test_id)
            rowtmp += '<div class="test">'
            rowtmp += '<h4 class="widget-title blue smaller"><i class="ace-icon fa glyphicon-asterisk orange"></i>'
            rowtmp += 'Enter the question: </h4>'
            rowtmp += '<textarea name={0} class="form-control limited lesson-title question-text-content" id="form-lesson-title" placeholder="Enter the question"> </textarea>'.format(input_name)
            rowtmp += '<div class="col-xs-12" id="image-select-type2">'
            rowtmp += '</div></div><hr>'
            rowtmp += '<div>'
            rowtmp += '<h4 class="widget-title blue smaller">'
            rowtmp += '<i class="ace-icon fa glyphicon-asterisk orange"></i>Please type option</h4>'
            rowtmp += '<div class="col-xs-12">'

            for i in range(1, CommonConfig.NumberOfAnswer + 1):
                name = "{0}-{1}-{2}".format(str(question_id), str(type), str(test_id))
                placeholder = 'Options ' + str(i)
                rowtmp += '     <div class="col-xs-6">'
                rowtmp += '         <input type = "text" class ="input-large answer-option" name="input-option-{0}-{1}" ' \
                          'placeholder="{2}" >'.format(name, i, placeholder)
                rowtmp += '             &nbsp;&nbsp'
                if i == 1:
                    rowtmp += '         <input name = "answer-{0}" type = "radio" class ="ace radio-answer" value={1} checked>'.format(name, i)
                else:
                    rowtmp += '         <input name = "answer-{0}" type = "radio" class ="ace radio-answer" value={1}>'.format(name, i)
                rowtmp += '         <span class ="lbl"></span>'
                rowtmp += '     </div>'
                if i % 2 == 0:
                    rowtmp += '<br><br>'
            rowtmp += '</div><br><br><br><br>'
            rowtmp += '</div>'
        elif type == QuestionType.Type6.code:
            rowtmp += '<div class="answer-option" id="answer-{0}-{1}-{2}">'.format(str(question_id), str(type), str(test_id))
            rowtmp += ' <h4 class="widget-title blue smaller">'
            rowtmp += '   <i class="ace-icon fa glyphicon-asterisk orange"></i>'
            rowtmp += '     Please choose image'
            rowtmp += ' </h4>'
            rowtmp += ' <div class="col-xs-12" id="audio-select-type1">'
            rowtmp += '    <label class="ace-file-input">'
            rowtmp += '       <input type="file" class="input-file question-option" name="image-{0}-{1}-{2}" >'.format(
                str(question_id),
                str(type),
                str(test_id))
            rowtmp += '    </label>'
            rowtmp += ' </div>'
            rowtmp += '</div>'
            rowtmp += '<hr>'
            rowtmp += '<div>'
            rowtmp += ' <h4 class="widget-title blue smaller">'
            rowtmp += '    <i class="ace-icon fa glyphicon-asterisk orange"></i>'
            rowtmp += '    Please choose audio files'
            rowtmp += ' </h4>'
            rowtmp += ' <div class="col-xs-12" id="audio-select-type1">'
            rowtmp += '    <label class="ace-file-input">'
            rowtmp += '       <input type="file" class="input-file question-option" name="audio-{0}-{1}-{2}" >'.format(
                str(question_id),
                str(type),
                str(test_id))
            rowtmp += '    </label>'
            rowtmp += ' </div>'
            rowtmp += '<div>'
            rowtmp += ' <h4 class="widget-title blue smaller">'
            rowtmp += '   <i class="ace-icon fa glyphicon-asterisk orange"></i>'
            rowtmp += '     Please choose image hint'
            rowtmp += ' </h4>'
            rowtmp += ' <div class="col-xs-12" id="audio-select-type1">'
            rowtmp += '    <label class="ace-file-input">'
            rowtmp += '       <input type="file" class="input-file question-option" name="image_hint-{0}-{1}-{2}" >'.format(
                str(question_id),
                str(type),
                str(test_id))
            rowtmp += '    </label>'
            rowtmp += ' </div>'
            rowtmp += ' </br></br></div>'
        elif type == QuestionType.Type7.code:
            rowtmp += '<div class="answer-option" id="answer-{0}-{1}-{2}">'.format(str(question_id), str(type), str(test_id))
            rowtmp += ' <h4 class="widget-title blue smaller">'
            rowtmp += '    <i class="ace-icon fa glyphicon-asterisk orange"></i>'
            rowtmp += '    Please choose video'
            rowtmp += ' </h4>'
            rowtmp += ' <div class="col-xs-12" id="audio-select-type1">'
            rowtmp += '    <label class="ace-file-input">'
            rowtmp += '       <input type="file" class="input-file question-option" name="video-{0}-{1}-{2}" >'.format(
                str(question_id),
                str(type),
                str(test_id))
            rowtmp += '    </label>'
            rowtmp += ' </div>'
            rowtmp += '<div>'
            rowtmp += ' <h4 class="widget-title blue smaller">'
            rowtmp += '   <i class="ace-icon fa glyphicon-asterisk orange"></i>'
            rowtmp += '     Please choose image hint'
            rowtmp += ' </h4>'
            rowtmp += ' <div class="col-xs-12" id="audio-select-type1">'
            rowtmp += '    <label class="ace-file-input">'
            rowtmp += '       <input type="file" class="input-file question-option" name="image_hint-{0}-{1}-{2}" >'.format(
                str(question_id),
                str(type),
                str(test_id))
            rowtmp += '    </label>'
            rowtmp += ' </div>'
            rowtmp += ' </br></br></div>'
        elif type == QuestionType.Type3.code:
            rowtmp += '<div>'
            rowtmp += ' <h4 class="widget-title blue smaller">'
            rowtmp += '   <i class="ace-icon fa glyphicon-asterisk orange"></i>'
            rowtmp += '     Please choose image'
            rowtmp += ' </h4>'
            rowtmp += ' <div class="col-xs-12" id="audio-select-type1">'
            rowtmp += '    <label class="ace-file-input">'
            rowtmp += '       <input type="file" class="input-file question-option" name="image-{0}-{1}-{2}" >'.format(
                str(question_id),
                str(type),
                str(test_id))
            rowtmp += '    </label>'
            rowtmp += ' </div>'
            rowtmp += '</div>'
            rowtmp += '<hr>'

            rowtmp += '<div>'
            rowtmp += ' <h4 class="widget-title blue smaller">'
            rowtmp += '   <i class="ace-icon fa glyphicon-asterisk orange"></i>'
            rowtmp += '     Please choose audio'
            rowtmp += ' </h4>'
            rowtmp += ' <div class="col-xs-12" id="audio-select-type1">'
            rowtmp += '    <label class="ace-file-input">'
            rowtmp += '       <input type="file" class="input-file question-option" name="audio-{0}-{1}-{2}" >'.format(
                str(question_id),
                str(type),
                str(test_id))
            rowtmp += '    </label>'
            rowtmp += ' </div>'
            rowtmp += '</div>'

            rowtmp += '<hr>'
            rowtmp += '<div>'
            rowtmp += ' <h4 class="widget-title blue smaller">'
            rowtmp += '    <i class="ace-icon fa glyphicon-asterisk orange"></i>'
            rowtmp += '    Please choose audio files'
            rowtmp += ' </h4>'
            rowtmp += ' <div class ="col-xs-12">'
            rowtmp += '     <input class="id-input-file-3 question-option" multiple="" type="file" ' \
                      '     id="id-input-file-{0}" name="answer_audio-{1}-{2}-{3}">'.format(str(question_id), str(question_id),
                                                                                     str(type), str(test_id))
            rowtmp += ' </div>'
            rowtmp += '</div>'
            rowtmp += '<hr>'
            rowtmp += '<div>'
            rowtmp += ' <div> <h4 class ="widget-title blue smaller" >'
            rowtmp += '     <i class ="ace-icon fa glyphicon-asterisk orange"> </i>'
            rowtmp += '        Select answer'
            rowtmp += '       </h4>'
            rowtmp += '     <select class ="form-control answer-option" name="answer-{0}-{1}-{2}">'.format(
                str(question_id),
                str(type), str(test_id))
            rowtmp += '     </select>'
            rowtmp += '</div>'
            rowtmp += '</div>'
        sb.append(rowtmp)
        return sb.__str__()
    # Update

    @staticmethod
    def render_update_test_type(self, test_list):
        question_update_data = self.get_question_update_data()
        sb = StringBuilder()
        rowtmp = ''
        rowtmp += '<div class="row test-form-count" >'
        rowtmp += '   <div class="col-xs-12 col-sm-12">'
        rowtmp += '     <div class="widget-box">'
        rowtmp += '         <div class="widget-header">'
        rowtmp += '             <input type="text" value="{1}" class="test-name" placeholder="Test Name" name="test-{0}" style="margin-top:0.5%;margin-bottom:0.5%;"/>'.format(test_list["id"], test_list["name"])
        rowtmp += '             <input type="number" value="{1}" class="test-goalnumber" placeholder="Goal Number" name="test-{0}" style="margin:0.5% 0.5% 0.5% 45%;"/>'.format(test_list["id"], test_list["number_goal"])
        rowtmp += '             <input type="number" value="{1}" class="test-goalpercent" placeholder="Goal Percent" name="test-{0}" style="margin:0.5% 0.5% 0.5% 0.5%;"/>'.format(test_list["id"], test_list["percent_goal"])

        rowtmp += '             <div class="widget-toolbar">'
        rowtmp += '                 <a href="#" data-action="collapse">'
        rowtmp += '                     <i class="ace-icon fa fa-chevron-up"></i>'
        rowtmp += '                 </a>'
        rowtmp += '                 <a href="#" data-action="close">'
        rowtmp += '                     <i class="ace-icon fa fa-times" onclick="CloseDetails(this)"></i>'
        rowtmp += '                 </a>'
        rowtmp += '         </div>'
        rowtmp += '         </div>'
        rowtmp += '         <div class="widget-body" style="display: block;">'
        rowtmp += '             <div class="widget-main" name="test-{0}-{1}" id="test-{0}-{1}">'.format(str(test_list["type"]), str(test_list["id"]))
        rowtmp += '             <div>'
        rowtmp += '                 <button type = "button" class ="btn btn-success" onclick="AddQuestion(this,{0},{1}, {2})" /> Add Question\n'.format(test_list["type"], test_list["id"], test_list['max_question_id'])
        rowtmp += '             </div>'
        for i in range(len(question_update_data)):
            if question_update_data[i]["test_id"] == test_list["id"]:
                    rowtmp += LagForm.render_update_question_content(self, question_update_data[i])
        rowtmp += '</div>'
        rowtmp += '         </div>'
        rowtmp += '     </div>'
        rowtmp += '  </div>'
        rowtmp += '</div>'
        sb.append(rowtmp)
        return sb.__str__()

    def render_update_question_content(self, question_list):
        sb = StringBuilder()
        rowtmp = ''
        rowtmp += '<div class="row">'
        rowtmp += '   <div class="col-xs-12 col-sm-12">'
        rowtmp += '     <div class="widget-box">'
        rowtmp += '         <div class="widget-header">'
        rowtmp += '             <h4 class="widget-title">Question</h4>'
        rowtmp += '             <div class="widget-toolbar">'
        rowtmp += '                 <a href="#" data-action="collapse">'
        rowtmp += '                     <i class="ace-icon fa fa-chevron-up"></i>'
        rowtmp += '                 </a>'
        rowtmp += '                 <a href="#" data-action="close">'
        rowtmp += '                     <i class="ace-icon fa fa-times" onclick="CloseDetails(this)"></i>'
        rowtmp += '                 </a>'
        rowtmp += '         </div>'
        rowtmp += '         </div>'
        rowtmp += '         <div class="widget-body" style="display: block;">'
        rowtmp += '             <div class="widget-main">'
        rowtmp += LagForm.render_update_question_type(self, question_list["type"], question_list["id"], question_list["test_id"], question_list["answer"], question_list["lesson_id"], question_list["question"], question_list["list_answer"])
        rowtmp += '             </form>'
        rowtmp += '             </div>'
        rowtmp += '         </div>'
        rowtmp += '     </div>'
        rowtmp += '  </div>'
        rowtmp += '</div>'
        sb.append(rowtmp)
        return sb.__str__()

    def render_update_question_type(self, type, question_id, test_id, answer, lesson_id, question_name, answer_list):
        sb = StringBuilder()
        rowtmp = ''
        if type == QuestionType.Type1.code:
            rowtmp += '<div>'
            rowtmp += ' <h4 class="widget-title blue smaller">'
            rowtmp += '   <i class="ace-icon fa glyphicon-asterisk orange"></i>'
            rowtmp += '     Please choose audio'
            rowtmp += ' </h4>'
            rowtmp += ' <div class="col-xs-12" id="audio-select-type1">'
            rowtmp += '    <label class="ace-file-input">'
            rowtmp += '       <input type="file" class="input-file question-option simple-file-{0}-{1}-{2}" name="audio-{0}-{1}-{2}" >'.format(str(question_id), str(type), str(test_id))
            rowtmp += '    </label>'
            rowtmp += ' </div>'
            rowtmp += '</div>'
            rowtmp += '<hr>'
            rowtmp += '<div>'
            rowtmp += ' <h4 class="widget-title blue smaller">'
            rowtmp += '    <i class="ace-icon fa glyphicon-asterisk orange"></i>'
            rowtmp += '    Please choose images'
            rowtmp += ' </h4>'
            rowtmp += ' <div class ="col-xs-12">'
            rowtmp += '     <input class="id-input-file-3 question-option mutiple-file-{0}-{1}-{2}" multiple="" type="file" ' \
                      '     id="id-input-file-{0}" name="image-{0}-{1}-{2}">'.format(str(question_id), str(type), str(test_id))

            rowtmp += ' </div>'
            rowtmp += '</div>'
            rowtmp += '<hr>'
            rowtmp += '<div>'
            rowtmp += ' <div> <h4 class ="widget-title blue smaller" >'
            rowtmp += '     <i class ="ace-icon fa glyphicon-asterisk orange"> </i>'
            rowtmp += '        Select answer'
            rowtmp += '       </h4>'
            rowtmp += '     <select class ="form-control answer-option" name="answer-{0}-{1}-{2}">'.format(str(question_id), str(type), str(test_id))
            answer_file_path = os.path.join(settings.BASE_DIR, 'media/', str(lesson_id), 'test',
                                            str(test_id), str(question_id), 'answer')
            answer_file_list = list()
            if os.path.exists(answer_file_path):
                answer_file_list = [f for f in os.listdir(answer_file_path)]
                # with os.scandir(answer_file_path) as list_file:
                #     for files in list_file:
                #         if files.is_file():
                #             answer_file_list.append(files.name)

            for file in answer_file_list:
                if file == answer:
                    rowtmp += '<option  selected > {0} </option>'.format(file)
                else:
                    rowtmp += '<option > {0} </option>'.format(file)
            rowtmp += '     </select>'
            rowtmp += '</div>'
            rowtmp += '</div>'

        elif type == QuestionType.Type2.code or type == QuestionType.Type8.code:
            rowtmp += '<div>'
            rowtmp += ' <h4 class="widget-title blue smaller">'
            rowtmp += '   <i class="ace-icon fa glyphicon-asterisk orange"></i>'
            rowtmp += '     Please choose image'
            rowtmp += ' </h4>'
            rowtmp += ' <div class="col-xs-12" id="audio-select-type1">'
            rowtmp += '    <label class="ace-file-input">'
            rowtmp += '       <input type="file" class="input-file question-option simple-file-{0}-{1}-{2}" name="image-{0}-{1}-{2}" >'.format(str(question_id),
                                                                                                       str(type),
                                                                                                       str(test_id))
            rowtmp += '    </label>'
            rowtmp += ' </div>'
            rowtmp += '</div>'
            rowtmp += '<hr>'
            rowtmp += '<div>'
            rowtmp += ' <h4 class="widget-title blue smaller">'
            rowtmp += '    <i class="ace-icon fa glyphicon-asterisk orange"></i>'
            rowtmp += '    Please choose audio files'
            rowtmp += ' </h4>'
            rowtmp += ' <div class ="col-xs-12">'
            rowtmp += '     <input class="id-input-file-3 question-option mutiple-file-{0}-{1}-{2}" multiple="" type="file" ' \
                      '     id="id-input-file-{0}" name="audio-{0}-{1}-{2}">'.format(str(question_id),
                                                                                     str(type), str(test_id))
            rowtmp += ' </div>'
            rowtmp += '</div>'
            rowtmp += '<hr>'
            rowtmp += '<div>'
            rowtmp += ' <div> <h4 class ="widget-title blue smaller" >'
            rowtmp += '     <i class ="ace-icon fa glyphicon-asterisk orange"> </i>'
            rowtmp += '        Select answer'
            rowtmp += '       </h4>'
            rowtmp += '     <select class ="form-control answer-option" name="answer-{0}-{1}-{2}">'.format(
                str(question_id), str(type), str(test_id))
            answer_file_path = os.path.join(settings.BASE_DIR, 'media/', str(lesson_id), 'test',
                                            str(test_id), str(question_id), 'answer')
            answer_file_list = list()
            if os.path.exists(answer_file_path):
                answer_file_list = [f for f in os.listdir(answer_file_path)]
                #
                # with os.scandir(answer_file_path) as list_file:
                #     for files in list_file:
                #         if files.is_file():
                #             answer_file_list.append(files.name)

            for file in answer_file_list:
                if file == answer:
                    rowtmp += '<option selected > {0} </option>'.format(file)
                else:
                    rowtmp += '<option > {0} </option>'.format(file)
            rowtmp += '     </select>'
            rowtmp += '</div>'
            rowtmp += '</div>'

        elif type == QuestionType.Type4.code:
            rowtmp += '<div>'
            rowtmp += '<h4 class="widget-title blue smaller">'
            rowtmp += '   <i class="ace-icon fa glyphicon-asterisk orange"></i>'
            rowtmp += 'Please choose audio'
            rowtmp += '</h4>'
            rowtmp += '<div class="col-xs-12" id="audio-select-type1">'
            rowtmp += '    <label class="ace-file-input">'
            rowtmp += '       <input type="file" class="input-file question-option simple-file" name="audio-{0}-{1}-{2}" >'.format(str(question_id),
                                                                                                       str(type),
                                                                                                       str(test_id))
            rowtmp += '    </label>'
            rowtmp += '</div>'
            rowtmp += '</div>'
            rowtmp += ' <hr>'

            rowtmp += '<div>'
            rowtmp += '<h4 class="widget-title blue smaller">'
            rowtmp += '<i class="ace-icon fa glyphicon-asterisk orange"></i>Please type correct word</h4>'
            rowtmp += '<div class="col-xs-12">'
            rowtmp += '<input type="text" placeholder="Correct Word" class="col-xs-3 col-sm-3 answer-option" name="answer-{0}-{1}-{2}" value="{3}">'.format(str(question_id), str(type),
                                                                                         str(test_id), answer)
            rowtmp += '</div><br><br></div>'

        elif type == QuestionType.Type5.code:
            input_name = "question-" + str(question_id) + "-" + str(type) + "-" + str(test_id)
            rowtmp += '<div class="test">'
            rowtmp += '<h4 class="widget-title blue smaller"><i class="ace-icon fa glyphicon-asterisk orange"></i>'
            rowtmp += 'Enter the question: </h4>'
            rowtmp += '<textarea name={0} class="form-control limited lesson-title question-text-content" id="form-lesson-title" placeholder="Enter the question">{1} </textarea>'.format(input_name, question_name)
            rowtmp += '<div class="col-xs-12" id="image-select-type2">'

            rowtmp += '</div></div><hr>'
            rowtmp += '<div>'
            rowtmp += '<h4 class="widget-title blue smaller">'
            rowtmp += '<i class="ace-icon fa glyphicon-asterisk orange"></i>Please type noun</h4>'
            rowtmp += '<div class="col-xs-12">'
            rowtmp += '<form>'

            answer_correct = Answer.objects.filter(id=int(answer))[0].answer

            for i in range(1, CommonConfig.NumberOfAnswer + 1):
                ratio_name = "answer-{0}-{1}-{2}".format(str(question_id), str(type),str(test_id))
                answer_text = answer_list[i - 1]

                name = "{0}-{1}-{2}".format(str(question_id), str(type), str(test_id))
                placeholder = 'Options ' + str(i)
                rowtmp += '     <div class="col-xs-6">'
                rowtmp += '         <input type = "text" class ="input-large answer-option" name="input-option-{0}-{1}" value="{3}" ' \
                          'placeholder="{2}" >'.format(name, i, placeholder, answer_text)
                rowtmp += '             &nbsp;&nbsp'
                if answer_correct == answer_text:
                    rowtmp += '         <input name = "{0}" type = "radio" class ="ace radio-answer" value={1} checked>'.format(ratio_name,i)

                else:
                    rowtmp += '         <input name = "{0}" type = "radio" class ="ace radio-answer" value={1}>'.format(ratio_name, i)
                rowtmp += '         <span class ="lbl" > </span> '
                rowtmp += '     </div>'

                if i % 2 == 0:
                    rowtmp += '<br><br>'
            rowtmp += '</div><br><br><br><br>'
            rowtmp += '</div>'

        elif type == QuestionType.Type6.code:
            rowtmp += '<div class="answer-option" id="answer-{0}-{1}-{2}">'.format(str(question_id), str(type), str(test_id))
            rowtmp += ' <h4 class="widget-title blue smaller">'
            rowtmp += '   <i class="ace-icon fa glyphicon-asterisk orange"></i>'
            rowtmp += '     Please choose image'
            rowtmp += ' </h4>'
            rowtmp += ' <div class="col-xs-12" id="audio-select-type1">'
            rowtmp += '    <label class="ace-file-input">'
            rowtmp += '       <input type="file" class="input-file question-option simple-file-image-{0}-{1}-{2}" name="image-{0}-{1}-{2}" >'.format(
                str(question_id),
                str(type),
                str(test_id))
            rowtmp += '    </label>'
            rowtmp += ' </div>'
            rowtmp += '</div>'
            rowtmp += '<hr>'
            rowtmp += '<div>'
            rowtmp += ' <h4 class="widget-title blue smaller">'
            rowtmp += '    <i class="ace-icon fa glyphicon-asterisk orange"></i>'
            rowtmp += '    Please choose audio files'
            rowtmp += ' </h4>'
            rowtmp += ' <div class="col-xs-12" id="audio-select-type1">'
            rowtmp += '    <label class="ace-file-input">'
            rowtmp += '       <input type="file" class="input-file question-option simple-file-audio-{0}-{1}-{2}" name="audio-{0}-{1}-{2}" >'.format(
                str(question_id),
                str(type),
                str(test_id))
            rowtmp += '    </label>'
            rowtmp += ' </div>'
            rowtmp += '<div>'
            rowtmp += ' <h4 class="widget-title blue smaller">'
            rowtmp += '   <i class="ace-icon fa glyphicon-asterisk orange"></i>'
            rowtmp += '     Please choose image hint'
            rowtmp += ' </h4>'
            rowtmp += ' <div class="col-xs-12" id="audio-select-type1">'
            rowtmp += '    <label class="ace-file-input">'
            rowtmp += '       <input type="file" class="input-file question-option simple-file-image_hint-{0}-{1}-{2}" name="image_hint-{0}-{1}-{2}" >'.format(
                str(question_id),
                str(type),
                str(test_id))
            rowtmp += '    </label>'
            rowtmp += ' </div>'
            rowtmp += ' </br></br></div></div>'
        elif type == QuestionType.Type7.code:
            rowtmp += '<div class="answer-option" id="answer-{0}-{1}-{2}">'.format(str(question_id), str(type), str(test_id))
            rowtmp += ' <h4 class="widget-title blue smaller">'
            rowtmp += '    <i class="ace-icon fa glyphicon-asterisk orange"></i>'
            rowtmp += '    Please choose video'
            rowtmp += ' </h4>'
            rowtmp += ' <div class="col-xs-12" id="audio-select-type1">'
            rowtmp += '    <label class="ace-file-input">'
            rowtmp += '       <input type="file" class="input-file question-option simple-file-video-{0}-{1}-{2}" name="video-{0}-{1}-{2}" >'.format(
                str(question_id),
                str(type),
                str(test_id))
            rowtmp += '    </label>'
            rowtmp += ' </div>'
            rowtmp += '<div>'
            rowtmp += ' <h4 class="widget-title blue smaller">'
            rowtmp += '   <i class="ace-icon fa glyphicon-asterisk orange"></i>'
            rowtmp += '     Please choose image hint'
            rowtmp += ' </h4>'
            rowtmp += ' <div class="col-xs-12" id="audio-select-type1">'
            rowtmp += '    <label class="ace-file-input">'
            rowtmp += '       <input type="file" class="input-file question-option simple-file-image_hint-{0}-{1}-{2}" name="image_hint-{0}-{1}-{2}" >'.format(
                str(question_id),
                str(type),
                str(test_id))
            rowtmp += '    </label>'
            rowtmp += ' </div>'
            rowtmp += ' </br></br></div></div>'
        elif type == QuestionType.Type3.code:
            rowtmp += '<div>'
            rowtmp += ' <h4 class="widget-title blue smaller">'
            rowtmp += '   <i class="ace-icon fa glyphicon-asterisk orange"></i>'
            rowtmp += '     Please choose image'
            rowtmp += ' </h4>'
            rowtmp += ' <div class="col-xs-12" id="audio-select-type1">'
            rowtmp += '    <label class="ace-file-input">'
            rowtmp += '       <input type="file" class="input-file question-option simple-file-image-{0}-{1}-{2}" name="image-{0}-{1}-{2}" >'.format(
                str(question_id),
                str(type),
                str(test_id))
            rowtmp += '    </label>'
            rowtmp += ' </div>'
            rowtmp += '</div>'
            rowtmp += '<hr>'

            rowtmp += '<div>'
            rowtmp += ' <h4 class="widget-title blue smaller">'
            rowtmp += '   <i class="ace-icon fa glyphicon-asterisk orange"></i>'
            rowtmp += '     Please choose audio'
            rowtmp += ' </h4>'
            rowtmp += ' <div class="col-xs-12" id="audio-select-type1">'
            rowtmp += '    <label class="ace-file-input">'
            rowtmp += '       <input type="file" class="input-file question-option simple-file-audio-{0}-{1}-{2}" name="audio-{0}-{1}-{2}" >'.format(
                str(question_id),
                str(type),
                str(test_id))
            rowtmp += '    </label>'
            rowtmp += ' </div>'
            rowtmp += '</div>'
            rowtmp += '<hr>'

            rowtmp += '<div>'
            rowtmp += ' <h4 class="widget-title blue smaller">'
            rowtmp += '    <i class="ace-icon fa glyphicon-asterisk orange"></i>'
            rowtmp += '    Please choose audio files'
            rowtmp += ' </h4>'
            rowtmp += ' <div class ="col-xs-12">'
            rowtmp += '     <input class="id-input-file-3 question-option mutiple-file-{0}-{1}-{2}" multiple="" type="file" ' \
                      '     id="id-input-file-{0}" name="answer_audio-{0}-{1}-{2}">'.format(str(question_id),
                                                                                     str(type), str(test_id))
            rowtmp += ' </div>'
            rowtmp += '</div>'
            rowtmp += '<hr>'
            rowtmp += '<div>'
            rowtmp += ' <div> <h4 class ="widget-title blue smaller" >'
            rowtmp += '     <i class ="ace-icon fa glyphicon-asterisk orange"> </i>'
            rowtmp += '        Select answer'
            rowtmp += '       </h4>'
            rowtmp += '     <select class ="form-control answer-option" name="answer-{0}-{1}-{2}">'.format(
                str(question_id), str(type), str(test_id))
            answer_file_path = os.path.join(settings.BASE_DIR, 'media/', str(lesson_id), 'test',
                                            str(test_id), str(question_id), 'answer')
            answer_file_list = list()
            if os.path.exists(answer_file_path):
                answer_file_list = [f for f in os.listdir(answer_file_path)]
                #
                # with os.scandir(answer_file_path) as list_file:
                #     for files in list_file:
                #         if files.is_file():
                #             answer_file_list.append(files.name)

            for file in answer_file_list:
                if file == answer:
                    rowtmp += '<option selected > {0} </option>'.format(file)
                else:
                    rowtmp += '<option > {0} </option>'.format(file)
            rowtmp += '     </select>'
            rowtmp += '</div>'
            rowtmp += '</div>'
        sb.append(rowtmp)
        return sb.__str__()

class LagField:
    sorting = False
    title = None
    field_type = None

    def __init__(self, sorting, title):
        self.sorting = sorting
        self.title = title
