#!/usr/bin/env python
# coding=utf-8
import urllib.request
import urllib.parse
import http.cookiejar
import string
import re
import pymysql
import base64
import chardet
import socket
import json
import codecs
import sys
from bs4 import BeautifulSoup
import time
timeout = 30
now_xn = 2015
now_xq = 2
socket.setdefaulttimeout(timeout)

conn = pymysql.connect(host="localhost", user="root",
                       passwd="root", db="QWeixin", charset="utf8")
cursor = conn.cursor()
output = open('log.txt', 'a+')

def insertData(tablename, data):
    key = []
    val = []
    for k, v in data.items():
        key.append(k)
        val.append("'" + str(v) + "'")
    key1 = ",".join(key)
    val1 = ",".join(val)
    sql = "insert into " + tablename + "(" + key1 + ") values (" + val1 + ")"
    return sql


def updateData(tablename, data, condition):
    val = []
    for i in range(len(data)):
        val.append(data.keys()[i] + "='" + str(data.values()[i]) + "'")
    val1 = ",".join(val)
    sql = "update " + tablename + " set " + val1 + " where " + condition
    return sql


def deal_table(soup):  # return list which contain all table
    temp = []
    map = []
    soup = BeautifulSoup(soup, 'html.parser')
    for tabb in soup.find_all('tr'):
        for tdd in tabb.find_all('td'):
            temp.append(tdd.get_text())
        map.append(list(temp))
        temp.clear()
    return map


def deal_xml(str, key):
    temp = []
    data = BeautifulSoup(str, 'html.parser')
    s = data.find(key).get_text()
    return s


def opensite(url, postdata, refer=""):
    postdata = urllib.parse.urlencode(postdata).encode(encoding="gbk")
    req = urllib.request.Request(url, postdata)
    req.add_header("Referer", refer)
    try:
        req = urllib.request.urlopen(req)
        d = req.read()
        char = chardet.detect(d)
        char = char['encoding']
        d = d.decode(char, "ignore")
        return d
    except Exception as e:
        output.write(string(e))
        return "err"


class OucJw:

    def __init__(self, username, password):
        self.xn = 2015
        self.xq = 2
        self.url = "http://jwgl2.ouc.edu.cn/"
        self.username = username
        self.password = password
        self.cj = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(self.cj))
        self.opener.addheaders = [('Host', self.url), (
            'User-Agent', 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729)')]
        urllib.request.install_opener(self.opener)

    def login(self):
        s = (self.username + ";;").encode(encoding="gbk")
        encode_username = base64.b64encode(s)
        postdata = {'_p': self.password, '_u': encode_username}
        url = self.url + "cas/logon.action"
        data = opensite(url, postdata)
        data = json.loads(data)
        print(type(data))
        return data

    def get_user_info(self):
        url = self.url + "STU_BaseInfoAction.do"
        postdata = {'hidOption': 'InitData'}
        refer = self.url + "student/stu.xsxj.xjda.jbxx.html?menucode=JW13020101"
        data = opensite(url, postdata, refer)
        print(data)
        temp = {}
        temp['xm'] = deal_xml(data, 'xm')
        temp['birth'] = deal_xml(data, 'csrq')
        temp['sex'] = deal_xml(data, 'xb')
        temp['dept'] = deal_xml(data, 'zymc')
        temp['btime'] = deal_xml(data, 'rxnj')

    def get_score_data(self):
        url = self.url + "student/xscj.stuckcj_data.jsp"
        refer = self.url + "student/xscj.stuckcj.jsp?menucode=JW130705"
        postdata = {'xn': now_xn, 'xq': now_xq, 'ysyx': 'yscj', 'sjxz': 'sjxz1',
                    'userCode': self.username, 'ysyxS': 'on', 'sjxzS': 'on'}
        data = opensite(url, postdata, refer)
        data = deal_table(data)
        dataset = {}
        for x in data:
            if(len(x) < 2 or len(x) == 2):
                temp = re.findall(r'\d+', x[0])
                if(len(temp)):
                    temp_xn = temp[0]
                else:
                    break
                temp = {'秋': 1, '春': 2, '夏': 0}
                for k, v in temp.items():
                    if(k in x[0]):
                        temp_xq = v
                        break
                if temp_xq == 2:
                    temp_xn = int(temp_xn) - 1
                continue
            if x[0] == "序号":
                continue
            temp = {}
            temp['username'] = self.username
            temp['xn'] = temp_xn
            temp['xq'] = temp_xq
            temp['course_name'] = x[1]
            temp['credit'] = float(x[2])
            temp['jd'] = self.cal_gpa(x[6])
            temp['score1'] = x[6]
            dataset[x[1]]  = temp;
        return dataset 

    def cal_gpa(self, str):
        try:
            s = float(str)
            if s <= 100 and s >= 90:
                result = 4.0
            elif s < 90 and s >= 85:
                result = 3.7
            elif s < 85 and s >= 81:
                result = 3.3
            elif s < 81 and s >= 78:
                result = 3.0
            elif s < 78 and s >= 75:
                result = 2.7
            elif s < 75 and s >= 71:
                result = 2.3
            elif s < 71 and s >= 68:
                result = 2.0
            elif s < 68 and s >= 64:
                result = 1.7
            elif s < 64 and s >= 60:
                result = 1.0
            else:
                result = 0.0
        except:
            if(str == "优秀"):
                result = 3.9
            elif(str == "良好"):
                result = 3.3
            elif(str == "中等"):
                result = 2.3
            elif(str == "合格"):
                result = 1.0
            else:
                result = 0.0
        return result

    def getCurrentCourseData(self):
        url = self.url + "wsxk/xkjg.ckdgxsxdkchj_data.jsp"
        refer = self.url + "student/xkjg.wdkb.jsp?menucode=JW130416"
        param = ("xn={}&xq={}&xh="+self.username).format(self.xn,self.xq).encode(encoding = 'gbk')
        param = base64.b64encode(param)
        postdata = {'params': param}
        data = opensite(url, postdata, refer)
        data = deal_table(data)
        dataset = {}
        if(len(data) > 0):
            del(data[0])
        for x in data:
            temp = {}
            temp['Id'] = x[0]
            temp['xn'] = self.xn
            temp['xq'] = self.xq
            temp['course_name'] = x[1]
            temp['xkb'] = x[8]
            temp['xf'] = x[3]
            temp['cx'] = x[4]
            temp['kch'] = x[13]
            temp['username'] = self.username
            dataset[x[0]] = temp;
        return dataset

if __name__ == '__main__':
    username = sys.argv[1]
    password = sys.argv[2]
    method = sys.argv[3]
    if method == '1':
        oucjw = OucJw(username, password)
        data = oucjw.login()
        print(json.dumps(data))
        oucjw.get_user_info()
    elif method == '2':
        oucjw = OucJw(username, password)
        oucjw.login()