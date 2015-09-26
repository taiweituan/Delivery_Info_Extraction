from dbConn import conn, cursor
from custInfo import getID, getInv

readdir = 'P:\\WebTeam\\Dev\\UPS-Tracking\\FEDEX.SFC'
writedir = 'P:\\WebTeam\\Dev\\UPS-Tracking\\Filtered_FEDEX.txt'

with open(readdir,'r') as getStuff:
	with open(writedir, 'w') as putStuff:
		manyStuff = getStuff.read().splitlines()
		
		# remove header
		manyStuff.pop(0)
		
		for stuff in range(0, len(manyStuff)):
			stuffList = manyStuff[stuff].split(',')
			ccAndSO = stuffList[2]
			mmddyyyy = stuffList[0]
			
			
			date = mmddyyyy[4:]+mmddyyyy[:4]
			salesOrder = ccAndSO[6:]
			customerCode = ccAndSO[:7]
			trackingNum = str(stuffList[3])
			
			invNum = ''
			
			getInvNum = getInv(salesOrder)
			
			if getInvNum == None :
				invNum = 'Not Found'
			else:
				invNum = getInvNum[0]
			
			result = '%s %s %s %s %s' % (salesOrder, trackingNum, customerCode, date, invNum)
			
			putStuff.writelines(result+'\n')
			print result