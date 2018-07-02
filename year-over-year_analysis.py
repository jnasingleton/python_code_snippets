
# This script creates a year-over-year database file of all provided csv file
# Field names etc would need to be adjusted depending on the source csv file

def table_exists(cur, table)
	sql = "SELECT name FROM sqlite_master WHERE type='table' AND name='" + table + "';"
	table_exists = cur.execute(sql).fetchone()[0]
	return table_exists

import csv, sqlite3

#csv_file is the source csv file containing year as an index field, other index fields, and a value field.
csv_file = "combined_csv.csv"

con = sqlite3.connect("year-over-year-analysis.db")

cur = con.cursor()

# tbl_temp
table1 = 'tbl_temp'
if table_exists(cur, table1)
	sql = 'DROP TABLE ' + table1 + ' '
	cur.execute(sql)
sql = 'CREATE TABLE ' + table1 + ' '
sql += '( '
sql += 'province, year, molecule, level1, level2, level3, level4, level5, value '
sql += '); '
cur.execute(sql)

# tbl_temp2
table2 = 'tbl_temp2'
if table_exists(cur, table2)
	sql = 'DROP TABLE ' + table2 + ' '
	cur.execute(sql)
cur.execute(sql)
sql = 'CREATE TABLE ' + table2 + ' '
sql += '( '
sql += 'province, year, molecule, level1, level2, level3, level4, level5, value '
sql += '); '
cur.execute(sql)

# Import to tbl_temp and tbl_temp2
with open(csv_file,'r') as file:
    dr = csv.DictReader(file)
    to_db = [(i['province'], i['year'], i['molecule'], i['level1'], i['level2'], i['level3'], i['level4'], i['level5'], i['value']) for i in dr]

# tbl_temp2
sql = 'INSERT INTO ' + table1 + ' (province, year, molecule, level1, level2, level3, level4, level5, value) '
sql += 'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);'
cur.executemany(sql, to_db)

# tbl_temp2
sql = 'INSERT INTO ' + table2 + ' (province, year, molecule, level1, level2, level3, level4, level5, value) '
sql += 'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);'
cur.executemany(sql, to_db)

# tbl_output
table3 = 'tbl_output'
if table_exists(cur, table3)
	sql = 'DROP TABLE ' + table3 + ' '
	cur.execute(sql)
sql = 'CREATE TABLE ' + table3 + ' '
sql += '( '
sql += 'province, year_pre, year_post, molecule, level1, level2, level3, level4, level5, value_pre, value_post, value_diff, value_diff_percent '
sql += '); '
cur.execute(sql)

# Insert to tbl_output
sql = 'SELECT year*1 FROM ' + table1 + ' GROUP BY year'
years = cur.execute(sql).fetchall()
for year_post in years:
	year_post = year_post[0]
	for year_pre in years:
		year_pre = year_pre[0]

		if year_pre < year_post:

			print(year_pre, year_post)

			sql = 'INSERT INTO '
			sql += 'tbl_output '
			sql += 'SELECT '
			sql += 'T1.province, '
			sql += 'T1.[year] as year_pre, '
			sql += 'T2.[year] as year_post, '
			sql += 'T1.molecule, '
			sql += 'T1.level1, T1.level2, T1.level3, T1.level4, T1.level5, '
			sql += 'T1.[value] as value_pre, '
			sql += 'T2.[value] as value_post, '
			sql += '(T2.[value] - T1.[value]) as value_diff, '
			sql += '((T2.[value] - T1.[value])/T1.[value]) as value_diff_percent '
			sql += 'FROM '
			sql += 'tbl_temp as T1, '
			sql += 'tbl_temp2 as T2 '
			sql += 'WHERE '
			sql += '(T1.province = T2.province) '
			sql += 'and (T1.molecule = T2.molecule) '
			sql += 'and (T1.level1 = T2.level1) and (T1.level2 = T2.level2) and (T1.level3 = T2.level3) and (T1.level4 = T2.level4) and (T1.level5 = T2.level5) '
			sql += 'and T1.[year]*1 = ' + str(year_pre) + ' '
			sql += 'and T2.[year]*1 = ' + str(year_post) + ' '
			cur.execute(sql)

con.commit()
con.close()

