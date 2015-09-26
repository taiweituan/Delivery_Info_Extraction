import csv
import time
from dbConn import conn, cursor
from custInfo import getID, getInv


readdir = 'C:\\UPS_NCSV_EXPORT.csv'
writedir = 'C:\\Users\\taiwei\\Desktop\\test.csv'
with open(readdir,'rb') as ups_file:
	with open(writedir, 'wb')as write_file:
		writer = csv.writer(write_file, delimiter=',')
		reader = csv.reader(ups_file)
		
		# date in YYYYMMDD format
		currentdate = int(time.strftime("%Y%m%d"))
		#twoYearsAgoDate = currentdate - 20000
		twoYearsAgoDate = currentdate - 300
		
		# buffers for speeding up process and use less resources
		soBuffer = 0
		invNumberBuffer = None
		
		for record in reader:
			invNumberFromInv = ''
			ccFromInv = ''
			salesPersonFromInv = ''
			
			if 'R' in record[0]:
				continue
				
			if int(record[16]) < twoYearsAgoDate:
				continue
			
			# if '/' is found, separate the string
			elif '/' in record[0]:					
				tempList = record[0].split("/")
				# loop through list to validate SO
				pos = 0
				while pos < len(tempList):					
					# check if SO only contains digits
					if not tempList[pos].isdigit():
						tempList.pop(pos)
						pos-=1
					pos+=1
				
				for result in tempList:	
					#get invoice info 
					invNumber = getInv(result)
					
					if invNumber != None:
						invNumberFromInv =  str(invNumber[0])
						salesPersonFromInv = str(invNumber[2])					
				
					# check if no customerCode, then check database to retrieve one
					if record[2] == '': 
						address = str(record[8])
						date = str(record[16])
						getCCID = getID(address, date)
						
						if (getCCID == '') or (getCCID == None) or len(getCCID) < 2:
							# check invoice # if customerCode can be found for the last time!!
							if invNumber == None:
								invNumberResult = "CC Not Found!"
							else:
								# add CC if found after search using invNumber
								record[2] = str(invNumber[1])
							
						else:
							ccID = getID(address, date)[0]
							record[2] = ccID
						
					# don't write to file if Salesperson is 'RM'
					if not "RM" in salesPersonFromInv and not len(salesPersonFromInv) > 2:
						# get Invoice Number
						finalResult = []
						finalResult.extend([result, record[1],record[2],record[3],record[8],record[16], invNumberFromInv,salesPersonFromInv])
						writer.writerows([finalResult])
						print finalResult
						
			# check if SO is valid 
			elif record[0].isdigit():
				#get invoice info 
				invNumber = getInv(record[0])
				
				if not invNumber == None:
					print invNumber
					invNumberFromInv =  str(invNumber[0])
					salesPersonFromInv = str(invNumber[2])		
					
				# check if no customerCode, then check database to retrieve one
				if record[2] == '': 
					address = str(record[8])
					date = str(record[16])
					getCCID = getID(address, date)
					
					if (getCCID == '') or (getCCID == None) or len(getCCID) < 2:
						# check invoice # if customerCode can be found for the last time!!
						if invNumber == None:
							invNumberResult = "CC Not Found!"
						else:
							# add CC if found after search using invNumber
							record[2] = str(invNumber[1])
						
					else:
						ccID = getID(address, date)[0]
						record[2] = ccID
					
				# don't write to file if Salesperson is 'RM'
				if not "RM" in salesPersonFromInv and not len(salesPersonFromInv) > 2:
					# get Invoice Number
					finalResult = []
					finalResult.extend([record[0], record[1],record[2],record[3],record[8],record[16], invNumberFromInv,salesPersonFromInv])
					writer.writerows([finalResult])
					print finalResult
				
				
		input = raw_input('Finished!')
		conn.close()