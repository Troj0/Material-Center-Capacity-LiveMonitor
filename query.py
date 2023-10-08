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
	cursor.execute("SELECT top (999) [itemnum],[itemname],[itemnamee],[unitnamee],[QtyBalance] FROM [Xp_CSAy2022].[dbo].[InventroyListWithLocation] where storloc1 = cast ('{}' as nvarchar);".format(buttonName))
	for row in cursor.fetchall():
		print (row)

def colorOnContents(buttonName):
	cursor.execute("SELECT top (999) [itemnum],[itemname],[itemnamee],[unitnamee],[QtyBalance] FROM [Xp_CSAy2022].[dbo].[InventroyListWithLocation] where storloc1 = cast ('{}' as nvarchar);".format(buttonName))
	exist = cursor.fetchone()
	fgColor = ''
	
	if exist is not None: fgColor = 'red'
	else: fgColor = 'green'
	return fgColor