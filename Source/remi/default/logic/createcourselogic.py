import os.path

from default.models.models import *
from default.config.common_config import *
from django.conf import settings
import shutil
import base64
import datetime

class CreateCourseLogic:
    @staticmethod
    def get_level_dict():
        lessons = Lesson.objects.filter()
        lessons_dict = {}
        for lesson in lessons:
            lesson_dict = dict()
            lesson_dict[lesson.id] = lesson.name
            lessons_dict.update(lesson_dict)
        return lessons_dict

    @staticmethod
    def store_lesson_data(request):
        lesson_id_new = CreateCourseLogic.store_part(request)
        lesson_id = request.POST.get('lesson_id', '')
        if lesson_id == '':
            lesson_id = lesson_id_new
        CreateCourseLogic.store_question_list(request, lesson_id)

        # CreateCourseLogic.store_course_content(request, lesson_id)
        return True

    @staticmethod
    def save_upload_file(request, file_field, path):
        file = request.FILES.get(file_field, None)
        if file:
            with open(path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            return file.name
        return None

    @staticmethod
    def save_course_video(request, part_id, filename):
        upload_video_path = os.path.join(settings.BASE_DIR, 'static/courses/', part_id, 'video')
        if not os.path.exists(upload_video_path):
            os.makedirs(upload_video_path)
        upload_video_path = os.path.join(upload_video_path, filename)
        CreateCourseLogic.save_upload_file(request, 'course_video', upload_video_path)
        return True

    @staticmethod
    def save_lesson_summary(request, lesson_id, filename):
        filename_strip = filename.replace(" ","-")
        upload_pdf_path = os.path.join(settings.BASE_DIR, 'static/courses/', lesson_id, 'summary')
        if not os.path.exists(upload_pdf_path):
            os.makedirs(upload_pdf_path)
        upload_video_path = os.path.join(upload_pdf_path, filename_strip)
        CreateCourseLogic.save_upload_file(request, 'lesson_summary', upload_video_path)
        return True

    @staticmethod
    def get_lesson_file(request, param):
        param_name = ''
        if request.FILES.get(param) is not None:
            param_name = request.FILES.get(param).name
        else:
            return param_name
        return param_name

    @staticmethod
    # store video_course, lesson table
    def store_part(request):
        params = request.POST
        lesson_id = params.get('lesson_part', '')
        part_id = params.get('lesson_id', '')
        if lesson_id != '':
            lesson_id = int(lesson_id)
        part_course_video = CreateCourseLogic.get_lesson_file(request, 'course_video')
        part_summary_pdf = CreateCourseLogic.get_lesson_file(request, 'lesson_summary').replace(" ","-")
        lesson_title = params.get('lesson_title', '')
        lesson_content = params.get('lesson_content', '')
        if part_id == '':
            new_lesson_order = 1
            from default.logic.testcontentlogic import TestContentLogic
            orders = TestContentLogic.get_part_order_ids(lesson_id)
            if len(orders) != 0:
                new_lesson_order = orders[len(orders) - 1] + 1

            new_part = Part()
            new_part.lesson_id = lesson_id
            new_part.name = lesson_title
            new_part.content = lesson_content
            new_part.summary = part_summary_pdf
            new_part.order = new_lesson_order
            new_part.updated_datetime = datetime.datetime.now()
            new_part.video = part_course_video
            new_part.save()
            id_value = new_part.id
            if part_course_video != '':
                    CreateCourseLogic.save_course_video(request, str(id_value), part_course_video)
            if part_summary_pdf != '':
                CreateCourseLogic.save_lesson_summary(request, str(id_value), part_summary_pdf)

        else:
            part_id = int(part_id)
            current_part = Part.objects.get(id=part_id)
            current_part.lesson_id = lesson_id
            current_part.name = lesson_title
            current_part.content = lesson_content
            current_part.updated_datetime = datetime.datetime.now()
            id_value = current_part.id

            if part_course_video != '':
                CreateCourseLogic.save_course_video(request, str(id_value), part_course_video)
                current_part.video = part_course_video
            if part_summary_pdf != '':
                CreateCourseLogic.save_lesson_summary(request, str(id_value), part_summary_pdf)
                current_part.summary = part_summary_pdf
            current_part.save()
        return id_value

    @staticmethod
    def store_question_list(request,  part_id):
        params = request.POST
        test_params_dict = {}
        #test from database
        list_testid = list()
        #list question change
        list_question_change = params.getlist('question_change')
        test_object = Test.objects.filter(part_id=part_id)
        for i in range(0, len(test_object)):
            list_testid.append(test_object[i].id)
        list_questionid = list()

        for key in params.keys():
            if "answer" in key:
                element = key.split('-')
                test_id = int(element[3])
                test_type = int(element[2])
                test_dict_ahihi = dict()
                test_key = 'test-' + str(test_id)
                header_test_list = params.getlist(test_key)
                if test_id not in test_params_dict:
                    test_dict_ahihi['test_type'] = test_type
                    test_dict_ahihi['test_define_id'] = test_id
                    test_name = header_test_list[0]
                    if header_test_list[2] == '':
                        number_goal = 0
                    else:
                        number_goal = header_test_list[2]
                    if header_test_list[1] == '':
                        percent_goal = 0
                    else:
                        percent_goal = header_test_list[1]
                    test_dict_ahihi['test_name'] = test_name
                    test_dict_ahihi['number_goal'] = number_goal
                    test_dict_ahihi['percent_goal'] = percent_goal
                    test_params_dict[test_id] = test_dict_ahihi
                    test_params_dict[test_id]['param_key_list'] = [key]
                else:
                    test_dict_ahihi = test_params_dict[test_id]
                    test_dict_ahihi['param_key_list'].append(key)

        for test_define_id in test_params_dict.keys():
            if test_define_id in list_testid:
                list_testid.remove(test_define_id)

            question_object = Question.objects.filter(part_id=part_id, test_id=test_define_id)
            for i in range(0, len(question_object)):
                list_questionid.append(question_object[i].id)
            test_dict = test_params_dict[test_define_id]
            test_type = test_dict['test_type']
            test_name = test_dict['test_name']
            test_number_goal = test_dict['number_goal']
            test_percent_goal = test_dict['percent_goal']
            if not Test.objects.filter(pk=test_define_id):
                test_new = Test()
            else:
                test_new = Test.objects.get(part_id=part_id, id=test_define_id)
            test_new.type = test_type
            test_new.part = Part.objects.get(pk=part_id)
            test_new.name = test_name
            test_new.question_percent_goal = test_number_goal
            test_new.question_number_goal = test_percent_goal
            test_new.save()
            question_param_key_list = test_params_dict[test_define_id]['param_key_list']
            for question_param_key in question_param_key_list:
                element = question_param_key.split('-')
                question_order = int(element[1])
                question_type = int(element[2])
                test_id = int(element[3])

                if question_order in list_questionid:
                    list_questionid.remove(question_order)
                is_new = False
                if not Question.objects.filter(pk=question_order):
                    question_new = Question()
                    is_update_type_5 = False
                    is_new = True
                else:
                    is_update_type_5 = True
                    question_new = Question.objects.get(part_id=part_id, test_id=test_new.id, id=question_order)
                question_new.test = Test.objects.get(pk=test_new.id)
                question_new.part_id = part_id
                question_new.type = question_type
                if question_type == QuestionType.Type5.code:
                    question_key = "question-" + element[1] + "-" + element[2] + "-" + element[3]
                    question_new.question = params.get(question_key, '')
                if question_type != QuestionType.Type5.code:
                    if is_new:
                        question_new.question = ""
                    question_new.answer = params.get(question_param_key, '')
                question_new.save()
                if question_type == QuestionType.Type5.code:
                    CreateCourseLogic.store_options_type5(question_new.id, request, question_param_key, is_update_type_5)
                    continue
                question_info = dict()
                question_info['test_id'] = test_new.id
                question_info['lesson_id'] = part_id
                question_info['question_type'] = question_type
                question_info['question_id'] = question_new.id
                question_info['question_order'] = question_order
                question_info['test_define_id'] = test_define_id
                question_info['question'] = question_new.question

                result = CreateCourseLogic.store_question_files(request, question_info)
                if not result:
                    return False

        # Delete test and question not exist
        for i in range(0, len(list_testid)):
            Test.objects.filter(id=list_testid[i]).delete()
            test_dir = os.path.join(settings.BASE_DIR, 'static/courses/', str(part_id), 'test', str(list_testid[i]))
            if os.path.exists(test_dir):
                shutil.rmtree(test_dir, ignore_errors=True)
        for i in range(0, len(list_questionid)):
            test_id = Question.objects.filter(id=list_questionid[i])[0].test_id
            Question.objects.filter(id=list_questionid[i]).delete()
            question_dir = os.path.join(settings.BASE_DIR, 'static/courses/', str(part_id), 'test', str(test_id), str(list_questionid[i]))
            if os.path.exists(question_dir):
                shutil.rmtree(question_dir, ignore_errors=True)
        # Delete question item

        return True


    @staticmethod
    def store_options_type5(question_id, request, key, is_update):
        answer_index = int(request.POST.get(key, 0))
        element = key.split('-')

        for i in range(1, CommonConfig.NumberOfAnswer + 1):
            option_key = 'input-option-' + element[1] + '-' + element[2] + '-' + element[3] + '-' + str(i)
            option_value = request.POST.get(option_key, '')

            # if not Answer.objects.filter(question_id=question_id):
            #     answer_new = Answer()
            # else:
            #     answer_new = Answer.objects.filter(question_id=question_id)
            if is_update is False:
                answer_new = Answer()
                answer_new.question_id = question_id
                answer_new.answer = option_value
                answer_new.save()
                if i == answer_index:
                    question = Question.objects.get(pk=question_id)
                    question.answer = answer_new.id
                    question.save()
            else:
                answer_object = Answer.objects.filter(question_id=question_id)
                # for j in range(0, answer_object.count()):
                answer_update = Answer.objects.get(id=answer_object[i-1].id)
                answer_update.answer = option_value
                answer_update.save()
                if i == answer_index:
                    question_update = Question.objects.get(pk=question_id)
                    question_update.answer = answer_update.id
                    question_update.save()

    @staticmethod
    def store_question_files(request, question_info):
        files = request.FILES
        test_id = question_info['test_id']
        test_define_id = question_info['test_define_id']
        lesson_id = question_info['lesson_id']
        question_type = question_info['question_type']
        question_id = question_info['question_id']
        question_order = question_info['question_order']
        question_name = question_info['question']
        end_name = str(question_order) + '-' + str(question_type) + '-' + str(test_define_id)
        question_file_name = None
        if question_type == QuestionType.Type1.code:
            audio_key = "audio-" + end_name
            if request.FILES.get(audio_key) is not None:
                audio_file = files[audio_key]
            else:
                audio_file = None
            if audio_file is not None:
                question_file_name = audio_file.name
                question_file_path = os.path.join(settings.BASE_DIR, 'static/courses/', str(lesson_id), 'test', str(test_id),
                                                 str(question_id), 'question')
                #delete before save
                if os.path.exists(question_file_path):
                    shutil.rmtree(question_file_path, ignore_errors=True)
                result = CreateCourseLogic.store_file(audio_file, question_file_path, question_file_name)
                if result is None:
                    return False

            # check to delete answer before save
            list_question_change = request.POST.getlist('question_change', None)
            if list_question_change is not None:
                if str(question_id) in list_question_change:
                    answer_dir = os.path.join(settings.BASE_DIR, 'static/courses/', str(lesson_id), 'test', str(test_id), str(question_id), 'answer')
                    if os.path.exists(answer_dir):
                        shutil.rmtree(answer_dir, ignore_errors=True)
            #save answer
            image_key = 'image-' + end_name
            images = files.getlist(image_key)
            for image in images:
                image_path = os.path.join(settings.BASE_DIR, 'static/courses/', str(lesson_id), 'test',
                                          str(test_id), str(question_id), 'answer')
                result = CreateCourseLogic.store_file(image, image_path, image.name)
                if result is None:
                    return False
        elif question_type == QuestionType.Type2.code or question_type == QuestionType.Type8.code:
            image_key = 'image-' + end_name
            if request.FILES.get(image_key) is not None:
                image_file = files[image_key]
            else:
                image_file = None
            if image_file is not None:
                question_file_name = image_file.name
                question_file_path = os.path.join(settings.BASE_DIR, 'static/courses/', str(lesson_id), 'test', str(test_id),
                                                 str(question_id), 'question')
                # delete before save
                if os.path.exists(question_file_path):
                    shutil.rmtree(question_file_path, ignore_errors=True)
                result = CreateCourseLogic.store_file(image_file, question_file_path, question_file_name)
                if result is None:
                    return False

            # check to delete answer before save
            list_question_change = request.POST.getlist('question_change', None)
            if list_question_change is not None:
                if str(question_id) in list_question_change:
                    answer_dir = os.path.join(settings.BASE_DIR, 'static/courses/', str(lesson_id), 'test',
                                              str(test_id), str(question_id), 'answer')
                    if os.path.exists(answer_dir):
                        shutil.rmtree(answer_dir, ignore_errors=True)


            audios_key = 'audio-' + end_name
            audios = files.getlist(audios_key)
            for audio in audios:
                audio_path = os.path.join(settings.BASE_DIR, 'static/courses', str(lesson_id), 'test',
                                          str(test_id),
                                          str(question_id), 'answer')
                result = CreateCourseLogic.store_file(audio, audio_path, audio.name)
                if result is None:
                    return False

        elif question_type == QuestionType.Type4.code:
            audio_key = 'audio-' + end_name
            if request.FILES.get(audio_key) is not None:
                audio_file = files[audio_key]
            else:
                audio_file = None
            if audio_file is not None:
                #Delete answer before save
                answer_dir = os.path.join(settings.BASE_DIR, 'static/courses/', str(lesson_id), 'test',
                                          str(test_id), str(question_id), 'question')
                if os.path.exists(answer_dir):
                    shutil.rmtree(answer_dir, ignore_errors=True)
                #save ne
                question_file_name = audio_file.name
                upload_video_path = os.path.join(settings.BASE_DIR, 'static/courses/', str(lesson_id), 'test', str(test_id),
                                                 str(question_id), 'question')
                result = CreateCourseLogic.store_file(audio_file, upload_video_path, question_file_name)
                if result is None:
                    return False

        elif question_type == QuestionType.Type5.code:
            return
        elif question_type == QuestionType.Type6.code:
            image_file_key = 'image-' + end_name
            audio_file_key = 'audio-' + end_name
            image_hint_file_key = 'image_hint-' + end_name
            path_save_qf = os.path.join(settings.BASE_DIR, 'static/courses/', str(lesson_id), 'test',
                                        str(test_id),
                                        str(question_id), 'question')
            CreateCourseLogic.save_follow_key(request, image_file_key, path_save_qf, False)
            CreateCourseLogic.save_follow_key(request, audio_file_key, path_save_qf, False)
            CreateCourseLogic.save_follow_key(request, image_hint_file_key, path_save_qf, False)
        elif question_type == QuestionType.Type7.code:
            video_file_key = 'video-' + end_name
            image_hint_file_key = 'image_hint-' + end_name
            path_save_qf = os.path.join(settings.BASE_DIR, 'static/courses/', str(lesson_id), 'test',
                                        str(test_id),
                                        str(question_id), 'question')
            CreateCourseLogic.save_follow_key(request, video_file_key, path_save_qf, False)
            CreateCourseLogic.save_follow_key(request, image_hint_file_key, path_save_qf, False)
        elif question_type == QuestionType.Type3.code:
            image_file_key = 'image-' + end_name
            question_audio_file_key = 'audio-' + end_name
            path_save_qf = os.path.join(settings.BASE_DIR, 'static/courses/', str(lesson_id), 'test',
                                        str(test_id),
                                        str(question_id), 'question')
            CreateCourseLogic.save_follow_key(request, image_file_key, path_save_qf, False)
            CreateCourseLogic.save_follow_key(request, question_audio_file_key, path_save_qf, False)

            #save answer
            path_save_af = os.path.join(settings.BASE_DIR, 'static/courses/', str(lesson_id), 'test',
                                        str(test_id),
                                        str(question_id), 'answer')
            audio_file_key = 'answer_audio-' + end_name
            CreateCourseLogic.save_follow_key(request, audio_file_key, path_save_af, True)

        if question_file_name is not None:
            question_update = Question.objects.get(pk=question_id)
            question_update.question = question_file_name
            question_update.save()

        return True

    @staticmethod
    def save_follow_key(request, key, path_question, is_answer):
        if is_answer is True:
            folder_name = ''
            file = request.FILES.getlist(key)
            if len(file) != 0:
                path_save = os.path.join(path_question, folder_name)
                if os.path.exists(path_save):
                    shutil.rmtree(path_save, ignore_errors=True)
                for audio in file:
                    result = CreateCourseLogic.store_file(audio, path_save, audio.name)
                    if result is None:
                        return False
        else:
            folder_name = key.split('-')[0]
            file = request.FILES.get(key)
            if file is not None:
                file_name = file.name
                path_save = os.path.join(path_question, folder_name)
                # delete before save
                if os.path.exists(path_save):
                    shutil.rmtree(path_save, ignore_errors=True)
                # save ne
                result = CreateCourseLogic.store_file(file, path_save, file_name)
                if result is None:
                    return False

    @staticmethod
    def store_file(file, path, file_name):
        if not os.path.exists(path):
            os.makedirs(path)
        upload_video_path = os.path.join(path, file_name)
        with open(upload_video_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        return file.name

    @staticmethod
    def get_course_list():
        course_list_db = Part.objects.filter().select_related()
        course_list_array = list()
        list_count = course_list_db.count()
        index = CourseList()
        lesson_dict = CreateCourseLogic.get_level_dict()
        for i in range(0, list_count):
            course_list_dict = dict()
            course_list_dict[index.test_number] = Test.objects.filter(part_id=course_list_db[i].id).count()
            course_list_dict[index.id] = course_list_db[i].id
            course_list_dict[index.name] = course_list_db[i].name
            course_list_dict[index.level] = course_list_db[i].lesson_id
            course_list_dict[index.order] = course_list_db[i].order
            course_list_dict[index.level_name] = lesson_dict[course_list_db[i].lesson_id]
            course_list_dict[index.update_date] = course_list_db[i].updated_datetime
            course_list_array.append(course_list_dict)
        return course_list_array

    @staticmethod
    def delete_part(part_id):
        """
        :type lesson_id: int
        :param lesson_id:
        :return:
        """
        Part.objects.filter(id=part_id).delete()
        # BaseStudentLesson.objects.filter(lesson_id=lesson_id).delete()
        Test.objects.filter(part_id=part_id).delete()
        BaseUserPart.objects.filter(part_id=part_id).delete()
        Question.objects.filter(part_id=part_id).delete()
        # TODO: Delete related files
        lesson_dir = os.path.join(settings.BASE_DIR, 'static/courses/', str(part_id))
        if os.path.exists(lesson_dir):
            shutil.rmtree(lesson_dir, ignore_errors=True)

    @staticmethod
    def edit_lesson(part_id):
        # lesson info
        part_list = dict()
        part_info = Part.objects.filter(id=part_id)
        part_lesson = part_info[0].lesson_id
        part_title = part_info[0].name
        part_content = part_info[0].content
        part_summary = part_info[0].summary
        part_course_video = part_info[0].video
        if part_course_video is None:
            part_course_video = ""
        part_list["lesson_level"] = part_lesson
        part_list["lesson_title"] = part_title
        part_list["lesson_content"] = part_content
        part_list["lesson_summary"] = part_summary
        part_list["lesson_course_video"] = part_course_video

        # test info

        test_info = Test.objects.filter(part_id=part_id)
        test_list = list()
        question_list = list()
        for i in range(0, test_info.count()):
            test_dict = dict()
            test_dict["id"] = test_info[i].id
            test_dict["type"] = test_info[i].type
            test_dict["name"] = test_info[i].name
            test_dict["number_goal"] = test_info[i].question_number_goal
            test_dict["percent_goal"] = test_info[i].question_percent_goal
            test_question_objecs = Question.objects.filter(test_id=test_info[i].id).order_by('-id')
            test_question_ids = []
            for test_question_object in test_question_objecs:
                test_question_ids.append(test_question_object.id)

            test_dict['max_question_id'] = test_question_ids[0] + 1

            test_list.append(test_dict)
            question_info = Question.objects.filter(part_id=part_id, test_id=test_info[i].id)
            for j in range(0, question_info.count()):
                question_dict = dict()
                question_dict["id"] = question_info[j].id
                question_dict["test_id"] = question_info[j].test_id
                question_dict["lesson_id"] = question_info[j].part_id
                question_dict["question"] = question_info[j].question
                question_dict["answer"] = question_info[j].answer
                question_dict["type"] = test_info[i].type
                #get question in folder
                type_test = test_info[i].type
                if type_test != 5:
                    question_file_list = list()
                    question_file_path = os.path.join(settings.BASE_DIR, 'static/courses/', str(part_id), 'test',
                                                      str(test_info[i].id), str(question_info[j].id), 'question')
                    if type_test == 6:
                        image_path = os.path.join(question_file_path, 'image')
                        if os.path.exists(image_path):
                            list_file = [f for f in os.listdir(image_path)]
                            question_file_list.append(list_file)
                        audio_path = os.path.join(question_file_path, 'audio')
                        if os.path.exists(audio_path):
                            list_file = [f for f in os.listdir(audio_path)]
                            question_file_list.append(list_file)
                        image_hint_path = os.path.join(question_file_path, 'image_hint')
                        if os.path.exists(image_hint_path):
                            list_file = [f for f in os.listdir(image_hint_path)]
                            question_file_list.append(list_file)
                    elif type_test == 7:
                        video_path = os.path.join(question_file_path, 'video')
                        if os.path.exists(video_path):
                            list_file = [f for f in os.listdir(video_path)]
                            question_file_list.append(list_file)
                        image_hint_path = os.path.join(question_file_path, 'image_hint')
                        if os.path.exists(image_hint_path):
                            list_file = [f for f in os.listdir(image_hint_path)]
                            question_file_list.append(list_file)
                    elif type_test == 3:
                        image_path = os.path.join(question_file_path, 'image')
                        if os.path.exists(image_path):
                            list_file = [f for f in os.listdir(image_path)]
                            question_file_list.append(list_file)
                        audio_path = os.path.join(question_file_path, 'audio')
                        if os.path.exists(audio_path):
                            list_file = [f for f in os.listdir(audio_path)]
                            question_file_list.append(list_file)
                    else:
                        if os.path.exists(question_file_path):
                            list_file = [f for f in os.listdir(question_file_path)]
                            question_file_list = list_file
                #get answer in folder
                    answer_file_list = list()
                    answer_file_path = os.path.join(settings.BASE_DIR, 'static/courses/', str(part_id), 'test', str(test_info[i].id), str(question_info[j].id), 'answer')
                    if os.path.exists(answer_file_path):
                        answer_file_list = [f for f in os.listdir(answer_file_path)]


                    question_dict["list_filename_question"] = question_file_list
                    question_dict["list_filename_answer"] = answer_file_list

                #get answer type 5
                list_answer = list()
                if test_info[i].type == 5:
                    object_answer = Answer.objects.filter(question_id=question_info[j].id)
                    # list_answer = list()
                    if list_answer is not None:
                        for k in range(0, object_answer.count()):
                            # index_answer = "answer_" + str(i+1)
                            list_answer.append(object_answer[k].answer)
                question_dict["list_answer"] = list_answer
                question_list.append(question_dict)
        context = {
            'lesson_list': part_list,
            'test_list': test_list,
            'question_list': question_list
        }
        return context


class CourseList:
    id = 'id'
    name = 'name'
    level = 'lesson_id'
    update_date = 'update'
    level_name = 'level_name'
    order = 'lesson_order'
    test_number = 'test_number'