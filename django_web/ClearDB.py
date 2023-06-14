import MySQLdb as mysql

db = mysql.connect(
    host="localhost",
    user="root",
    passwd="111111",
    database="softwareproject"
)
print(db)
cursor = db.cursor()
# defining the Query
query = "truncate table django_web_douban"

# executing the query
cursor.execute(query)

# final step to tell the database that we have changed the table data
db.commit()
db.close()
