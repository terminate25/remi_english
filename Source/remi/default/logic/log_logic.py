# -*- coding: utf-8 -*-

from default.config.config_log import LogModule, LogType, LogResult
# from default.models.models2 import OperationLog
from default.logic.user_logic import LoginUser


class LogOperation:
    @staticmethod
    def log(log_module, log_type, log_result, operation_object=None, error_message=None):
        """
        LogOperation.log( LogModule.User, LogType.Insert, LogResult.Success, user_id)
        LogOperation.log( LogModule.User, LogType.Delete, LogResult.Fail, user_id, "Fail to delete")
        @type log_module: LogModule
        @param log_module:
        @type log_type: LogType
        @param log_type:
        @type log_result: LogResult
        @param log_result:
        @param operation_object:
        @param error_message:
        @return:
        """
        user = LoginUser.get_login_user()
        if user is None:
            return
        #
        # log_object = OperationLog()
        # log_object.user_id = user.id
        # log_object.data_name = log_module.value
        # log_object.log_result = log_result.value
        # log_object.log_type = log_type.value
        # if operation_object is not None:
        #     log_object.log_object = str(operation_object)
        # if error_message is not None:
        #     log_object.error_message = error_message
        #
        # log_object.save()
