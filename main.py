import requests
from bs4 import BeautifulSoup
import chromadb

#Get wikipedia page, output raw text
#parsede_html.body.find line is important; for a particular page format (i.e. non wikipedia), may need to change attrs searched for
def getPageContent():
    r = requests.get('https://en.wikipedia.org/wiki/Chindians#:~:text=Chindian%20(Chinese%3A%20%E4%B8%AD%E5%8D%B0%E4%BA%BA,to%20modern%20China%20and%20India.')
    print(r.status_code)

    html = r.content
    parsed_html = BeautifulSoup(html)
    temp_body = parsed_html.body.find('div', attrs={'class':'mw-parser-output'}).text
    return temp_body

#Vectorize content
def vectorize_content(temp_list):
    client = chromadb.Client()
    collection = client.create_collection("temp_collection")
    collection.add(
        documents= temp_list,
        metadatas=[{"source":"wikipedia"}],
        ids=["doc1"]
    )
    return collection

temp = getPageContent()
temp_collection = vectorize_content(temp)
results = temp_collection.query(
    query_texts=["Indian"],
    n_results = 2
)

print(results)