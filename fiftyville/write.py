import csv
from cs50 import SQL
db = SQL("sqlite:///fiftyville.db")


#interviews = db.execute("select * from interviews")

#with open("interview.txt", "w") as f:
 #   fieldnames = interviews[0]
  #  writer = csv.DictWriter(f, fieldnames)
   # for row in interviews:
    #    writer.writerow(row)

def writeTable(table):
    database = db.execute(f"select * from {table}")

    with open(f"{table}.txt", "w") as f:
        fieldnames = database[0]
        writer = csv.DictWriter(f, fieldnames)
        for row in database:
            writer.writerow(row)

writeTable("crime_scene_reports")