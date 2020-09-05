import sqlite3
import csv
from collections import Counter
import matplotlib.pyplot as plt
import tldextract

def is_third_party(top_level_url, url):
    ext1 = tldextract.extract(top_level_url)
    ext2 = tldextract.extract(url)
    if ext1.domain == ext2.domain and ext1.subdomain == ext2.subdomain and ext1.suffix == ext2.suffix:
        return False
    return True

conn = sqlite3.connect("/home/ian/Desktop/crawl_with_adblock/crawl-data.sqlite")
cur = conn.cursor()
cur.execute("""select
                visit_id,
                top_level_url,
                url
                from http_requests;""")
results = cur.fetchall()
cur.close()
conn.close()

all_requests = []
sites = []
with open('/home/ian/Downloads/top-1m.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in spamreader:
        a = row[0].split(',')
        sites.append([a[1], 0])
        if a[0] == '100':
            break

for result in results:
    top_level_url = result[1]
    url = result[2]
    visit_id = int(result[0]) - 1

    third_party = is_third_party(top_level_url, url)
    if third_party:
        sites[visit_id][1] += 1

        ext = tldextract.extract(url)
        domain = ext.domain + '.' + ext.suffix
        all_requests.append(domain)


top_10 = Counter(all_requests).most_common(10)
for i in range(10):
    print ("{}.   {} requests,   '{}'".format(str(i+1), top_10[i][1], top_10[i][0]))

sites = sorted(sites, key = lambda x: x[1])
fig = plt.figure()
ax = fig.add_subplot(111)
x = [x[0] for x in sites]
y = [x[1] for x in sites]
ax.axes.xaxis.set_visible(False)

ax.bar(x, y)
plt.show()







