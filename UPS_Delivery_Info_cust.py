from dbConn import conn, cursor
from custInfo import getID, getInv

address = "46523 INVERNESS"
date = '20140611'
getCCID = getID(address, date)
# if (getCCID == '') or (getCCID == None) or len(getCCID) < 2:
	# print 'not found'
# else:
	# print "'"+getID(address, date) + "'"

# return ('MS5618', '725908', 'HC')
print getInv("77433")
# return ('', 'JM7840', 'IW')
