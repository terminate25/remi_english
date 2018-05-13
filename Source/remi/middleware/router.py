from django.db import connections


class DatabaseRouter(object):
    """
    Django features. Determine which database to use.
    User table are in default database. Others in db_data database
    """
    user_database = 'default'
    data_database = 'default'

    # default_database_tables = ['user']
    default_database_tables = []
    """
    A router to control all database operations on models in the
    auth application.
    """
    def db_for_read(self, model, **hints):
        """

        @param model:
        @param hints:
        @return:
        """
        if model._meta.db_table not in self.default_database_tables:
            return self.data_database
        return None

    def db_for_write(self, model, **hints):
        """

        @param model:
        @param hints:
        @return:
        """
        if model._meta.db_table not in self.default_database_tables:
            return self.data_database
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """

        @param obj1:
        @param obj2:
        @param hints:
        @return:
        """
        if obj1._meta.db_table in self.default_database_tables and \
           obj2._meta.db_table not in self.default_database_tables:
            return False

        if obj1._meta.db_table not in self.default_database_tables and \
            obj2._meta.db_table in self.default_database_tables:
            return False

        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """

        @param db:
        @param app_label:
        @param model_name:
        @param hints:
        @return:
        """
        return self.data_database

    @staticmethod
    def add_database(host, name, user, password, port=3306, engine='django.db.backends.mysql'):
        if name in connections:
            return

        new_database = dict()
        new_database['ENGINE'] = engine
        new_database['NAME'] = name
        new_database['USER'] = user
        new_database['PASSWORD'] = password
        new_database['HOST'] = host
        new_database['PORT'] = port
        connections.databases[name] = new_database

    @staticmethod
    def delete_database(name):
        if name in connections:
            connections[name].close()
            del connections[name]

    @staticmethod
    def set_data_database(name):
        DatabaseRouter.data_database = name
