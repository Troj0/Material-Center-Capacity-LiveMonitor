import pyodbc
import pandas as pd

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

def dataExport():
    data = {"itemnum": [], "itemnamee": [], "qty": [], "unitnamee": [], "Area": [],
            "storloc1": [], "storloc2": [], "storloc3": [], "storloc4": [], "storloc5": [],
            "storloc6": [], "storloc7": [], "storloc8": [], "storloc9": [], "storloc10": [],
            "storloc11": [], "storloc12": [], "storloc13": [], "storloc14": [], "storloc15": []}

    cursor.execute("SELECT ALL [itemnum],[itemnamee],[qty],[unitnamee],[AreaName],[storloc1],[storloc2],[storloc3],[storloc4],[storloc5],[storloc6],[storloc7],[storloc8],[storloc9],[storloc10],[storloc11],[storloc12],[storloc13],[storloc14],[storloc15] FROM [Xp_CSAy2022].[dbo].[v_b2_names1_Area]")

    for row in cursor.fetchall():
        data["itemnum"].append(row[0])
        data["itemnamee"].append(row[1])
        data["qty"].append(row[2])
        data["unitnamee"].append(row[3])
        data["Area"].append(row[4])
        data["storloc1"].append(row[5])
        data["storloc2"].append(row[6])
        data["storloc3"].append(row[7])
        data["storloc4"].append(row[8])
        data["storloc5"].append(row[9])
        data["storloc6"].append(row[10])
        data["storloc7"].append(row[11])
        data["storloc8"].append(row[12])
        data["storloc9"].append(row[13])
        data["storloc10"].append(row[14])
        data["storloc11"].append(row[15])
        data["storloc12"].append(row[16])
        data["storloc13"].append(row[17])
        data["storloc14"].append(row[18])
        data["storloc15"].append(row[19])

    df = pd.DataFrame(data)
    df.to_csv('export_data.csv', index=False)

dataExport()