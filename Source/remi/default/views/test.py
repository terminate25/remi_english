
import requests
import datetime
import sys

username = "trantuananh93@gmail.com"
password = "12345678"


def login():
    url = "http://www.cophieu68.vn/account/login.php"
    params = {
                'username': username,
                'tpassword': password,
                'ajax': 1,
                'login': 1
                }
    r = requests.post(url, data=params)
    if r.text.strip() != '1':
        return None
    import re
    m = re.search('PHPSESSID=(\w+)', r.cookies.__str__())
    return {"PHPSESSID": m.group(1)}


def get_stock_by_date(date, cookies):
    url = "http://www.cophieu68.vn/export/dailyexcel.php?date={0}".format(date)
    import os
    import datetime
    response = requests.get(url, cookies=cookies)
    file_name = '{0}-{1}.csv'.format(date, datetime.datetime.today().__str__())
    save_file(file_name, response)


def get_stock_by_id(id, cookies):
    url = "http://www.cophieu68.vn/export/excelfull.php?id={0}".format(id)
    import os
    import datetime
    response = requests.get(url, cookies=cookies)
    file_name = '{0}-{1}.csv'.format(id, datetime.datetime.today().__str__())
    save_file(file_name, response)


def save_file(file_name, response):
    import os
    script_path = os.path.dirname(sys.argv[0])
    file_path = os.path.join(os.path.join(script_path, file_name))
    output = open(file_path, 'wb')
    output.write(response.content)
    output.close()


def execute():
    cookies = login()
    if cookies is None:
        print("Login failed!")
        return
    date_time = input("Enter date time (dd-mm-yyyy): ")
    get_stock_by_date(date_time, cookies)
    id = input("Enter date time (example:  \"000001.SS\"): ")
    get_stock_by_id(id, cookies)


if __name__ == "__main__":
    execute()
