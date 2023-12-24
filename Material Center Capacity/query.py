import pyodbc
try:
	conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
						'SERVER=SASTORE\SQLEXPRESS;'
						'UID=;'
						'PWD=;'
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
	cursor.execute("SELECT top (999) [itemnum],[itemname],[itemnamee],[unitnamee],[QtyBalance] FROM [Xp_CSAy2022].[dbo].[InventroyListWithLocation] where storloc1 = cast ('{}' as nvarchar) OR storloc2 = cast ('{}' as nvarchar) OR storloc3 = cast ('{}' as nvarchar) OR storloc4 = cast ('{}' as nvarchar) OR storloc5 = cast ('{}' as nvarchar) OR storloc6 = cast ('{}' as nvarchar) OR storloc7 = cast ('{}' as nvarchar) OR storloc8 = cast ('{}' as nvarchar);".format(buttonName, buttonName, buttonName, buttonName, buttonName, buttonName, buttonName, buttonName))
	for row in cursor.fetchall():
		print (row)

def colorOnContents(buttonName):
	cursor.execute("SELECT top (999) [itemnum],[itemname],[itemnamee],[unitnamee],[QtyBalance] FROM [Xp_CSAy2022].[dbo].[InventroyListWithLocation] where storloc1 = cast ('{}' as nvarchar) AND [QtyBalance] > 0 OR storloc2 = cast ('{}' as nvarchar) AND [QtyBalance] > 0 OR storloc3 = cast ('{}' as nvarchar) AND [QtyBalance] > 0 OR storloc4 = cast ('{}' as nvarchar) AND [QtyBalance] > 0 OR storloc5 = cast ('{}' as nvarchar) AND [QtyBalance] > 0 OR storloc6 = cast ('{}' as nvarchar) AND [QtyBalance] > 0 OR storloc7 = cast ('{}' as nvarchar) OR storloc8 = cast ('{}' as nvarchar) AND [QtyBalance] > 0;".format(buttonName, buttonName, buttonName, buttonName, buttonName, buttonName, buttonName, buttonName))
	exist = cursor.fetchone()
	fgColor = ''

	if exist is not None: fgColor = 'red'
	else: fgColor = 'green'
	return fgColor

def countRedButtons(buttonName):
	buttonTexts = ["A", "B", "C", "D", "E", "F", "G", "H", "J", "K", "L"]
	buttonDictExist = {buttonText: 0 for buttonText in buttonTexts}
	buttonDictNonExist = {buttonText: 0 for buttonText in buttonTexts}
	
	cursor.execute("SELECT top (999) [itemnum],[itemname],[itemnamee],[unitnamee],[QtyBalance] FROM [Xp_CSAy2022].[dbo].[InventroyListWithLocation] where storloc1 = cast ('{}' as nvarchar) AND [QtyBalance] > 0 OR storloc2 = cast ('{}' as nvarchar) AND [QtyBalance] > 0 OR storloc3 = cast ('{}' as nvarchar) AND [QtyBalance] > 0 OR storloc4 = cast ('{}' as nvarchar) AND [QtyBalance] > 0 OR storloc5 = cast ('{}' as nvarchar) AND [QtyBalance] > 0 OR storloc6 = cast ('{}' as nvarchar) AND [QtyBalance] > 0 OR storloc7 = cast ('{}' as nvarchar) OR storloc8 = cast ('{}' as nvarchar) AND [QtyBalance] > 0;".format(buttonName, buttonName, buttonName, buttonName, buttonName, buttonName, buttonName, buttonName))
	exist = cursor.fetchone()

	if exist is not None: 
		for buttonText in buttonTexts:
			if buttonName.startswith(buttonText):
				buttonDictExist[buttonText] += 1
	else: 
		for buttonText in buttonTexts:
			if buttonName.startswith(buttonText):
				buttonDictNonExist[buttonText] += 1
	return buttonDictExist, buttonDictNonExist
