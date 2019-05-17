import urllib3
from bs4 import BeautifulSoup
import csv
import argparse, sys
from datetime import datetime

#timeset
waktu = datetime.now()
tahun = waktu.year
bulan = waktu.month
hari = waktu.day

#argumenset

parser = argparse.ArgumentParser()
parser.add_argument('--search', help='input keyword', nargs='+')

args = parser.parse_args()
keyword = ''.join(args.search)
keyword1 = str(keyword)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
http = urllib3.PoolManager()

#createCSV

with open('malshare/malshare-{}-{}-{}-{}.csv'.format(tahun, bulan, hari, keyword1), 'w') as csvfile:

    writecsv = csv.writer(csvfile)
    writecsv.writerow(["Date", "Domain", "File Type", "Detail"])

    url = http.request('GET', 'https://malshare.com/search.php?query=%s' % keyword1)
    data = url.data

    bs = BeautifulSoup(data, 'lxml')
    table_body = bs.find('body')
    rows = table_body.find_all('tr', class_=None)[1:]

    for row in rows:
        kolom = row.findAll('td')
        if len(kolom) > 1:
            writecsv.writerow([kolom[2].text, kolom[3].text, kolom[1].text, str("https://malshare.com/sample.php?action=detail&hash=%s" % kolom[0].text)])

print ("malshare-%s-%s-%s-%s.csv" % (tahun, bulan, hari, keyword1))
