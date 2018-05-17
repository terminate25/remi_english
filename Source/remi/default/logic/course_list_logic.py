import os
from default.models.models import (Level, BaseUserLevel,
                                   BaseUserLesson,
                                   Lesson, BaseUserPart,
                                   Part, BaseUserStep,
                                   Course, BaseUserCourse,
                                   Test)

from default.config.common_config import (CommonState,
                                          LevelType,
                                          BaseUserRowState)
from django.db.models import Q
from default.config.config_common import TestResult
from collections import OrderedDict
from cashflow import settings


class CourseListLogic:

    @classmethod
    def get_course_content(cls, user_id, course_id):
        """
        Get list of lesson base on use
        :param user_id:
        :param course_id:
        :rtype: dict
        :return:
        """
        # course => level => lesson => part => test => question + answer
        # Get level list by course id
        level_list = Level.objects\
            .filter(course_id=course_id).order_by('order')
        # Get base user level state (done or not)
        user_level_dict = cls.__get_user_level_state_dict(user_id)

        course_level_dict = OrderedDict()
        for level in level_list:
            course_level_dict[level.id] = dict()
            course_level_dict[level.id]['id'] = level.id
            course_level_dict[level.id]['name'] = level.name
            course_level_dict[level.id]['state'] = \
                cls.__get_base_user_table_state(level.id, user_level_dict)
            course_level_dict[level.id]['order'] = level.order
            course_level_dict[level.id]['lessons'] = \
                cls.__get_level_lesson_list(user_id, level.id)
        return course_level_dict

    @classmethod
    def __get_level_lesson_list(cls, user_id, level_id):

        # Get base user lesson dict { lesson_id : lesson_data_obj }
        user_lesson_dict = cls.__get_user_lesson_state_dict(user_id)
        # Get lessons from database by lesson id
        lesson_list = Lesson.objects.filter(level_id=level_id).order_by(
            'order')
        lesson_level_list = []
        for lesson in lesson_list:
            lesson_dict = dict()
            lesson_dict['id'] = lesson.id
            lesson_dict['name'] = lesson.name
            lesson_dict['state'] = cls.__get_base_user_table_state(
                lesson.id, user_lesson_dict
            )
            lesson_dict['parts'] = cls.__get_lesson_part_list(
                lesson.id, user_id
            )
            lesson_level_list.append(lesson_dict)
        return lesson_level_list

    @classmethod
    def __get_lesson_part_list(cls, lesson_id, user_id):
        # Get base user part dict { part_id: user_part_obj }
        user_part_dict = cls.__get_user_part_state_dict(user_id)
        # Get parts from database by lesson id
        part_list = Part.objects.filter(lesson_id=lesson_id).order_by('order')
        # Create list of part_dict
        lesson_part_list = []
        for part in part_list:
            part_dict = dict()
            part_dict['id'] = part.id
            part_dict['name'] = part.name
            part_dict['content'] = part.content
            part_dict['order'] = part.order
            part_dict['state'] = cls.__get_base_user_table_state(
                part.id, user_part_dict
            )
            lesson_part_list.append(part_dict)
        return lesson_part_list

    @classmethod
    def __get_base_user_table_state(cls, target_id, target_dict):
        if target_id in target_dict:
            if target_dict[target_id] == BaseUserRowState.Passed.code:
                return CommonState.Success.code
            else:
                return CommonState.Unlocked.code
        return CommonState.Locked.code

    @classmethod
    def __get_user_level_state_dict(cls, user_id):
        """
        Get user level state dict -> van chua biet lam qq gi
        :param user_id:
        :return:
        """
        # Get base user level from database
        user_level_dict = {}
        user_levels = BaseUserLevel.objects.filter(user_id=user_id)
        for ret in user_levels:
            user_level_dict[ret.level_id] = ret.is_done

        return user_level_dict

    @classmethod
    def __get_user_lesson_state_dict(cls, user_id):
        """
        Get user lesson dict
        :param user_id:
        :return:
        """
        usr_lesson_dict = {}
        usr_lessons = BaseUserLesson.objects.filter(user_id=user_id)
        for usr_lesson in usr_lessons:
            usr_lesson_dict[usr_lesson.lesson_id] = usr_lesson.is_done

        return usr_lesson_dict

    @classmethod
    def __get_user_part_state_dict(cls, user_id):
        """
        Get base user part dict
        :param user_id:
        :return:
        """
        usr_part_dict = {}

        usr_parts = BaseUserPart.objects.filter(user_id=user_id)
        for usr_part in usr_parts:
            usr_part_dict[usr_part.part_id] = usr_part.is_done

        return usr_part_dict

    @staticmethod
    def get_user_test_dict(user_id, part_id):
        u_dicts = {}
        u_tests = BaseUserStep.objects.filter(
            Q(user_id=user_id) & Q(part_id=part_id)) \
            .order_by('-is_done', 'right_number_question', 'right_percent',
                      '-id')

        for u_test in u_tests:
            if u_test.test_id not in u_dicts:
                u_dicts[u_test.test_id] = dict()
                u_dicts[u_test.test_id]['right_percent'] = u_test.right_percent
                u_dicts[u_test.test_id]['right_number_question'] = \
                    u_test.right_number_question
                u_dicts[u_test.test_id]['is_done'] = u_test.is_done
            else:
                if u_dicts[u_test.test_id]['is_done'] > u_test.is_done:
                    continue
                else:
                    if u_dicts[u_test.test_id][
                        'right_percent'
                    ] < u_test.right_percent:

                        u_dicts[u_test.test_id]['right_percent'] \
                            = u_test.right_percent

                        u_dicts[u_test.test_id]['right_number_question'] \
                            = u_test.right_number_question

                        u_dicts[u_test.test_id]['is_done'] = u_test.is_done

                    elif u_dicts[u_test.test_id]['right_percent'] \
                            == u_test.right_percent:
                        if u_dicts[u_test.test_id][
                            'right_number_question'
                        ] < u_test.right_number_question:
                            u_dicts[u_test.test_id]['right_percent'] = \
                                u_test.right_percent

                            u_dicts[u_test.test_id]['right_number_question'] = \
                                u_test.right_number_question

                            u_dicts[u_test.test_id]['is_done'] = u_test.is_done
        return u_dicts

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
        user_lesson = BaseUserPart.objects.get(
            Q(part_id=part_id) & Q(user_id=user_id))
        tests = Test.objects.filter(part_id=part_id)

        user_dicts = CourseListLogic.get_user_test_dict(user_id, part_id)

        test_list = []
        for index, test in enumerate(tests):
            test_dict = dict()
            if test.name is not None:
                test_dict['name'] = 'Step ' + str(index + 2) + ': ' + str(
                    test.name) + ' [ ' + str(test.question_number_goal) + ' ' \
                                    + str(test.question_percent_goal) + '% ]'
            else:
                test_dict['name'] = 'Step ' + str(
                    index + 2) + ': Test' + ' [ ' + str(
                    test.question_number_goal) + ' ' \
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
        upload_video_path = settings.MEDIA_URL + str(
            part_id) + '/video/{0}'.format(current_part.video)
        return upload_video_path

    @staticmethod
    def get_user_courses_ids(user_id):
        user_coures_id = BaseUserCourse.objects.filter(
            user_id=user_id).values_list('course_id', flat=True)
        return user_coures_id

    @staticmethod
    def get_user_courses_dict(user_id):
        user_courses_id = CourseListLogic.get_user_courses_ids(user_id)
        user_courses = Course.objects.filter(
            id__in=user_courses_id).order_by('order')
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
            current_ids = Part.objects.filter(
                lesson_id=next_level_id).order_by('-order')\
                .values_list('id', flat=True)
        elif level_type == LevelType.Lesson:
            current_ids = Lesson.objects.filter(
                leve_id=next_level_id).order_by('-order')\
                .values_list('id', flat=True)
        elif level_type == LevelType.Level:
            current_ids = Level.objects.filter(
                course_id=next_level_id).order_by('-order').values_list()
        elif level_type == LevelType.Course:
            user_course_ids = BaseUserCourse.objects.filter(
                user_id=next_level_id).values_list('course_id', flat=True)
            current_ids = Course.objects.filter(
                id__in=user_course_ids).order_by('-order')\
                .values_list('id', flat=True)

        if current_ids.index(current_id) == 0:
            return None
        else:
            return current_ids[current_ids.index(current_id) - 1]

    @staticmethod
    def get_lesson_content_dict(lesson_id, user_id):
        parts = Part.objects.fitler(lesson_id=lesson_id)
        part_ids = parts.values_list('id', flat=True)
        base_user_parts = BaseUserPart.objects.filter(user_id=user_id,
                                                      part_id__in=part_ids)
        base_user_part_dict = {}
        for base_user_part in base_user_parts:
            base_user_part_dict[
                base_user_part.part_id] = base_user_part.is_done
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
        base_user_lessons = BaseUserLesson.objects.filter(
            user_id=user_id, lesson_id__in=lessons_ids
        )
        base_user_lessons_dict = {}
        for base_user_lesson in base_user_lessons:
            base_user_lessons_dict[
                base_user_lesson.lesson_id] = base_user_lesson.is_done

        level = Level.objects.get(pk=level_id)
        level_dict = dict()
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
        base_user_levels = BaseUserLevel.objects.filter(
            user_id=user_id, level_id__in=levels_ids
        )
        base_user_levels_dict = {}
        for base_user_level in base_user_levels:
            base_user_levels_dict[base_user_level.id] =\
                base_user_level.is_done
        levels_dict = dict()
        levels_dict['levels'] = []
        for level in levels:
            level_dict = {}
            if level.id in base_user_levels_dict:
                level_dict['is_done'] = base_user_levels_dict[level.id]
            else:
                level_dict['is_done'] = TestResult.Failed.code
            levels_dict['levels'].append(level_dict)

        return levels_dict
