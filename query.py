import pyodbc
import os

creds = {}
creds_file = open('config.ini')
for line in creds_file:
    line = line.strip()  # Remove leading and trailing whitespace
    if "=" in line:
        key, value = line.split("=", 1)
        creds[key.strip()] = value.strip()  # Remove leading and trailing whitespace from key and value
    else:
        print(f"Invalid line format: {line.rstrip()}")
creds

# assign creds
driver = 'ODBC Driver 17 for SQL Server'
server = creds.get("SERVER")
db = creds.get("DATABASE")
user = creds.get("un")
password = creds.get("password")

# using pyodbc connect to MS SQL server usign credentials in .env 
cnxn_str = f"DRIVER={driver};SERVER={server};DATABASE={db};UID={user};PWD={password}; Trusted_connection = yes;"
cnxn = pyodbc.connect(cnxn_str)
try:
	conn = cnxn
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
