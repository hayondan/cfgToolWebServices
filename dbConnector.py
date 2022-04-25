import pymysql

# Establishing a connection to DB
from flask import json

conn = pymysql.connect(host='remotemysql.com', port=3306, user='zMGXeJWAc0', passwd='sYCbS2p8OV', db='zMGXeJWAc0')

# Getting a cursor from Database
cursor = conn.cursor()


# Getting all data from table

def getVersion(version):
    with conn.cursor() as cursor:
        versions = ['A32', 'A3210', 'A3220', 'A32Old', 'A3210Old', 'A3220Old']
        SQLversionNumber = "SELECT * FROM zMGXeJWAc0." + version + ";"
        print(SQLversionNumber)
        cursor.execute(SQLversionNumber)
        versionInfo = cursor.fetchall()
        versionJson = versionInfo[0]
        buildJson = versionInfo[1]
        appJson = versionInfo[2]
        if version in versions:
            vernum = versionJson[0]
            builnum = buildJson[1]
            appnum = appJson[2]
            if vernum or builnum or appnum is not None:
                print(vernum, builnum, appnum)
                # print("version "+version+"=" + vernum + " build= " + builnum + "appbuild= " + appnum)
                print("test_db | getVersion | version = ", vernum,  "build = ", builnum, "appBuild = ", appnum)
                return {'version': vernum, 'build': builnum, 'appBuild': appnum}
            else:
                print(vernum, builnum, appnum)
                print("None")
                return None



def getVersionNu(version):
    sql = "SELECT version FROM zMGXeJWAc0." + version + ";"
    with conn.cursor() as cursor:
        print(sql)
        cursor.execute(sql)
        versionNum = cursor.fetchall()
        # print("\ntest_db | getVersionNu | info= ", versionNum)
        return versionNum


def getBuildNu(version):
    sql = "SELECT build FROM zMGXeJWAc0." + version + ";"
    with conn.cursor() as cursor:
        print(sql)
        cursor.execute(sql)
        buildNum = cursor.fetchall()
        # print("\ntest_db | getBuildNu | build_number= ", buildNum)
        return buildNum


def insertVersion(version, verNum):
    conn.autocommit(True)
    with conn.cursor() as cursor:
        values = verNum
        SQLtoDB = "INSERT into zMGXeJWAc0." + version
        SQLtoinsert = " (version) VALUES"+"("+str(values)+")"
        query = SQLtoDB + SQLtoinsert
        print(query)
        cursor.execute(query)
        return verNum


def updateVersion(version, verNum):
    conn.autocommit(True)
    with conn.cursor() as cursor:
        SQLtoDB = "UPDATE zMGXeJWAc0." + version
        SQLtoPUT = " SET version=" + verNum
        query = SQLtoDB + SQLtoPUT
        print(query)
        cursor.execute(query)
        return verNum


def createRoute(version, verNum):
    versions = ['A32', 'A3210', 'A3220', 'A32Old', 'A3210Old', 'A3220Old']
    if version in versions:
        route = 'http://127.0.0.1:5000/data/version/'+ version + '/' + verNum
        return route


def insertBuild(version, buildNum):
    conn.autocommit(True)
    with conn.cursor() as cursor:
        values = buildNum
        SQLtoDB = "INSERT into zMGXeJWAc0." + version
        SQLtoinsert = " (build) VALUES"+"("+str(values)+")"
        query = SQLtoDB + SQLtoinsert
        print(query)
        cursor.execute(query)
        return buildNum


def updateBuild(version, buildNum):
    conn.autocommit(True)
    with conn.cursor() as cursor:
        SQLtoDB = "UPDATE zMGXeJWAc0." + version
        SQLtoPUT = " SET build=" + buildNum
        query = SQLtoDB + SQLtoPUT
        print(query)
        cursor.execute(query)
        return buildNum


def insertappBuild(version, appBuildNum):
    conn.autocommit(True)
    with conn.cursor() as cursor:
        values = appBuildNum
        SQLtoDB = "INSERT into zMGXeJWAc0." + version
        SQLtoinsert = " (appBuild) VALUES"+"("+str(values)+")"
        query = SQLtoDB + SQLtoinsert
        print(query)
        cursor.execute(query)
        return appBuildNum


def updateappBuild(version, appBuildNum):
    conn.autocommit(True)
    with conn.cursor() as cursor:
        SQLtoDB = "UPDATE zMGXeJWAc0." + version
        SQLtoPUT = " SET appBuild=" + appBuildNum
        query = SQLtoDB + SQLtoPUT
        print(query)
        cursor.execute(query)
        return appBuildNum



def deleteAllFromColumn(version):
    conn.autocommit(True)
    with conn.cursor() as cursor:
        sql = "DELETE FROM zMGXeJWAc0." + version
        print(sql)
        cursor.execute(sql)
        return version