# # -*- coding: utf-8 -*-
# from __future__ import unicode_literals
# from django.db import transaction
# from django.db.models import Q
# from django.db.utils import IntegrityError
# from default.models.mo import *
# import datetime
# from middleware.router import DatabaseRouter
#
#
# class MetaException(Exception):
#     """
#     raise exception
#     """
#
#
# class MetaLogic:
#     """
#     Define function:
#         merge_meta_info(): transaction processing while hit merge button
#     """
#
#     @staticmethod
#     @transaction.atomic(using=DatabaseRouter.data_database)
#     def merge_meta_info(meta_type_id, meta_info_source, meta_info_destination):
#         """
#         @type meta_type_id: int
#         @type meta_info_source: list
#         @type meta_info_destination: int
#         @return: raise exception and rollback if error
#         """
#
#         if meta_type_id < 0:
#             raise MetaException('')
#         if not meta_info_source:
#             raise MetaException('')
#         if meta_info_destination < 0:
#             raise MetaException('')
#
#         try:
#             # update meta_id in base_data_meta_rel
#             BaseDataMetaRel.objects \
#                 .filter(Q(meta_type_id=meta_type_id) &
#                         Q(meta_id__in=meta_info_source)) \
#                 .update(meta_id=meta_info_destination)
#             # delete meta_info has id in meta_info_source
#             MetaInfo.objects.filter(id__in=meta_info_source).delete()
#         except IntegrityError as e:
#             raise MetaException(e)
#
#     @staticmethod
#     def get_current_meta_list(meta_type_id, current_date=None):
#         """
#         Get meta info list after filter valid period (有効期限)
#         @param meta_type_id:
#         @param current_date:
#         @return:
#         """
#         if current_date is None:
#             current_date = datetime.datetime.now().date()
#
#         return MetaInfo.objects.filter(Q(meta_type_id=meta_type_id) &
#                                            (Q(valid_start_date__lte=current_date)
#                                             | Q(valid_start_date__isnull=True)) &
#                                            (Q(valid_end_date__gte=current_date)
#                                             | Q(valid_end_date__isnull=True)))
#
#
# class AuthMetaLogic:
#     """
#     Define function:
#         merge_auth_meta_info(): transaction processing while hit merge button
#     """
#
#     @staticmethod
#     @transaction.atomic(using=DatabaseRouter.data_database)
#     def merge_auth_meta_info(auth_meta_type_id, auth_meta_info_source, auth_meta_info_destination):
#         """
#         @type auth_meta_type_id: int
#         @type auth_meta_info_source: list
#         @type auth_meta_info_destination: int
#         @return: raise exception and rollback if error
#         """
#
#         if auth_meta_type_id < 0:
#             raise MetaException('')
#         if not auth_meta_info_source:
#             raise MetaException('')
#         if auth_meta_info_destination < 0:
#             raise MetaException('')
#
#         try:
#             # update meta_id in base_data_meta_rel
#             BaseDataAuthMetaRel.objects \
#                 .filter(Q(meta_type_id=auth_meta_type_id) &
#                         Q(meta_id__in=auth_meta_info_source)) \
#                 .update(meta_id=auth_meta_info_destination)
#             # update meta_id in user_filter
#             UserFilter.objects \
#                 .filter(Q(meta_type_id=auth_meta_type_id) &
#                         Q(meta_id__in=auth_meta_info_source)) \
#                 .update(meta_id=auth_meta_info_destination)
#             # delete auth_meta_info has id in meta_info_source
#             AuthMetaInfo.objects.filter(id__in=auth_meta_info_source).delete()
#         except IntegrityError as e:
#             raise MetaException(e)
#
#     @staticmethod
#     def get_current_meta_list(meta_type_id, current_date=None):
#         """
#         Get meta info list after filter valid period (有効期限)
#         @param meta_type_id:
#         @param current_date:
#         @return:
#         """
#         if current_date is None:
#             current_date = datetime.datetime.now().date()
#
#         return AuthMetaInfo.objects.filter(Q(meta_type_id=meta_type_id) &
#                                            (Q(valid_start_date__lte=current_date)
#                                             | Q(valid_start_date__isnull=True)) &
#                                            (Q(valid_end_date__gte=current_date)
#                                             | Q(valid_end_date__isnull=True)))
#
#     @staticmethod
#     def get_meta_list(meta_type_id):
#         """
#         Get meta info list no filter valid period (有効期限)
#         @param meta_type_id:
#         @return:
#         """
#         return AuthMetaInfo.objects.filter(Q(meta_type_id=meta_type_id))
#
