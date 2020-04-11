import requests
import csv
import json
from multiprocessing import Pool, Process

years = [2019, 2018, 2017]
baseUrl = "https://ieeexplore.ieee.org/rest"

path = {2019: "/search/pub/8907344/issue/8916833/toc", 2018: '/search/pub/8543039/issue/8569013/toc',
        2017: '/search/pub/8307147/issue/8317580/toc'}
punumbers = {
    2019: "8907344",
    2018: "8543039",
    2017: "8307147"
}
isnumber = {
    2019: 8916833,
    2018: 8569013,
    2017: 8317580
}
headers = {"Origin": "https://ieeexplore.ieee.org"}


def spider(page, year):
    print("Page: "+str(page))
    print("Year: "+str(year))
    res = requests.post(baseUrl+path[year], json={"rowsPerPage": "100",
                                                  "pageNumber": page, "punumber": punumbers[year], "isnumber": isnumber[year]}, headers=headers).json()
    total = []
    print(len(res["records"]))
    index = 0
    for record in res["records"]:
        print("Record: "+str(index))
        index += 1
        authors = record.get('authors', None)
        if(not authors):
            continue
        authorName = authors[0]["preferredName"]
        authorId = authors[0].get('id', None)
        text = [authorName, record["articleTitle"]]
        if(authorId):
            data = requests.get(
                baseUrl+'/author/{}'.format(authorId), headers=headers).json()
            text.insert(1, data[0].get(
                "currentAffiliation", ""))
        total.append(text)
    return total, year


def save(t):
    (total, year) = t
    print("Save "+str(year))
    with open('res-'+str(year)+'.csv', 'a', encoding='utf-8', newline="") as f:
        writer = csv.writer(f)
        writer.writerows(total)


if __name__ == "__main__":
    pool = Pool(4)
    for year in years:
        for page in range(0, 9):
            pool.apply_async(spider, (page, year), callback=save)
    pool.close()
    pool.join()
