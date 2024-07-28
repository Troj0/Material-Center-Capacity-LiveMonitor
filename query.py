import pyodbc
try:
	conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
						'SERVER=SASTORE\SQLEXPRESS;'
						'UID=troj;'
						'PWD=01250125;'
						'DATABASE=Xp_CSAy2022; Trusted_connection = yes')
except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        if sqlstate == '42S22':
            print("Query value should only be INT")

cursor = conn.cursor()

def materialQuery(materialNo):
	cursor.execute('SELECT * FROM [Xp_CSAy2022].[dbo].[ItemsLocation] where itemnum = cast ({} as nvarchar)'.format(materialNo))
	for row in cursor.fetchall():
		print (row)

def locationButtonOnClick(buttonName):
		#print("SELECT top (999) [itemnum],[itemname],[itemnamee],[unitnamee],[QtyBalance] FROM [Xp_CSAy2022].[dbo].[InventroyListWithLocation] where storloc1 = cast ('{}' as nvarchar);".format(buttonName))
	txn = []
	cursor.execute("SELECT ALL [itemnum],[QtyBalance],[unitnum],[batchnum],[expdate],[AreaName] FROM [Xp_CSAy2022].[dbo].[QtyBalanceWithChargesAndLocation] where [batchnum] = cast('{}' as nvarchar ) AND QtyBalance > 0;".format(buttonName))
	for rows in cursor.fetchall():
		txn.append({
			"Material": rows[0],
			"Quantity": rows[1],
			"unitnum": rows[2],
			"Location": rows[3],
			"expdate": rows[4],
			"Owner Area": rows[5]
		})
	return txn

def colorOnContents(buttonName):
	cursor.execute("SELECT ALL [itemnum],[QtyBalance],[unitnum],[batchnum],[expdate],[AreaName] FROM [Xp_CSAy2022].[dbo].[QtyBalanceWithChargesAndLocation] where [batchnum] = cast('{}' as nvarchar ) AND QtyBalance > 0;".format(buttonName))
	exist = cursor.fetchone()
	fgColor = ''

	if exist is not None: fgColor = 'red'
	else: fgColor = 'green'
	return fgColor

def fetchDescription(materialNo):
	cursor.execute("SELECT TOP 999 [itemname] FROM [Xp_CSAy2022].[dbo].[items] where itemnum = '{}'".format(materialNo))
	row = cursor.fetchone()
	description = {"Description": row[0]}
	return description

def locationUsed(buttonName):

	cursor.execute("SELECT ALL [itemnum],[QtyBalance],[unitnum],[batchnum],[expdate],[AreaName] FROM [Xp_CSAy2022].[dbo].[QtyBalanceWithChargesAndLocation] where [batchnum] = cast('{}' as nvarchar ) AND QtyBalance > 0;".format(buttonName))
	exist = cursor.fetchone()

	if exist is not None: 
		return True
	else: 
		return False

# OLD QUERY:
#	cursor.execute("SELECT top (999) [itemnum],[itemname],[itemnamee],[unitnamee],[QtyBalance] FROM [Xp_CSAy2022].[dbo].[InventroyListWithLocation] where storloc1 = cast ('{}' as nvarchar) AND [QtyBalance] > 0 OR storloc2 = cast ('{}' as nvarchar) AND [QtyBalance] > 0 OR storloc3 = cast ('{}' as nvarchar) AND [QtyBalance] > 0 OR storloc4 = cast ('{}' as nvarchar) AND [QtyBalance] > 0 OR storloc5 = cast ('{}' as nvarchar) AND [QtyBalance] > 0 OR storloc6 = cast ('{}' as nvarchar) AND [QtyBalance] > 0 OR storloc7 = cast ('{}' as nvarchar) OR storloc8 = cast ('{}' as nvarchar) AND [QtyBalance] > 0;".format(buttonName, buttonName, buttonName, buttonName, buttonName, buttonName, buttonName, buttonName))
