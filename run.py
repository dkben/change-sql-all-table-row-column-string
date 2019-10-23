#!/usr/bin/python
import subprocess
import sys
import pymysql.cursors
import yaml

with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

host = cfg['mysql']['host']
user = cfg['mysql']['user']
password = cfg['mysql']['password']
dbName = cfg['mysql']['db']
oldString = cfg['setup']['old_string']
newString = cfg['setup']['new_string']
tableList = cfg['setup']['table_list']
excludeTableList = cfg['setup']['exclude_table_list']
git_remote = 'git@github.com:dkben/change-sql-all-table-row-column-string.git'


# Connect to the database
connection = pymysql.connect(host=host,
                             user=user,
                             password=password,
                             db=dbName,
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)


def get_tables():
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    for table in tables:
        tableList.append(table["Tables_in_" + dbName])


def get_columns(table_name):
    cursor.execute("SHOW columns FROM " + table_name)
    columns = cursor.fetchall()
    column_list = []
    for column in columns:
        if "varchar" in column["Type"] or "text" in column["Type"]:
            column_list.append(column["Field"])
    return column_list


def update(table_name, column_list):
    for column in column_list:
        sql = "UPDATE " + table_name + " SET " + column + " = REPLACE(" + column + ", %s, %s)"
        cursor.execute(sql, (oldString, newString))
    connection.commit()


def main():
    print("============================================================")
    check_update()

    if len(tableList) == 0:
        get_tables()
    print("all tables :", tableList)

    for excludeTable in excludeTableList:
        if excludeTable in tableList:
            tableList.remove(excludeTable)

    if len(tableList) > 0:
        for table_name in tableList:
            column_list = get_columns(table_name)
            if len(column_list) > 0:
                print(table_name, ":", column_list)
                update(table_name, column_list)


def check_update():
    check = str(input('是否檢查更新？y 檢查更新 / n 繼續...[y/n]:'))
    if check == 'y':
        print('檢查更新中...')
        local_hash = subprocess.check_output('git log --pretty="%h" -n1 HEAD'.split()).decode()[1:8]
        remote_hash = subprocess.check_output(
            ('git ls-remote %s HEAD' % git_remote).split()).decode()[0:7]
        print(local_hash, remote_hash)
        if local_hash != remote_hash:
            skip = str(input('有新版程式，請 git pull 更新...，按 y 繼續 / n 離開程式...[y/n]:'))
            if skip == 'n':
                sys.exit()
        else:
            input('已經是最新版...按任意鍵繼續...')


if __name__ == '__main__':
    try:
        with connection.cursor() as cursor:
            main()
    finally:
        connection.close()

