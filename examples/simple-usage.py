from fyCursor import connect

cursor = connect("database.db")

# you can execute basic sqlite3 script if fyCursor does not have its functionality yet.
cursor.execute("""
    CREATE TABLE myTable(
        id INTEGER PRIMARY KEY
        name STRING
        money INTEGER
""") #creating a table

# get money of user with name "felix"
felixMoney = cursor.select("money", from_="myTable").where(name="felix").one()

# change money of user with id 5
cursor.update("myTable").set(money=349).where(id=5).commit()

# add 5 to money to all users
cursor.update("myTable").add(money=5).commit()

