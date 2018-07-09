import csv, pyodbc
import os
import errno

def silentremove(filename):
    try:
        os.remove(filename)
    except OSError as e: # this would be "except OSError, e:" before Python 2.6
        if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
            raise # re-raise exception if a different error occurred
            
def extract_db_structure(csv_file, db_file, db_pwd):
    DRV = '{Microsoft Access Driver (*.mdb, *.accdb)}'
    DBQ = db_file
    PWD = db_pwd
    conn = pyodbc.connect('DRIVER={};DBQ={};PWD={}'.format(DRV,DBQ,PWD))
    curs_tables = conn.cursor()
    curs_fields = conn.cursor()  
    silentremove(csv_file)
    for table1 in curs_tables.tables():
        if table1.table_type == 'TABLE': 
            csv_row = []
            csv_row.append(table1.table_name)
            for column1 in curs_fields.columns(table=table1.table_name):
                csv_row.append(column1.column_name)
            with open(csv_file, 'a', newline='') as fou:
                csv_writer = csv.writer(fou)
                csv_writer.writerow(csv_row)
    curs_fields.close()
    curs_tables.close()
    conn.close()
            
db1_file = os.path.join('D:' + os.sep,'My Documents','BMS','BMS_ICP','BMS_ICP_2017','Data','db_Data.mdb')
db1_pwd = ''
db2_file = os.path.join('D:' + os.sep,'My Documents','BMS','BMS_ICP','BMS_ICP_2017','Data','db_Temp.mdb')
db2_pwd = ''
db3_file = os.path.join('D:' + os.sep,'My Documents','BMS','BMS_ICP','BMS_ICP_2017','Data','db_Temp2.mdb')
db3_pwd = ''
db4_file = os.path.join('D:' + os.sep,'My Documents','BMS','BMS_ICP','BMS_ICP_2017','Data','db_Audit.mdb')
db4_pwd = 'bmsicp2010'
db5_file = os.path.join('D:' + os.sep,'My Documents','BMS','BMS_ICP','BMS_ICP_2017','Config','db_Config.mdb')
db5_pwd = 'bmsicp2010'

db_files = [(db1_file, db1_pwd), (db2_file, db2_pwd), (db3_file, db3_pwd), (db4_file, db4_pwd), (db5_file, db5_pwd)]
for db in db_files:
    db_file = db[0]
    db_pwd = db[1]
    db_file_pre, db_file_ext = os.path.splitext(db[0])
    csv_file = db_file_pre + '.csv'
    extract_db_structure(csv_file, db_file, db_pwd)