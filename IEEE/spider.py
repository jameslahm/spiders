import requests
import csv
import json
from multiprocessing import Pool, Process

pages = range(0, 8)
baseUrl = "https://ieeexplore.ieee.org/rest"

path = "/search/pub/8907344/issue/8916833/toc"
headers = {"Origin": "https://ieeexplore.ieee.org"}


def spider(page):
    print("Page: "+str(page))
    res=requests.post(baseUrl+path, json={"rowsPerPage": "100",
        "pageNumber": page, "punumber": "8907344", "isnumber": 8916833},headers=headers).json()
    total = []
    print(len(res["records"]))
    index=0
    for record in res["records"]:
        print("Record: "+str(index))
        index+=1
        authors = [x["preferredName"] for x in record.get("authors", [])]
        authorsId = [x["id"] for x in record.get("authors", [])]
        for i in range(0, len(authorsId)):
            data = requests.get(
                baseUrl+'/author/{}'.format(authorsId[i]), headers=headers).json()
            authors[i]=authors[i]+" "+data[0].get("currentAffiliation","")
        authors.append(record["articleTitle"])
        total.append(authors)
    return total


def save(total):
    print("Save")
    with open('res.csv', 'a',encoding='utf-8',newline="") as f:
        writer = csv.writer(f)
        writer.writerows(total)




if __name__ == "__main__":
    # p = Process(target=spider, args=(0,))
    # p.start()
    # p.join()
    pool=Pool(1)
    for page in range(8,9):
        pool.apply_async(spider,(page,),callback=save)
    pool.close()
    pool.join()
