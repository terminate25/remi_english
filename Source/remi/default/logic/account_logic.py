# -*- coding: utf-8 -*-

from default.config.config_common import *


class AccountLogic:

    @staticmethod
    def get_account_type(account_type_id):
        """
        Get account type name by account type id
        @type account_type_id: int
        @param account_type_id: 
        @return: 
        """
        account_type_str = ""
        account_types = [account_type.value for account_type in AccountType]
        for account_type in account_types:
            if account_type[0] == account_type_id:
                account_type_str = account_type[1]
        return account_type_str

    @staticmethod
    def get_default_account_types():
        """
        Get Account type list 
        @rtype: list of AccountType value
        @return: 
        """
        account_types = [account_type.value for account_type in AccountType]
        return account_types

    @staticmethod
    def get_account_class(account_class_id):
        """
        Get account class name using account class id 
        @param account_class_id: 
        @rtype: str
        @return: 
        """
        account_class_str = ""
        account_classes = [cl.value for cl in AccountClass]
        for cl in account_classes:
            if cl[0] == account_class_id:
                account_class_str = cl[1]
        return account_class_str

    @staticmethod
    def get_checkbox_boolean(check_box_value):
        """
        Parser check box value 
        @param check_box_value:
        @rtype: bool
        @return: 
        """
        return check_box_value == 1

    @staticmethod
    def get_checkbox_int(check_box_value):
        """
        
        @param check_box_value: 
        @rtype: int
        @return: 
        """
        if check_box_value is None:
            return 0
        return int(check_box_value)

