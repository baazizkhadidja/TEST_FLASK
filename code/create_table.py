import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()


create_table = "CREATE TABLE IF NOT EXISTS accounts (id INTEGER PRIMARY KEY, name TEXT)"
cursor.execute(create_table)
cursor.execute("INSERT INTO accounts (id, name) VALUES (1, 'ABC'), (2, 'DEF'), (3, 'GHI'), (4, 'JKL')")


create_table = "CREATE TABLE IF NOT EXISTS malls (id INTEGER PRIMARY KEY, name TEXT, account_id INTEGER, FOREIGN KEY (account_id) REFERENCES accounts (id))"
cursor.execute(create_table)
cursor.execute("INSERT INTO malls (id, name, account_id) VALUES (6, 'My place', 1), (7, 'Soleil', 2), (8, 'Westfield', 3), (9, 'Village', 4)")

create_table = "CREATE TABLE IF NOT EXISTS units (id INTEGER PRIMARY KEY, name TEXT, mall_id INTEGER, FOREIGN KEY (mall_id) REFERENCES malls (id))"
cursor.execute(create_table)
cursor.execute("INSERT INTO units (id, name, mall_id) VALUES (10, 'Sephora', 6), (11, 'Auchan', 7), (12, 'H&M', 8), (13, 'Action', 9)")



connection.commit()

connection.close()