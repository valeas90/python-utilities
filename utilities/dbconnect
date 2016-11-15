# -*-coding:utf-8-*-
"""
***********************************************************************************************************************
                                                dbconnect()

Class wrapper to minimize code duplication in any given project when operating with a MySQL type database.
Just instantiate the class and use dbcursor to launch querys. For example:
db = dbconnect.Dbconnect(conf)
*Important note: ConfigParser instance must be passed with the necessary data. 
Otherwise, hard-coded values must be added, or refactor the code.

db.dbcursor.execute('SELECT * FROM %s' % table_name) 
or 
db.dbcursor.execute('SELECT * FROM {table_name} WHERE FIELD_1 != %s'.format(table_name=table_name), (field_value,))

dbcursor is built as a generator so it can be iterated both ways.
results = db.dbcursor.fetchall() 
for result in results:
	pass
or 
for result in db.dbcursor:
	pass
Obviously, using the second way will only allow you to iterate over it once.

***********************************************************************************************************************
"""

import MySQLdb

class Dbconnect(object):

    def __init__(self, conf):
        self.dbconection = MySQLdb.connect(host=conf.get('mysql_data', 'DATABASE_DESA_HOST'),
                                           port=int(conf.get('mysql_data', 'DATABASE_DESA_PORT')),
                                           user=conf.get('mysql_data', 'DATABASE_DESA_USER'),
                                           passwd=conf.get('mysql_data', 'DATABASE_DESA_PASSWD'),
                                           db=conf.get('mysql_data', 'DATABASE_DESA_DB'))
        self.dbcursor = self.dbconection.cursor()

    def close_db(self):
        self.dbcursor.close()
        self.dbconection.close()
    def commit_db(self):
        self.dbconection.commit()
