from Jw import *
import pymysql
from email.header import Header
from email.mime.text import MIMEText
import smtplib
output = open('oucjw.txt', 'a+')
conn = pymysql.connect(host="localhost", user="root",
                       passwd="root", db="QWeixin", charset="utf8")
cursor = conn.cursor()
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

def getData(table, keys, conditions, isdistinct=0):
    '''
        生成select的sql语句
    @table，查询记录的表名
    @key，需要查询的字段
    @conditions,插入的数据，字典
    @isdistinct,查询的数据是否不重复
    '''
    if isdistinct:
        sql = 'select distinct %s ' % ",".join(keys)
    else:
        sql = 'select  %s ' % ",".join(keys)
    sql += ' from %s ' % table
    if conditions:
        sql += ' where %s ' % dict_2_str_and(conditions)
    return sql

def dict_2_str(dictin):
    '''
    将字典变成，key='value',key='value' 的形式
    '''
    tmplist = []
    for k, v in dictin.items():
        tmp = "%s='%s'" % (str(k), safe(str(v)))
        tmplist.append(' ' + tmp + ' ')
    return ','.join(tmplist)


def dict_2_str_and(dictin):
    '''
    将字典变成，key='value' and key='value'的形式
    '''
    tmplist = []
    for k, v in dictin.items():
        tmp = "%s='%s'" % (str(k), safe(str(v)))
        tmplist.append(' ' + tmp + ' ')
    return ' and '.join(tmplist)
def safe(s):
	return s

def send(m,c):
	from_addr = 'xmxj@cj.it592.com'
	password = '07070913zyll'
	to_addr = m
	smtp_server = "smtpdm.aliyun.com"

	msg = MIMEText(c, 'plain', 'utf-8')
	msg['From'] = from_addr
	msg['To'] = to_addr
	msg['Subject'] = Header(u'虾米小匠成绩更新通知', 'utf-8').encode()

	server = smtplib.SMTP(smtp_server, 25)
	server.set_debuglevel(1)
	server.login(from_addr, password)
	server.sendmail(from_addr, [to_addr], msg.as_string())
	server.quit()
def getUser():
	sql = getData('AddonOucJw_studentinfo',['id','username','password','mail'],0)
	cursor.execute(sql)
	data = []
	for x in cursor:
		data.append(x)
	return data

def getScore(user):
	sql = getData('AddonOucJw_studentscore',['coursename','year'],{'username_id':user})
	cursor.execute(sql)
	print(sql)
	data = []
	for x in cursor:
		data.append(x)
	return data
def main():
	ISOTIMEFORMAT='%Y-%m-%d %X'
	output.write(time.strftime( ISOTIMEFORMAT, time.localtime())+'begin\n')
	userdata = getUser()
	for x in userdata:
		oucjw = OucJw(x[1],x[2])
		t = (oucjw.login())
		if(t['status'] == '200'):
			data = oucjw.getScoreData()
			td = getScore(x[0])
			if len(data) == len(td):
				continue
			for v in td:
				del data[v[0]+v[1]]
			content = ''
			for (k,v) in data.items():
				temp = {'username_id':x[0],'coursename':v['coursename'],'coursetype':v['coursetype'],'year':v['year'],'jd':v['jd'],'score':v['score'],'xf':v['xf']}
				sql = insertData('AddonOucJw_studentscore',temp)
				content += v['coursename'] + v['score'] + ';\n'
				try:
					cursor.execute(sql)
					conn.commit()
				except Exception as e:
					print(e)
			if len(data):
				send('2943200389@qq.com',content)
	output.write(time.strftime( ISOTIMEFORMAT, time.localtime())+'end\n')

main()