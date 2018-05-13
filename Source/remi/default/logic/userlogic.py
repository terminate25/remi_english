# -*- coding: utf-8 -*-

import json

import bcrypt
from django.db.models import Q

from default.config.config_menu import *
from default.config.config_role import *
from default.models.models import *
from middleware.globals import GlobalRequest
from default.config.common_config import *


class UserLogic:

    @staticmethod
    def hash_password(password):
        """
        Encrypt password with bcrypt
        @param password: 
        @return: hashed string
        """
        return bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt(14))

    @staticmethod
    def create_user(user_name, login_name, gender, roles, phone, email, address, teacher, password=None):
        """
        Create user and save to database. Password will hashed
        :param user_name:
        :param login_name:
        :param gender
        :param roles
        :param phone
        :param address
        :param email
        :param teacher
        :param password:
        :return:
        """
        user = User()
        if password is None:
            password = login_name
        user.password = UserLogic.hash_password(password)
        user.login_name = login_name
        user.user_name = user_name
        user.gender = gender
        user.roles = roles
        user.phone = phone
        user.email = email
        user.address = address
        user.teacher_id = teacher
        user.save()
        return user

    @staticmethod
    def store_user_courses(user_id, user_courses):
        for user_course in user_courses:
            base_user_course = BaseUserCourse()
            base_user_course.course = Course.objects.get(pk=user_course)
            base_user_course.user = User.objects.get(pk=user_id)
            base_user_course.is_done = 0
            base_user_course.save()

    @staticmethod
    def update_user_courses(user_id, user_courses):
        user_base_courses = BaseUserCourse.objects.filter(user_id=user_id)
        for user_base_course in user_base_courses:
            user_base_course.delete()
        for user_course in user_courses:
            base_user_course = BaseUserCourse()
            base_user_course.course = Course.objects.get(pk=user_course)
            base_user_course.user = User.objects.get(pk=user_id)
            base_user_course.save()

    @staticmethod
    def update_user_password(user, password=None):
        """
        Set user password and save to database. Password will hashed
        @param user: User model
        @param password: 
        @return: 
        """
        if password is None:
            password = user.login_name
        user.password = UserLogic.hash_password(password)
        user.save()

    @staticmethod
    def is_password_match(password, hashed_password):
        """
        
        @param password: 
        @param hashed_password: 
        @return: 
        """
        return bcrypt.checkpw(password.encode('utf8'), hashed_password.encode('utf8'))

    @staticmethod
    def login(login_name, password=None):
        """
        Login with name and password. Return UserLogic if succeeded, None if failed
        @param login_name: 
        @param password: 
        @return: UserLogic
        """
        try:

            user = User.objects.get(Q(login_name=login_name))
            if password is not None and user.password is not None:
                if not bcrypt.checkpw(password.encode('utf8'), user.password.encode('utf8')):
                    user = None
            #
            #
            #
        except User.DoesNotExist:
            user = None

        return user

    @staticmethod
    def get_roles_dict():
        roles = Master.objects.filter(mastertype=MasterType.Roles.code)
        roles_dict = {}
        for role in roles:
            role_dict = dict()
            role_dict[role.master_id] = role.name
            roles_dict.update(role_dict)
        return roles_dict

    @staticmethod
    def get_genders_dict():
        genders = Master.objects.filter(mastertype=MasterType.Gender.code)
        genders_dict = {}
        for gender in genders:
            gender_dict = dict()
            gender_dict[gender.master_id] = gender.name
            genders_dict.update(gender_dict)
        return genders_dict

    @staticmethod
    def get_teachers_dict():

        teachers = User.objects.filter(roles=UserRoles.Teacher.code)
        if len(teachers) == 0:
            return {}
        teachers_dict = {}

        for teacher in teachers:
            teacher_dict = dict()
            teacher_dict[teacher.id] = teacher.user_name
            teachers_dict.update(teacher_dict)
        return teachers_dict

    @staticmethod
    def get_current_user_lesson(user_id):

        users_current_lesson = BaseUserPart.objects.filter(user_id=user_id).values('part_id__name', 'part_id')\
            .order_by('-part_id__lesson', '-part_id__order')
        if len(users_current_lesson) == 0:
            return ''
        latest_user_lesson = users_current_lesson[0]
        return 'ID: ' + str(latest_user_lesson['part_id']) + ', Name: ' + latest_user_lesson['part_id__name']





            # @staticmethod
        # def get_meta_id(meta_name):
    #     """
    #     Get Meta Id from Authen Meta Type table
    #     @param meta_name: meta type name
    #     @return: meta type Id
    #     """
    #     try:
    #         meta_id = AuthMetaType.objects.filter(meta_type=meta_name).values_list('id', flat=True)
    #         return meta_id
    #     except ObjectDoesNotExist:
    #         return None

    # # Generate user roles
    # @staticmethod
    # def generate_roles():
    #     """
    #     Generate the all roles in User role as
    #     {"id": role['id'], "selected": False, "name": role['name']}
    #     @return:
    #     """
    #
    #     user_roles = []
    #     roles = CockpitRole.objects.values('id', 'name')
    #     for role in roles:
    #         user_roles.append({"id": role['id'], "selected": False, "name": role['name']})
    #     return user_roles
    #
    #     # Generate user departments

    # @staticmethod
    # def generate_departments():
    #     """
    #     Generate departments list in AuthMetaInfo table, where meta type is department
    #     @return: Departments list, each element as {"id": deparment['id'], "selected": False, "name": deparment['value']}
    #     """
    #     from default.models.models2 import AuthMetaInfo
    #     departments = []
    #     dept_meta_id = AuthMetaTypeDefine.Department.code
    #
    #     if dept_meta_id is not None:
    #         departments_list = AuthMetaInfo.objects.filter(meta_type=dept_meta_id).values('id', 'value')
    #         for dept in departments_list:
    #             departments.append({"id": dept['id'], "selected": False, "name": dept['value']})
    #     return departments

    # @staticmethod
    # def set_user_roles(user_id):
    #     """
    #     Get Set user roles list for user
    #     @type user_id : int
    #     @param user_id: user id
    #     @return: User roles in List Type and roles list in String Type
    #     """
    #     user_roles_str = ''
    #     user_roles = UserLogic.generate_roles()
    #     try:
    #         user_updating_role = UserRole.objects.filter(user_id=user_id).values_list('role_type', flat=True)
    #     except ObjectDoesNotExist:
    #         return
    #
    #     for i in range(0, len(user_roles)):
    #         if user_roles[i]["id"] in user_updating_role:
    #             user_roles[i]["selected"] = True
    #             user_roles_str = user_roles_str + "\n" + user_roles[i]["name"]
    #
    #     return user_roles, user_roles_str
    #
    # @staticmethod
    # def set_user_departments(user_id):
    #     """
    #     Get Set user department list for user
    #     @type user_id: int
    #     @param user_id: user id
    #     @return: User departments in List Type and departments list in String Type
    #     """
    #     departments_str = ''
    #     departments = UserLogic.generate_departments()
    #     try:
    #         dept_id = AuthMetaTypeDefine.Department.code
    #         user_departments = UserFilter.objects.filter(
    #             Q(user_id=user_id) & Q(meta_type=dept_id)).values_list(
    #             'meta', flat=True)
    #     except ObjectDoesNotExist:
    #         return
    #     for i in range(0, len(departments)):
    #         if departments[i]["id"] in user_departments:
    #             departments[i]["selected"] = True
    #             departments_str = departments_str + "\n" + departments[i]["name"]
    #
    #     return departments, departments_str
    #
    # @staticmethod
    # def update_roles_and_department(type_form, user_updated, original_roles, original_departments):
    #
    #     """
    #     Update the roles list and departments list for the user
    #     @param type_form: Form View
    #     @param user_updated: user that is updated
    #     @param original_roles: the original roles list of user, before updated
    #     @param original_departments:  the original department list of user, before updated
    #     @return: True if have changed, False if doesn't have any changed.
    #     """
    #     changed = False
    #     today = datetime.datetime.today()
    #     role_list = type_form.get_field('roles').get_multi_choices_selected_values()
    #     role_list = [int(x) for x in role_list]
    #     # Compare new role list with original role list
    #     roles_deleted = list(set(original_roles) - set(role_list))
    #     for r_id in roles_deleted:
    #         try:
    #             user_role = UserRole.objects.filter(Q(user_id=user_updated.id) & Q(role_type=r_id))
    #             for u in user_role:
    #                 u.delete()
    #                 changed = True
    #
    #         except ObjectDoesNotExist:
    #             from .loglogic import LogOperation, LogModule, LogType, LogResult
    #             LogOperation.log(LogModule.User, LogType.Update, LogResult.Fail, user_updated.id,
    #                              "roles update: ObjectDoesNotExist")
    #
    #     roles_added = list(set(role_list) - set(original_roles))
    #     for r_id in roles_added:
    #         cockpit_role = CockpitRole.objects.get(id=r_id)
    #         user_role = UserRole(user_id=user_updated.id, role_type=cockpit_role,
    #                              updated_datetime=today, created_datetime=today)
    #         user_role.save()
    #         changed = True
    #
    #     departments_list = type_form.get_field('departments').get_multi_choices_selected_values()
    #     departments_list = [int(x) for x in departments_list]
    #     # Compare new department list with original department list
    #     departments_deleted = list(set(original_departments) - set(departments_list))
    #     for deptId in departments_deleted:
    #         try:
    #             user_department = UserFilter.objects.filter(Q(user_id=user_updated.id) & Q(meta=deptId))
    #             for dept in user_department:
    #                 changed = True
    #                 dept.delete()
    #
    #         except ObjectDoesNotExist:
    #             from .loglogic import LogOperation, LogModule, LogType, LogResult
    #             LogOperation.log(LogModule.User, LogType.Update, LogResult.Fail,
    #                              user_updated.id, "filters update: ObjectDoesNotExist")
    #
    #     dept_id = AuthMetaTypeDefine.Department.code
    #     departments_added = list(set(departments_list) - set(original_departments))
    #     for dpt in departments_added:
    #         meta = AuthMetaInfo.objects.get(id=dpt)
    #         meta_type = AuthMetaType.objects.get(id=dept_id)
    #         user_dept = UserFilter(user_id=user_updated.id, meta=meta, meta_type=meta_type,
    #                                updated_datetime=today, created_datetime=today)
    #         user_dept.save()
    #         changed = True
    #     return changed

    # @staticmethod
    # def delete_all_roles_and_departments(user_id):
    #     """
    #     Delete all roles and departments of user
    #     @type user_id: int
    #     @param user_id:
    #     @return:
    #     """
    #     try:
    #         user_role = UserRole.objects.filter(user_id=user_id)
    #         for u in user_role:
    #             u.delete()
    #
    #     except ObjectDoesNotExist:
    #         from .loglogic import LogOperation, LogModule, LogType, LogResult
    #         LogOperation.log(LogModule.User, LogType.Delete, LogResult.Fail,
    #                          user_id, "roles delete ObjectDoesNotExist")
    #     try:
    #         user_department = UserFilter.objects.filter(user_id=user_id)
    #         for dept in user_department:
    #             dept.delete()
    #
    #     except ObjectDoesNotExist:
    #         from .loglogic import LogOperation, LogModule, LogType, LogResult
    #         LogOperation.log(LogModule.User, LogType.Delete, LogResult.Fail,
    #                          user_id, "filters delete ObjectDoesNotExist")
    #
    # @staticmethod
    # def save_roles_and_department(type_form, user_id):
    #     """
    #     Save roles and department of user
    #     @param type_form:
    #     @type user_id: int
    #     @param user_id:
    #     @return:
    #     """
    #     today = datetime.datetime.today()
    #     role_list = type_form.get_field('roles').get_multi_choices_selected_values()
    #     for r in role_list:
    #         cockpit_role = CockpitRole.objects.get(id=r)
    #         user_role = UserRole(user_id=user_id, role_type=cockpit_role, created_datetime=today, updated_datetime=today)
    #         user_role.save()
    #     dept_id = AuthMetaTypeDefine.Department.code
    #
    #     department_list = type_form.get_field('departments').get_multi_choices_selected_values()
    #     for dpt in department_list:
    #         meta = AuthMetaInfo.objects.get(Q(id=dpt) & Q(meta_type=dept_id))
    #         meta_type = AuthMetaType.objects.get(id=dept_id)
    #         user_dept = UserFilter(user_id=user_id, meta=meta, meta_type=meta_type, created_datetime=today,
    #                                updated_datetime=today)
    #         user_dept.save()


class LoginUser:
    """
    Login user info manage.
    Check if user have right or filter.
    """
    id = 0
    name = None
    login_name = None
    roles = []
    filters = {}
    module_name = None

    login_user_session_key = 'login_user'

    def __init__(self, user=None):
        """
        @type user: User model
        @param user:
        """
        if user is not None:
            self.id = user.id
            self.name = user.user_name
            self.login_name = user.login_name
            self.roles = [user.roles]
            # self.filters = user.filters

        # self.roles.append(RoleName.Other.value)

    def __str__(self):
        """
        
        @return: 
        """
        return self.name

    def load(self, j):
        """
        
        @param j: 
        @return: 
        """
        self.__dict__ = json.loads(j)
        # Adjust user filters because json convert key to string
        adjusted = dict()
        for key, value in self.filters.items():
            adjusted[int(key)] = value
        self.filters = adjusted

    def save(self):
        """
        
        @return: 
        """
        return json.dumps(self.__dict__)

    def is_menu_available(self, screen_name):
        """
        Check if menu of screen should be shown or not
        @param screen_name: Screen name
        @return:
        """
        if screen_name in config_menus_roles:
            menu_roles = config_menus_roles[screen_name]
            # Other
            if menu_roles[0] == RoleName.Other:
                return True
            for role in self.roles:
                role_name = RoleName(role)
                if role_name in menu_roles:
                    return True
        else:
            return False

    def is_view_right(self):
        """
        
        @return: 
        """
        return self.is_right(self.module_name, UserRightType.View)

    def is_update_right(self):
        """
        
        @return: 
        """
        return self.is_right(self.module_name, UserRightType.Update)

    def is_add_right(self):
        """
        
        @return: 
        """
        return self.is_right(self.module_name, UserRightType.Insert)

    def is_delete_right(self):
        """
        
        @return: 
        """
        return self.is_right(self.module_name, UserRightType.Delete)

    def is_right(self, module_name, right):
        """
        Check if user have the right on module.
        @type module_name: ModuleName
        @param module_name:
        @type right: UserRightType
        @param right:
        @return:
        """
        # Have right in no module
        if module_name is None:
            return True
        if isinstance(module_name, int):
            module_name = ModuleName(module_name)

        if module_name in config_roles:
            # return True
            module_roles = config_roles[module_name]
            for role in self.roles:
                role_name = RoleName(role)
                if role_name in module_roles:
                    if module_roles[role_name]['right'] & right.value:
                        return True
            return False
        else:
            return True

    def get_filters(self, module_name):
        """
        Data filter rule as bellow
        This data will be show
            1.Data have no auth meta
            2.Data have auth meta match with user auth meta.
            "Match with user auth meta" mean user auth meta list is NONE or auth meta in user auth meta list.
        @type module_name: ModuleName
        @param module_name:
        If data must be filtered, return dictionary of filter info.
        Example filter_type1 = [filter_value1, filter_value2], filter_type2 = [filter_value1, filter_value2]
        @return: Dictionary. None: Don't need filter; Dictionary with empty list value: return no data
        """
        all_filter_name = config_all_filter[:]

        if module_name in config_roles:
            module_roles = config_roles[module_name]
            for role in self.roles:
                role_name = RoleName(role)
                if role_name in module_roles:
                    if module_roles[role_name]['filter'] is None:
                        del all_filter_name[:]
                    else:
                        for filter_name in all_filter_name:
                            if filter_name not in module_roles[role_name]['filter']:
                                all_filter_name.remove(filter_name)

            if len(all_filter_name) == 0:
                return None
            else:
                ret = {}
                for filter_name in all_filter_name:
                    if filter_name in self.filters:
                        ret[filter_name] = self.filters[filter_name]
                    else:
                        ret[filter_name] = []
                return ret
        else:
            return None

    def get_filtered_query_string(self, module_name, auth_meta_type_id, none_if_no_filter=True):
        """
        @type module_name: ModuleName
        @param module_name:
        @type auth_meta_type_id: int
        @param auth_meta_type_id:
        @param none_if_no_filter
        @rtype: str
        @return: string like 1,2,3,3 that used in query condition
        """
        from default.logic.metalogic import AuthMetaLogic
        filters = self.get_filters(module_name)
        if filters is None and none_if_no_filter:
            return None

        data = AuthMetaLogic.get_current_meta_list(auth_meta_type_id)
        data = LoginUser.filter_meta_info_list(data, filters, auth_meta_type_id)
        data = data.values_list('id', flat=True)
        return ",".join(map(str, data))

    def get_filtered_meta_ids(self, module_name, auth_meta_type_id):
        """
        @type module_name: ModuleName
        @param module_name:
        @type auth_meta_type_id: int
        @param auth_meta_type_id:
        @rtype: list
        @return: list of id
        """
        from default.logic.metalogic import AuthMetaLogic
        filters = self.get_filters(module_name)
        data = AuthMetaLogic.get_current_meta_list(auth_meta_type_id)
        data = LoginUser.filter_meta_info_list(data, filters, auth_meta_type_id)
        data = data.values_list('id', flat=True)
        return data

    def get_filtered_meta_list(self, module_name, auth_meta_type_id):
        """
        @type module_name: ModuleName
        @param module_name:
        @type auth_meta_type_id: int
        @param auth_meta_type_id:
        @rtype: list
        @return: list of object
        """
        from default.logic.metalogic import AuthMetaLogic
        filters = self.get_filters(module_name)
        data = AuthMetaLogic.get_current_meta_list(auth_meta_type_id)
        data = LoginUser.filter_meta_info_list(data, filters, auth_meta_type_id)
        return data


    # @staticmethod
    # def get_filtered_base_data_ids(filters, base_data_name):
    #     """
    #
    #     @param filters:
    #     @param base_data_name:
    #     @return: None: do not need to filter. Empty list: must return no data. List: filter with this list
    #     """
    #     if filters is None or not filters:
    #         return None
    #
    #     ret = None
    #
    #     # Trick: if base data is user, we see in user_filter. As the future, we need to use base_data_auth_meta_rel for
    #     # user_filter
    #     if base_data_name == AuthBaseDataName.User.value:
    #         for filter_code, filter_values in filters.items():
    #             if not filter_values:
    #                 return []
    #             if ret is None:
    #                 ret = UserFilter.objects
    #             ret = ret.filter(meta_type_id=filter_code, meta_id__in=filter_values)
    #         if ret is not None:
    #             ret = ret.values_list('user_id', flat=True)
    #     else:
    #         for filter_code, filter_values in filters.items():
    #             if not filter_values:
    #                 return []
    #             if ret is None:
    #                 ret = BaseDataAuthMetaRel.objects
    #             ret = ret.filter(base_data_name=base_data_name,
    #                              meta_type_id=filter_code, meta_id__in=filter_values)
    #         if ret is not None:
    #             ret = ret.values_list('base_data_id', flat=True)
    #     return ret

    @staticmethod
    def filter_meta_info_list(meta_info_list, filters, auth_meta_type):
        """
        @type meta_info_list: QuerySet
        @param meta_info_list:
        @type filters: dict
        @param filters: Get from LoginUser@get_filters
        @type auth_meta_type: int
        @param auth_meta_type: Auth Meta Type code
        @return:
        """
        if not meta_info_list:
            return meta_info_list

        if filters is None or not filters:
            return meta_info_list

        if auth_meta_type not in filters:
            return meta_info_list

        filter_ids = filters[auth_meta_type]

        meta_info_list = meta_info_list.filter(id__in=filter_ids)

        return meta_info_list

    def save_to_session(self, request):
        """
        
        @param request: 
        @return: 
        """
        request.session[LoginUser.login_user_session_key] = self.save()

    @staticmethod
    def do_logout(request):
        """
        
        @param request: 
        @return: 
        """
        try:
            del request.session[LoginUser.login_user_session_key]
        except KeyError:
            pass

    @staticmethod
    def do_login(request, user, password, remember_me=False):
        """
        User user and password to login. If user and password are right, save login info to session
        @param request:
        @param user:
        @param password:
        @param remember_me:
        @return: LoginUser
        """
        user = UserLogic.login(user)

        if user is not None:
            login_user = LoginUser(user)
            login_user.save_to_session(request)
            if remember_me:
                # remember for 30 day
                request.session['remember_me'] = True
                request.session.set_expiry(30 * 24 * 3600)
            else:
                request.session['remember_me'] = False
                request.session.set_expiry(0)
            return True
        else:
            return False

    @staticmethod
    def reload(request, view_func):
        """
        Load info from database
        @param request:
        @param view_func:
        @return: LoginUser
        """
        login_user = LoginUser.get_login_user(request)

        user = UserLogic.login(login_user.login_name)

        login_user = LoginUser(user)

        # Which module
        func_name = view_func.__name__
        if func_name in config_view_module_mapping:
            login_user.module_name = config_view_module_mapping[func_name]
        else:
            login_user.module_name = None

        login_user.save_to_session(request)
        if "remember_me" in request.session and request.session['remember_me']:
            request.session.set_expiry(30 * 24 * 3600)
        else:
            request.session.set_expiry(0)

        return login_user

    @staticmethod
    def get_login_user(request=None):
        """
        
        @param request: 
        @return: 
        """
        if request is None:
            request = GlobalRequest.get_request()
        if request is not None:
            j = request.session.get(LoginUser.login_user_session_key)
            if j is not None:
                login_user = LoginUser()
                login_user.load(j)
                return login_user
            return None
