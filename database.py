import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="MyNewPass",
  database="airTaskerScrap"

)

mycursor = mydb.cursor()


# mycursor.execute("""CREATE TABLE tasks (
#     slug VARCHAR(255),
#     name VARCHAR(255), 
#     classification VARCHAR(255), 
#     applied VARCHAR(255) )""")


def insert_values(slug, name, classification, applied):
    sql = f"""SELECT *
    FROM tasks
    WHERE slug='{slug}'"""
    
    mycursor.execute(sql)
    result = mycursor.fetchall()
    if len(result) == 0:
        sql = "INSERT INTO tasks (slug, name, classification, applied) VALUES (%s, %s, %s, %s)"
        val = (slug, name, classification, applied)
        mycursor.execute(sql, val)
        mydb.commit()
    else:
        print("Task is already in the DDBB")
    
insert_values("/at/123123224/walk-my-dogs", "walk my dogs", "cv", "No")

def add_column():
    sql = """ALTER TABLE tasks
    ADD id INT AUTO_INCREMENT PRIMARY KEY FIRST"""
    mycursor.execute(sql)
    mydb.commit()
    
# add_column()


def records():
    sql = """SELECT *
    FROM tasks
    WHERE applied='Yes'"""
    
    mycursor.execute(sql)
    result = mycursor.fetchall()
    print(len(result))
        
        
# records()