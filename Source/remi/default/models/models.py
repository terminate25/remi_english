# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Account(models.Model):
    type = models.IntegerField(blank=True, null=True)
    title = models.TextField()
    account_class = models.IntegerField()
    tax_class = models.IntegerField()
    is_cash = models.IntegerField(blank=True, null=True)
    settlement_date_type = models.IntegerField(blank=True, null=True)
    created_datetime = models.DateTimeField(blank=True, null=True)
    updated_datetime = models.DateTimeField(blank=True, null=True)
    deleted_flag = models.IntegerField()
    account_code = models.IntegerField()
    account_name = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'account'


class Answer(models.Model):
    question_id = models.IntegerField()
    answer = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'answer'


class ApiRestriction(models.Model):
    url = models.CharField(max_length=1024)
    need_owner_flag = models.IntegerField()
    created_datetime = models.DateTimeField()
    updated_datetime = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'api_restriction'


class AsyncTransaction(models.Model):
    transaction_id = models.BigAutoField(primary_key=True)
    client_order = models.BigIntegerField(blank=True, null=True)
    prev_client_order = models.BigIntegerField(blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    accepted_datetime = models.DateTimeField(blank=True, null=True)
    started_datetime = models.DateTimeField(blank=True, null=True)
    finished_datetime = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField()
    reason = models.TextField(blank=True, null=True)
    method = models.TextField(blank=True, null=True)
    resource_name = models.TextField(blank=True, null=True)
    params = models.TextField(blank=True, null=True)
    request_data = models.TextField(blank=True, null=True)
    result = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'async_transaction'


class BaseUserCourse(models.Model):
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    course = models.ForeignKey('Course', models.DO_NOTHING)
    is_done = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'base_user_course'


class BaseUserLesson(models.Model):
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    lesson = models.ForeignKey('Lesson', models.DO_NOTHING, blank=True, null=True)
    is_done = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'base_user_lesson'


class BaseUserLevel(models.Model):
    level = models.ForeignKey('Level', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    is_done = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'base_user_level'


class BaseUserPart(models.Model):
    user = models.ForeignKey('User', models.DO_NOTHING)
    part = models.ForeignKey('Part', models.DO_NOTHING)
    is_done = models.IntegerField()
    created_datetime = models.DateTimeField(blank=True, null=True)
    updated_datetime = models.DateTimeField(blank=True, null=True)
    video = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'base_user_part'


class BaseUserStep(models.Model):
    test_id = models.IntegerField(blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    part_id = models.IntegerField(blank=True, null=True)
    right_percent = models.IntegerField(blank=True, null=True)
    right_number_question = models.IntegerField(blank=True, null=True)
    implement_date = models.DateTimeField(blank=True, null=True)
    is_done = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'base_user_step'


class Course(models.Model):
    name = models.TextField(blank=True, null=True)
    created_datetime = models.DateTimeField(blank=True, null=True)
    updated_datetime = models.DateTimeField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'course'


class DefaultUser(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'default_user'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class Lesson(models.Model):
    level = models.ForeignKey('Level', models.DO_NOTHING, blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    created_datetime = models.DateTimeField(blank=True, null=True)
    updated_datetime = models.DateTimeField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'lesson'


class Level(models.Model):
    course = models.ForeignKey(Course, models.DO_NOTHING)
    name = models.TextField(blank=True, null=True)
    created_datetime = models.DateTimeField(blank=True, null=True)
    updated_datetime = models.DateTimeField(blank=True, null=True)
    order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'level'


class Master(models.Model):
    master_id = models.IntegerField()
    mastertype = models.IntegerField()
    name = models.CharField(max_length=400)
    created_datetime = models.DateTimeField(blank=True, null=True)
    updated_datetime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'master'


class Part(models.Model):
    lesson = models.ForeignKey(Lesson, models.DO_NOTHING)
    name = models.TextField(blank=True, null=True)
    created_datetime = models.DateTimeField(blank=True, null=True)
    updated_datetime = models.DateTimeField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    order = models.IntegerField(blank=True, null=True)
    video = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'part'


class Question(models.Model):
    part_id = models.IntegerField()
    name = models.TextField(blank=True, null=True)
    question = models.TextField(blank=True, null=True)
    answer = models.TextField(blank=True, null=True)
    created_datetime = models.DateTimeField(blank=True, null=True)
    updated_datetime = models.DateTimeField(blank=True, null=True)
    test = models.ForeignKey('Test', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'question'


class Test(models.Model):
    part = models.ForeignKey(Part, models.DO_NOTHING, blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)
    question_number_goal = models.IntegerField(blank=True, null=True)
    question_percent_goal = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'test'


class User(models.Model):
    login_name = models.CharField(unique=True, max_length=64)
    password = models.TextField(blank=True, null=True)
    user_name = models.CharField(max_length=64, blank=True, null=True)
    address = models.CharField(max_length=64, blank=True, null=True)
    phone = models.CharField(max_length=64, blank=True, null=True)
    email = models.CharField(max_length=64, blank=True, null=True)
    gender = models.IntegerField()
    created_datetime = models.DateTimeField(blank=True, null=True)
    updated_datetime = models.DateTimeField(blank=True, null=True)
    roles = models.IntegerField(blank=True, null=True)
    teacher_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'
