import csv

with open("data\\playerdata.csv", "r") as f:
    reader = csv.reader(f)
    data = list(reader)

print(data)
