import os
import csv

def processData(filename):
    path = f"./uploads/{filename}"
    with open(path) as csv_file:
        csvReader = csv.reader((csv_file), delimiter=',')
        lineCount = 0
        data = []
        for row in csvReader:
            if lineCount == 0:
                print("Column header, skipping")
                lineCount += 1
            else:
                if row[3] == "":
                    row[3] = "[]"
                lineData = (row[0], row[1], row[2], row[3])
                data.append(lineData)
                lineCount += 1
        return data