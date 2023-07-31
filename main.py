import requests
from bs4 import BeautifulSoup
import chromadb

import subprocess

#Get wikipedia page, output raw text
#parsed_html.body.find line is important; for a particular page format (i.e. non wikipedia), may need to change attrs searched for
def getPageContent():
    r = requests.get('https://en.wikipedia.org/wiki/Chindians#:~:text=Chindian%20(Chinese%3A%20%E4%B8%AD%E5%8D%B0%E4%BA%BA,to%20modern%20China%20and%20India.')
    print(r.status_code)

    html = r.content
    parsed_html = BeautifulSoup(html)
    temp_body = parsed_html.body.find('div', attrs={'class':'mw-parser-output'}).text
    return temp_body

#Remove junk lines from textbook
def cleanTextbook(outputFileName):
    with open(outputFileName, 'r', encoding="UTF-8") as fr:
        lines = fr.readlines()

        with open(outputFileName,'w',encoding="UTF-8") as fw:
            for line in lines:
                if("file:///D|/Documents" not in line):
                    fw.write(line)

#TODO:Remove non alphanum chars
#necessary? requires further testing
def preprocessText(outputFileName):
    with open(outputFileName, 'r', encoding="UTF-8") as fr:
        with open(outputFileName,'w',encoding="UTF-8") as fw:
            lines = fr.readlines()
            for line in lines:
                data = data.replace(",","")
                fw.write(data)

#Return contents of some textbook as a list of list of strings, where each list of strings is a chapter 
def getTextbookContent():
    outputFileName = 'output.txt'
    #Convert pdf contents to txt file
    subprocess.call(['pdftotext','TCPIP_Illustrated.pdf',outputFileName])
    cleanTextbook(outputFileName)

    #Parse txt and convert each chapter into a list of strings
    with open(outputFileName, "r",encoding="UTF-8") as f:
        lines = f.readlines()
        n=1
        #list of strings
        masterList = []
        #strings
        tempChapterDoc = ""
        endOfTOC = 0
        for line in lines:
            if(endOfTOC == 1):
                tempChapterDoc = tempChapterDoc + line
                chap = str(n)+".1 Introduction"
                if(chap in line):
                    masterList.append(tempChapterDoc)
                    tempChapterDoc = ""
                    n+=1

            else:
                if("Acronyms" in line):
                    endOfTOC = 1
    return masterList

#Vectorize content and return vectorized database
def vectorize_content(temp_list):
    id_list = []
    for i in range(len(temp_list)):
        id_list.append("Chapter"+str(i))

    client = chromadb.Client()
    collection = client.create_collection("temp_collection")
    collection.add(
        documents= temp_list,
        ids = id_list
    )
    return collection

text_contents = getTextbookContent()
temp_collection = vectorize_content(text_contents)
results = temp_collection.query(
    #USER INPUT HERE
    query_texts=["What is ICMP?"],
    n_results=3
)

print(results.get('ids'))
print(results.get('distances'))