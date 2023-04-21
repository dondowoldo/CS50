from cs50 import SQL

db = SQL("sqlite:///database.db")

sut = db.execute("SELECT * FROM users")

print(sut[0]["hash"])
