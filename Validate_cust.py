# ///////////////////////////////
# VALIDATE CUSTOMERS & CREATE CSV
# ///////////////////////////////
import csv, time, timeit, shutil, os, datetime
from dbConn import conn, cursor
from datetime import datetime

def ckCust(_company, _tel):
	result = False
	if len(_tel)  >= 13:
		_tel_split = _tel.split(' ')
		_tel_areacode = _tel_split[0].replace('(', '')
		_tel_areacode = _tel_areacode.replace(')', '')
		_telnew = _tel_areacode + "/" + _tel_split[1][0:3] + "-" + _tel_split[1][3:]
	try:
		SQL = "select top 1 custno from lsCustomers where (company like '%{0}%' or phone like '{1}')".format(_company, _telnew)
		cursor.execute(SQL)
		rows=cursor.fetchall()
		conn.commit()

		if len(rows) > 0:
			result = True
	except:
		pass
	return result		
	
#print ckCust("I-NET DVR", "(630) 741-2500")

# name, company name, tel, email

readdir = 'C:\\eBlast_Lead.csv'
writedir = 'C:\\Users\\taiwei\\Desktop\\New folder (2)\\validate_cust.csv'
with open(readdir,'rb') as read_file:
	# skip header
	next(read_file)
	with open(writedir, 'wb')as write_file:
		writer = csv.writer(write_file)
		reader = csv.reader(read_file)
		existCustomer = ""
		trueCnt = 0
		for record in reader:
			name = record[0] + " " + record[1]
			companyName = record[3]
			telNum = record[-2]
			if len(telNum) > 14:
				telNum = telNum[:14]
			emailAddress = record[6]
			
			if ckCust(companyName, telNum) == True:
				result = []
				result.extend([name, companyName, telNum, emailAddress])
				
				writer.writerows([result])
				print name + " , " + companyName+ " , " +telNum+ " , " +emailAddress
				#print name + " , " + companyName+ " , " +telNum+ " , " +emailAddress
			
				
			