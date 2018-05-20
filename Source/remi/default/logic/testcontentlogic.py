import os
from cashflow import settings
import random
from random import randint
from default.config.common_config import *
from default.models.models import *
from random import shuffle
from default.logic.courselistlogic import *
from default.logic.createcourselogic import *
from django.core.exceptions import ObjectDoesNotExist


class TestContentLogic:
    @staticmethod
    def create_options_dict(test_type, test_id, current_question_id):
        sames = [QuestionType.Type1.code, QuestionType.Type2.code,
                 QuestionType.Type3.code, QuestionType.Type8.code]
        if test_type in sames:
            test_question_map = \
                TestContentLogic.get_test_question_dict_type_1238(
                    test_id, current_question_id, test_type
                )
        elif test_type == QuestionType.Type4.code:
            test_question_map = TestContentLogic.get_test_question_dict_type_4(
                test_id, current_question_id)
        elif test_type == QuestionType.Type5.code:
            test_question_map = TestContentLogic.get_test_question_dict_type_5(
                test_id, current_question_id)
        elif test_type == QuestionType.Type6.code:
            test_question_map = TestContentLogic.get_test_question_dict_type_6(
                test_id, current_question_id)
        elif test_type == QuestionType.Type7.code:
            test_question_map = TestContentLogic.get_test_question_dict_type_7(
                test_id, current_question_id)

        return test_question_map

    @staticmethod
    def create_audio_url(lesson_id, question_id):
        """
        :type lesson_id: int
        :param lesson_id:
        :type question_id: int
        :param question_id:
        :return:
        """
        return "lesson/{0}/question/{1}/audio.mp3".format(lesson_id,
                                                          question_id)

    @staticmethod
    def get_test_question_dict_type_4(test_id, current_question_id):
        """
        :param current_question_id:
        :param test_id:
        :return:
        """
        number_options = 1
        test_questions = Question.objects.filter(test_id=test_id).values_list(
            'id', flat=True)
        test_questions_list = []
        for id in test_questions:
            if id != current_question_id:
                test_questions_list.append(id)

        if len(test_questions_list) == 0:
            next_question_id = current_question_id
        else:
            next_question_id = random.choice(test_questions_list)
        print(next_question_id)
        next_question = Question.objects.get(id=next_question_id)

        options_dict = dict()
        options_dict['answer'] = next_question.answer
        options_dict[
            'question'] = settings.MEDIA_URL + "{0}/test/{1}/{2}/question/{3}"\
            .format(next_question.lesson, test_id,
                    next_question.id, next_question.question
                    )

        return options_dict, number_options, next_question_id

    @staticmethod
    def get_test_question_dict_type_6(test_id, current_question_id):
        """
        :param current_question_id:
        :param test_id:
        :return:
        """
        number_options = 1
        test_questions = Question.objects.filter(test_id=test_id).values_list(
            'id', flat=True)
        test_questions_list = []
        for id in test_questions:
            if id != current_question_id:
                test_questions_list.append(id)

        if len(test_questions_list) == 0:
            next_question_id = current_question_id
        else:
            next_question_id = random.choice(test_questions_list)
        print(next_question_id)
        next_question = Question.objects.get(id=next_question_id)
        options_dict = dict()
        image_path = os.path.join(settings.BASE_DIR,
                                  settings.MEDIA_URL_RELATIVE,
                                  str(next_question.part_id), 'test',
                                  str(test_id),
                                  str(next_question.id), 'question', 'image')
        image_file_names = os.listdir(image_path)
        if len(image_file_names) > 0:
            options_dict[
                'image_url'] = settings.MEDIA_URL \
                               + "{0}/test/{1}/{2}/question/image/{3}".format(
                next_question.part_id, test_id,
                str(next_question.id),
                image_file_names[0])
        audio_path = os.path.join(settings.BASE_DIR,
                                  settings.MEDIA_URL_RELATIVE,
                                  str(next_question.part_id), 'test',
                                  str(test_id),
                                  str(next_question.id), 'question', 'audio')
        audio_files = os.listdir(audio_path)
        if len(audio_files) > 0:
            options_dict[
                'audio_url'] = settings.MEDIA_URL \
                               + "{0}/test/{1}/{2}/question/audio/{3}".format(
                next_question.part_id,
                test_id,
                next_question.id, audio_files[0])
        image_hint_path = os.path.join(settings.BASE_DIR,
                                       settings.MEDIA_URL_RELATIVE,
                                       str(next_question.part_id), 'test',
                                       str(test_id),
                                       str(next_question.id), 'question',
                                       'image_hint')
        image_hint_files = os.listdir(image_hint_path)
        if len(image_hint_files) > 0:
            options_dict[
                'image_hint_url'] = settings.MEDIA_URL \
                                    + "{0}/test/{1}/{2}/question/image_hint/{3}".format(
                next_question.part_id, test_id,
                next_question.id, image_hint_files[0])

        return options_dict, number_options, next_question_id

    @staticmethod
    def get_test_question_dict_type_7(test_id, current_question_id):
        """
        :param current_question_id:
        :param test_id:
        :return:
        """
        number_options = 1
        test_questions = Question.objects.filter(test_id=test_id).values_list(
            'id', flat=True)
        test_questions_list = []
        for id in test_questions:
            if id != current_question_id:
                test_questions_list.append(id)

        if len(test_questions_list) == 0:
            next_question_id = current_question_id
        else:
            next_question_id = random.choice(test_questions_list)
        print(next_question_id)
        next_question = Question.objects.get(id=next_question_id)

        options_dict = dict()

        video_path = os.path.join(settings.BASE_DIR,
                                  settings.MEDIA_URL_RELATIVE,
                                  str(next_question.part_id), 'test',
                                  str(test_id),
                                  str(next_question.id), 'question', 'video')
        video_files = os.listdir(video_path)
        if len(video_files) > 0:
            options_dict[
                'video_url'] = settings.MEDIA_URL + "{0}/test/{1}/{2}/question/video/{3}".format(
                next_question.part_id,
                test_id,
                next_question.id,
                video_files[0])

        image_hint_path = os.path.join(settings.BASE_DIR,
                                       settings.MEDIA_URL_RELATIVE,
                                       str(next_question.part_id), 'test',
                                       str(test_id),
                                       str(next_question.id), 'question',
                                       str(next_question.question),
                                       'image_hint')
        image_hint_path_files = os.listdir(image_hint_path)
        if len(image_hint_path_files) > 0:
            options_dict[
                'image_hint_url'] = settings.MEDIA_URL + "{0}/test/{1}/{2}/question/image_hint/{3}".format(
                next_question.part_id,
                test_id,
                next_question.id,
                image_hint_path_files[0])

        return options_dict, number_options, next_question_id

    @staticmethod
    def get_test_question_dict_type_8(test_id, current_question_id):
        """
        :param current_question_id:
        :param test_id:
        :return:
        """
        number_options = 4
        number_options = random.choice(CommonConfig.NumberAnswerOptions)

        test_questions = Question.objects.filter(test_id=test_id).values_list(
            'id', flat=True)
        test_questions_list = []
        for test_question_id in test_questions:
            if test_question_id != current_question_id:
                test_questions_list.append(test_question_id)

        if len(test_questions_list) == 0:
            next_question_id = current_question_id
        else:
            next_question_id = random.choice(test_questions_list)

        next_question = Question.objects.get(id=next_question_id)
        option_list = []

        right_option = dict()
        right_option[
            'url'] = settings.MEDIA_URL + "{0}/test/{1}/{2}/answer/{3}".format(
            next_question.part_id, test_id,
            next_question.id,
            next_question.answer)
        right_option['right'] = 1
        options_path = os.path.join(settings.BASE_DIR,
                                    settings.MEDIA_URL_RELATIVE,
                                    str(next_question.part_id), 'test',
                                    str(test_id),
                                    str(next_question.id), 'answer')
        options_files = os.listdir(options_path)
        options_files.remove(next_question.answer)

        for option_file in options_files:
            option = dict()
            option[
                'url'] = settings.MEDIA_URL + "{0}/test/{1}/{2}/answer/{3}".format(
                next_question.part_id, test_id,
                next_question.id,
                option_file)
            option['right'] = 0
            option_list.append(option)

        option_list.insert(randint(0, number_options - 1), right_option)
        options_dict = dict()
        options_dict['options'] = option_list

        audio_file_path = os.path.join(settings.BASE_DIR,
                                       settings.MEDIA_URL_RELATIVE + "{0}/test/{1}/{2}/question".format(
                                           next_question.part_id,
                                           test_id, next_question.id))
        audio_files = os.listdir(audio_file_path)[0]
        image_question_path = os.path.join(settings.BASE_DIR,
                                           settings.MEDIA_URL_RELATIVE + "{0}/test/{1}/{2}/question".format(
                                               next_question.part_id,
                                               test_id,
                                               next_question.id))
        image_question_file = os.listdir(image_question_path)[0]
        options_dict[
            'question_audio_url'] = settings.MEDIA_URL + "{0}/test/{1}/{2}/question/video/{3}".format(
            next_question.part_id,
            test_id, next_question.id, audio_files)
        options_dict[
            'questions_url'] = settings.MEDIA_URL + "{0}/test/{1}/{2}/question/image/{3}".format(
            next_question.part_id,
            test_id,
            next_question.id,
            image_question_file)
        return options_dict, number_options, next_question_id

    @staticmethod
    def get_test_question_dict_type_5(test_id, current_question_id):
        number_options = 4
        test_questions = Question.objects.filter(test_id=test_id).values_list(
            'id', flat=True)
        test_questions_list = []
        for test_question_id in test_questions:
            if test_question_id != current_question_id:
                test_questions_list.append(test_question_id)

        if len(test_questions_list) == 0:
            next_question_id = current_question_id
        else:
            next_question_id = random.choice(test_questions_list)
        print(next_question_id)
        next_question = Question.objects.get(id=next_question_id)
        question_dict = dict()
        question_dict['question'] = next_question.question
        question_dict['options'] = []
        answers = Answer.objects.filter(question_id=next_question_id)
        for answer in answers:
            answer_dict = dict()
            answer_dict['content'] = answer.answer
            answer_dict['right'] = 0
            if int(next_question.answer) == int(answer.id):
                answer_dict['right'] = 1
            question_dict['options'].append(answer_dict)
        shuffle(question_dict['options'])
        return question_dict, number_options, next_question_id

    @staticmethod
    def get_test_question_dict_type_1238(test_id, current_question_id,
                                         current_test_type):
        """

        :param test_id:
        :return:
        """
        number_options = 4
        if current_test_type == QuestionType.Type1.code:
            number_options = random.choice(CommonConfig.NumberAnswerOptions)

        test_questions = Question.objects.filter(test_id=test_id).values_list(
            'id', flat=True)
        test_questions_list = []
        for test_question_id in test_questions:
            if test_question_id != current_question_id:
                test_questions_list.append(test_question_id)

        if len(test_questions_list) == 0:
            next_question_id = current_question_id
        else:
            next_question_id = random.choice(test_questions_list)

        next_question = Question.objects.get(id=next_question_id)
        option_list = []

        right_option = dict()
        right_option[
            'url'] = settings.MEDIA_URL + "{0}/test/{1}/{2}/answer/{3}".format(
            next_question.part_id, test_id, next_question.id,
            next_question.answer)
        right_option['right'] = 1
        options_path = os.path.join(settings.BASE_DIR,
                                    settings.MEDIA_URL.replace('/', ''),
                                    str(next_question.part_id), 'test',
                                    str(test_id),
                                    str(next_question.id), 'answer')
        options_files = os.listdir(options_path)
        options_files.remove(next_question.answer)

        for option_file in options_files:
            option = dict()
            option[
                'url'] = settings.MEDIA_URL + "{0}/test/{1}/{2}/answer/{3}".format(
                next_question.part_id, test_id, next_question.id,
                option_file)
            option['right'] = 0
            option_list.append(option)

        option_list.insert(randint(0, number_options - 1), right_option)
        options_dict = dict()
        options_dict['options'] = option_list
        if current_test_type == QuestionType.Type1.code:
            options_dict[
                'questions_url'] = settings.MEDIA_URL + "{0}/test/{1}/{2}/question/{3}".format(
                next_question.part_id, test_id,
                next_question.id, next_question.question)
        elif current_test_type == QuestionType.Type2.code or current_test_type == QuestionType.Type8.code:
            options_dict[
                'questions_url'] = settings.MEDIA_URL + "{0}/test/{1}/{2}/question/{3}".format(
                next_question.part_id,
                test_id, next_question.id, next_question.question)
        if current_test_type == QuestionType.Type3.code:
            audio_file_path = os.path.join(settings.BASE_DIR,
                                           settings.MEDIA_URL_RELATIVE + "{0}/test/{1}/{2}/question".format(
                                               next_question.part_id,
                                               test_id, next_question.id),
                                           "audio")
            audio_files = os.listdir(audio_file_path)[0]
            image_question_path = os.path.join(settings.BASE_DIR,
                                               settings.MEDIA_URL_RELATIVE + "{0}/test/{1}/{2}/question".format(
                                                   next_question.part_id,
                                                   test_id, next_question.id),
                                               "image")
            image_question_file = os.listdir(image_question_path)[0]
            options_dict[
                'question_audio_url'] = settings.MEDIA_URL \
                                        + "{0}/test/{1}/{2}/question/audio/{3}".format(
                next_question.part_id,
                test_id, next_question.id, audio_files)
            options_dict[
                'questions_url'] = settings.MEDIA_URL \
                                   + "{0}/test/{1}/{2}/question/image/{3}".format(
                next_question.part_id,
                test_id, next_question.id,
                image_question_file)
        return options_dict, number_options, next_question_id

    @staticmethod
    def get_base_level_lesson_ids(level_ids):
        lesson_ids = []
        for level_id in level_ids:
            lessons = Lesson.objects.filter(level=level_id).order_by('order')
            if len(lessons) == 0:
                continue
            for lesson in lessons:
                lesson_ids.append(lesson.id)
            return lesson_ids
        return None

    @staticmethod
    def get_level_lesson_ids(level_id):
        lesson_ids = []
        lessons = Lesson.objects.filter(level=level_id).order_by('order')
        for lesson in lessons:
            lesson_ids.append(lesson.id)
        return lesson_ids

    @staticmethod
    def get_part_order_ids(lesson_id):
        parts = Part.objects.filter(lesson_id=lesson_id).order_by('order')
        orders = []
        for part in parts:
            orders.append(part.order)

        return orders

    @staticmethod
    def get_lesson_order(level_id):
        lessons = Lesson.objects.filter(level_id=level_id).order_by('order')
        orders = []
        for lesson in lessons:
            orders.append(lesson.order)
        return orders

    @staticmethod
    def get_level_order(course_id):
        levels = Level.objects.filter(course_id=course_id).order_by('order')
        orders = []
        for level in levels:
            orders.append(level.order)
        return orders

    @staticmethod
    def get_course_order():
        courses = Course.objects.all()
        orders = []
        for course in courses:
            orders.append(course.order)
        return orders

    @staticmethod
    def check_lesson_status(user_id, current_part_id=None):
        """
        Get user test list
        # If all done -> set is_done in base_student_lesson table to 1
        # Create new record in base_student_lesson for next order lesson
        :param user_id:
        :param current_part_id:
        :return:
        """
        if current_part_id is None:
            current_user = User.objects.get(pk=user_id)
            base_user_courses = BaseUserCourse.objects.filter(user_id=user_id)
            course_ids = Course.objects.all().order_by('order').values_list(
                'id', flat=True)
            if len(base_user_courses) > 0:
                base_user_levels = BaseUserLevel.objects.filter(
                    user_id=user_id)
                if len(base_user_levels) > 0:
                    return

                level_ids = Level.objects.filter(
                    course_id=course_ids[0]).order_by('order').values_list(
                    'id', flat=True)
                if len(level_ids) > 0:
                    new_base_user_level = BaseUserLevel()
                    new_base_user_level.user = current_user
                    new_base_user_level.level = Level.objects.get(
                        pk=level_ids[0])
                    new_base_user_level.is_done = TestResult.Failed.code
                    new_base_user_level.save()
                    lesson_ids = Lesson.objects.filter(
                        level_id=level_ids[0]).order_by('order').values_list(
                        'id', flat=True)
                    if len(lesson_ids) > 0:
                        new_base_user_lesson = BaseUserLesson()
                        new_base_user_lesson.user = current_user
                        new_base_user_lesson.lesson = Lesson.objects.get(
                            pk=lesson_ids[0])
                        new_base_user_lesson.is_done = TestResult.Failed.code
                        new_base_user_lesson.save()

                        part_ids = Part.objects.filter(
                            lesson_id=lesson_ids[0]).order_by(
                            'order').values_list('id', flat=True)
                        if len(part_ids) > 0:
                            base_user_part = BaseUserPart()
                            base_user_part.is_done = TestResult.Failed.code
                            base_user_part.user = current_user
                            base_user_part.part = Part.objects.get(
                                pk=part_ids[0])
                            base_user_part.video = TestResult.Failed.code
                            base_user_part.save()
                        return
                    return
                return
            return
        # Check parts user state
        part_contents_dict = CourseListLogic.get_part_content_dict(
            current_part_id, user_id)
        user_tests = part_contents_dict['tests']
        for test in user_tests:
            if test['is_done'] == TestResult.Failed.code:
                return
        base_user_part = BaseUserPart.objects.get(part_id=current_part_id)
        base_user_part.is_done = TestResult.Done.code
        base_user_part.save()

        current_user = User.objects.get(pk=user_id)
        # Get all lesson part, order by order
        # Get next_id
        current_lesson_id = part_contents_dict['lesson']
        next_part_id = CourseListLogic.get_next_id(current_part_id,
                                                   current_lesson_id,
                                                   LevelType.Part)
        if next_part_id is not None:
            next_base_user_part = BaseUserPart()
            next_base_user_part.part = Part.ojbects.get(pk=next_part_id)
            next_base_user_part.is_done = TestResult.Failed.code
            next_base_user_part.user = current_user
            next_base_user_part.video = TestResult.Failed.code
            next_base_user_part.save()
            return

        # Check lesson user state

        lessons_content_dict = CourseListLogic.get_lesson_content_dict(
            current_lesson_id, user_id
        )
        for user_part in lessons_content_dict['parts']:
            if user_part['is_done'] == TestResult.Failed.code:
                return
        base_user_lesson = BaseUserLesson.objects.get(
            lesson_id=current_lesson_id
        )
        base_user_lesson.is_done = TestResult.Done.code
        base_user_lesson.save()

        current_level_id = lessons_content_dict['level']
        next_lesson_id = CourseListLogic.get_next_id(
            current_lesson_id, current_level_id, LevelType.Lesson
        )
        if next_lesson_id is not None:
            next_base_user_lesson = BaseUserLesson()
            next_base_user_lesson.user = current_user
            next_base_user_lesson.lesson = Lesson.objects.get(
                pk=next_lesson_id)
            next_base_user_lesson.is_done = TestResult.Failed.code
            next_base_user_lesson.save()
            return

        # Check level user state
        levels_content_dict = CourseListLogic.get_level_content_dict(
            current_level_id, user_id)
        for user_lesson in levels_content_dict['lessons']:
            if user_lesson['is_done'] == TestResult.Failed.code:
                return
        base_user_level = BaseUserLevel.objects.get(level_id=current_level_id)
        base_user_level.is_done = TestResult.Done.code
        base_user_level.save()

        current_course_id = levels_content_dict['course']
        next_level_id = CourseListLogic.get_next_id(current_level_id,
                                                    current_course_id,
                                                    LevelType.Level)
        if next_level_id is not None:
            next_base_user_level = BaseUserLevel()
            next_base_user_level.is_done = TestResult.Failed.code
            next_base_user_level.level = Level.objects.get(pk=next_level_id)
            next_base_user_level.user = current_user
            next_base_user_level.save()
            return

        # Check course user state
        courses_content_dict = CourseListLogic.get_course_content_dict(
            current_course_id, user_id)
        for user_level in courses_content_dict['levels']:
            if user_level['is_done'] == TestResult.Failed.code:
                return

        base_user_course = BaseUserCourse.objects.get(
            course_id=current_course_id)
        base_user_course.is_done = TestResult.Done.code
        base_user_course.save()

        next_course_id = CourseListLogic.get_next_id(current_course_id,
                                                     user_id, LevelType.Course)
        if next_course_id is not None:
            next_base_user_course = BaseUserCourse.objects.get(
                course_id=next_course_id)
            next_base_user_course.is_done = TestResult.Failed.code
            next_base_user_course.save()
            return
