
import os
from default.models.models import *
from default.config.common_config import *
from django.db.models import Q
from default.config.config_common import *
from collections import OrderedDict
from cashflow import settings



class CourseListLogic:

    @staticmethod
    def get_lesson_dict(user_id, course_id):
        """
        Get list of lesson base on use
        :type user_id: int
        :param user_id:
        :rtype: dict
        :return:
        """
        levels = Level.objects.filter(course_id=course_id).order_by('order')
        levels_dict = OrderedDict()
        level_ids = Level.objects.filter(course_id=course_id).values_list('id', flat=True)
        base_user_levels = BaseUserLevel.objects.filter(user_id=user_id)

        base_user_levels_dict = {}
        for base_user_level in base_user_levels:
            base_user_levels_dict[base_user_level.level_id] = base_user_level.is_done


        lessons = Lesson.objects.filter(level_id__in=level_ids).order_by('order')
        base_user_lessons = BaseUserLesson.objects.filter(user_id=user_id)
        base_user_lessons_dict = {}
        for base_user_lesson in base_user_lessons:
            base_user_lessons_dict[base_user_lesson.lesson_id] = base_user_lesson

        base_user_parts = BaseUserPart.objects.filter(user_id=user_id)
        base_user_parts_dict = {}
        for base_user_part in base_user_parts:
            base_user_parts_dict[base_user_part.part_id] = base_user_part

        for level in levels:
            levels_dict[level.id] = dict()
            levels_dict[level.id]['id'] = level.id
            levels_dict[level.id]['name'] = level.name
            levels_dict[level.id]['lessons'] = []
            if level.id in base_user_levels_dict:
                if base_user_levels_dict[level.id] == 1:
                    levels_dict[level.id]['state'] = LessonState.Success.code
                else:
                    levels_dict[level.id]['state'] = LessonState.Unlocked.code

            else:
                levels_dict[level.id]['state'] = LessonState.Locked.code

            levels_dict[level.id]['order'] = level.order

        for lesson in lessons:
            lesson_dict = dict()
            lesson_dict['id'] = lesson.id
            lesson_dict['name'] = lesson.name
            if lesson.id in base_user_lessons_dict:
                if base_user_lessons_dict[lesson.id].is_done == 1:
                    lesson_dict['state'] = LessonState.Success.code
                else:
                    lesson_dict['state'] = LessonState.Unlocked.code
            else:
                lesson_dict['state'] = LessonState.Locked.code
            lesson_dict['parts'] = []

            parts = Part.objects.filter(lesson_id=lesson.id).order_by('order')
            for part in parts:
                part_dict = dict()
                part_dict['id'] = part.id
                part_dict['name'] = part.name
                part_dict['content'] = part.content
                part_dict['order'] = part.order
                if part.id in base_user_parts_dict:
                    if base_user_parts_dict[part.id] == 1:
                        part_dict['state'] = LessonState.Success.code
                    else:
                        part_dict['state'] = LessonState.Unlocked.code
                else:
                    part_dict['state'] = LessonState.Locked.code

                lesson_dict['parts'].append(part_dict)
            levels_dict[lesson.level_id]['lessons'].append(lesson_dict)

        return levels_dict

    @staticmethod
    def get_user_part_dict(user_id):
        """
        :type user_id: int
        :param user_id:
        :rtype: dict
        :return: 
        """
        user_parts = BaseUserPart.objects.filter(user_id=user_id)
        user_parts_dict = {}
        for user_part in user_parts:
            user_parts_dict[user_part.part_id] = user_part.is_done

        return user_parts_dict

    @staticmethod
    def get_user_test_dict(user_id, part_id):
        user_dicts = {}
        user_tests = BaseUserStep.objects.filter(Q(user_id=user_id) & Q(part_id=part_id)) \
            .order_by('-is_done', 'right_number_question', 'right_percent', '-id')

        for user_test in user_tests:
            if user_test.test_id not in user_dicts:
                user_dicts[user_test.test_id] = dict()
                user_dicts[user_test.test_id]['right_percent'] = user_test.right_percent
                user_dicts[user_test.test_id]['right_number_question'] = user_test.right_number_question
                user_dicts[user_test.test_id]['is_done'] = user_test.is_done
            else:
                if user_dicts[user_test.test_id]['is_done'] > user_test.is_done:
                    continue
                else:
                    if user_dicts[user_test.test_id]['right_percent'] < user_test.right_percent:
                        user_dicts[user_test.test_id]['right_percent'] = user_test.right_percent
                        user_dicts[user_test.test_id]['right_number_question'] = user_test.right_number_question
                        user_dicts[user_test.test_id]['is_done'] = user_test.is_done
                    elif user_dicts[user_test.test_id]['right_percent'] == user_test.right_percent:
                        if user_dicts[user_test.test_id]['right_number_question'] < user_test.right_number_question:
                            user_dicts[user_test.test_id]['right_percent'] = user_test.right_percent
                            user_dicts[user_test.test_id]['right_number_question'] = user_test.right_number_question
                            user_dicts[user_test.test_id]['is_done'] = user_test.is_done
        return user_dicts

    @staticmethod
    def get_part_content_dict(part_id, user_id):
        """
        :type part_id: int
        :param part_id:
        :type user_id: int
        :param user_id:
        :rtype: dict
        :return:
        """
        part_content = {}

        part = Part.objects.get(id=part_id)
        user_lesson = BaseUserPart.objects.get(Q(part_id=part_id) & Q(user_id=user_id))
        tests = Test.objects.filter(part_id=part_id)

        user_dicts = CourseListLogic.get_user_test_dict(user_id, part_id)

        test_list = []
        for index, test in enumerate(tests):
            test_dict = dict()
            if test.name is not None:
                test_dict['name'] = 'Step ' + str(index + 2)+': ' + str(test.name) + ' [ ' + str(test.question_number_goal) + ' ' \
                                + str(test.question_percent_goal) + '% ]'
            else:
                test_dict['name'] = 'Step ' + str(index + 2)+': Test' + ' [ ' + str(test.question_number_goal) + ' ' \
                                + str(test.question_percent_goal) + '% ]'
            test_dict['question_number_goal'] = test.question_number_goal
            test_dict['question_percent_goal'] = test.question_percent_goal
            test_dict['id'] = test.id
            if test.id in user_dicts:
                right_percent = user_dicts[test.id]['right_percent']
                right_number = user_dicts[test.id]['right_number_question']

                if right_percent >= test.question_percent_goal:
                    test_dict['is_percent_question_passed'] = True
                else:
                    test_dict['is_percent_question_passed'] = False

                if right_number >= test.question_number_goal:
                    test_dict['is_right_question_passed'] = True
                else:
                    test_dict['is_right_question_passed'] = False
                test_dict['right_question'] = right_number
                test_dict['percent'] = right_percent
                test_dict['is_done'] = user_dicts[test.id]['is_done']
            else:
                test_dict['is_right_question_passed'] = False
                test_dict['is_percent_question_passed'] = False
                test_dict['right_question'] = 0
                test_dict['percent'] = 0
                test_dict['is_done'] = TestResult.Failed.code
            test_list.append(test_dict)

        part_content['lesson_name'] = part.name
        if user_lesson.video == 1:
            part_content['video_state'] = True
        else:
            part_content['video_state'] = False
        part_content['tests'] = test_list
        part_content['part_id'] = part_id
        part_content['lesson'] = part.lesson_id

        return part_content

    @staticmethod
    def get_video_path(part_id):
        current_part = Part.objects.get(pk=part_id)
        upload_video_path = settings.MEDIA_URL + str(part_id) + '/video/{0}'.format(current_part.video)
        return upload_video_path

    @staticmethod
    def get_user_courses_ids(user_id):
        user_coures_id = BaseUserCourse.objects.filter(user_id=user_id).values_list('course_id', flat=True)
        return user_coures_id

    @staticmethod
    def get_user_courses_dict(user_id):
        user_courses_id = CourseListLogic.get_user_courses_ids(user_id)
        user_courses = Course.objects.filter(id__in=user_courses_id).order_by('order')
        user_courses_dict = OrderedDict()
        for user_course in user_courses:
            user_course_dict = dict()
            user_course_dict['name'] = user_course.name.upper()
            user_course_dict['content'] = user_course.content
            user_course_dict['id'] = user_course.id
            user_courses_dict[user_course.id] = user_course_dict
        return user_courses_dict

    @staticmethod
    def get_next_id(current_id, next_level_id, level_type):
        if level_type == LevelType.Part:
            current_ids = Part.objects.filter(lesson_id=next_level_id).order_by('-order').values_list('id', flat=True)
        elif level_type == LevelType.Lesson:
            current_ids = Lesson.objects.filter(leve_id=next_level_id).order_by('-order').values_list('id', flat=True)
        elif level_type == LevelType.Level:
            current_ids = Level.objects.filter(course_id=next_level_id).order_by('-order').values_list()
        elif level_type == LevelType.Course:
            user_course_ids = BaseUserCourse.objects.filter(user_id=next_level_id).values_list('course_id', flat=True)
            current_ids = Course.objects.filter(id__in=user_course_ids).order_by('-order').values_list('id', flat=True)

        if current_ids.index(current_id) == 0:
            return None
        else:
            return current_ids[current_ids.index(current_id)-1]

    @staticmethod
    def get_lesson_content_dict(lesson_id, user_id):
        parts = Part.objects.fitler(lesson_id=lesson_id)
        part_ids = parts.values_list('id', flat=True)
        base_user_parts = BaseUserPart.objects.filter(user_id=user_id, part_id__in=part_ids)
        base_user_part_dict = {}
        for base_user_part in base_user_parts:
            base_user_part_dict[base_user_part.part_id] = base_user_part.is_done
        current_lesson = Lesson.objects.get(pk=lesson_id)
        lesson_dict = dict()
        lesson_dict['level'] = current_lesson.level_id
        lesson_dict['parts'] = []

        for part in parts:
            part_dict = {}
            if part.id in base_user_part_dict:
                part_dict['is_done'] = base_user_part_dict[part.id]
            else:
                part_dict['is_done'] = TestResult.Failed.code

            lesson_dict['parts'].append(part_dict)
        return lesson_dict

    @staticmethod
    def get_level_content_dict(level_id, user_id):
        lessons = Lesson.objects.filter(level_id=level_id)
        lessons_ids = lessons.values_list('id', flat=True)
        base_user_lessons = BaseUserLesson.objects.filter(user_id=user_id, lesson_id__in=lessons_ids)
        base_user_lessons_dict = {}
        for base_user_lesson in base_user_lessons:
            base_user_lessons_dict[base_user_lesson.lesson_id] = base_user_lesson.is_done

        level = Level.objects.get(pk=level_id)
        level_dict = {}
        level_dict['course'] = level.course_id
        level_dict['lessons'] = []
        for lesson in lessons:
            lesson_dict = {}
            if lesson.id in base_user_lessons_dict:
                lesson_dict['is_done'] = base_user_lessons_dict[lesson.id]
            else:
                lesson_dict['is_done'] = TestResult.Failed.code
            level_dict['lessons'].append(level_dict)

        return level_dict

    @staticmethod
    def get_course_content_dict(course_id, user_id):
        levels = Level.objects.filter(course_id=course_id)
        levels_ids = levels.values_list('id', flat=True)
        base_user_levels = BaseUserLevel.objects.filter(user_id=user_id, level_id__in=levels_ids)
        base_user_levels_dict = {}
        for base_user_level in base_user_levels:
            base_user_levels_dict[base_user_level.id] = base_user_level.is_done
        levels_dict = {}
        levels_dict['levels'] = []
        for level in levels:
            level_dict = {}
            if level.id in base_user_levels_dict:
                level_dict['is_done'] =  base_user_levels_dict[level.id]
            else:
                level_dict['is_done'] = TestResult.Failed.code
            levels_dict['levels'].append(level_dict)

        return levels_dict




