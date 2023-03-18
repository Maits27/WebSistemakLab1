import csv
import datetime

with open('atala18.csv', 'w', newline='') as csvfile:
    fitxategi = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    fitxategi.writerow(['timestamp']+ ['cpu']+ ['ram'])
    for i in range(2):
        timestamp = datetime.datetime.now()
        cpu=i+1
        ram=i+5
        fitxategi.writerow([str(timestamp), str(cpu), str(ram)])