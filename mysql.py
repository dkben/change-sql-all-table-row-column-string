#!/usr/bin/python

import sys
import pymysql.cursors
import yaml

with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

host = cfg['mysql']['host']
user = cfg['mysql']['user']
password = cfg['mysql']['password']
dbName = cfg['mysql']['db']
oldString = "old string"  # 舊字串
newString = "new string"  # 新字串
tableList = []  # 空陣列代表全部，如果有輸入個別資料表，則處理個別資料表
excludeTableList = ["table_1", "table_2"]  # 要排除的資料表

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


if __name__ == '__main__':
    try:
        with connection.cursor() as cursor:
            main()
    finally:
        connection.close()

