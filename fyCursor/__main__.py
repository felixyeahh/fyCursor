'''from fyCursor import Table, Field, connect

cursor = connect("database.db")

# --------------------------------------------------------------------------------------//
#                                   CREATING A TABLE
# --------------------------------------------------------------------------------------//

# you can execute basic sqlite3 script if fyCursor does
# not have its functionality yet.
cursor.execute("""
    CREATE TABLE IF NOT EXISTS myTable(
        id INTEGER PRIMARY KEY,
        name STRING,
        money INTEGER
    )
""")  # creating a table

# you can also create a table using fyCursor method:
AnotherTable = Table(
    name="AnotherTable",
    cursor=cursor,
    kwargs_fields={
        "id": Field(primary_key=True),
        "name": Field(
            name='name',
            default="Does not have name",
            nullable=False
        ),
        "money": Field(default=12)
    }
)

# Now there are two versions of creating table,
# but they are working totally same:
AnotherTable.create(if_not_exist=True)
cursor.create_table(AnotherTable, if_not_exist=True)

# --------------------------------------------------------------------------------------//
#                                    GETTING VALUES
# --------------------------------------------------------------------------------------//


# get money of user with name "felix"
felixMoney = cursor.select("money", from_="myTable").where(name="felix").one()

# change money of user with id 5
cursor.update("myTable").set(money=349).where(id=5).commit()

# add 5 to money to all users
cursor.update("myTable").add(money=5).commit()
'''
