# coding: utf-8
import requests
from bs4 import BeautifulSoup
import re
from lxml import etree
def ahhhhhhh(url,admin,password):
  session = requests.Session()
  response = session.get("http://180.209.64.18/cxcy/index.aspx")
  html = response.content
  soup = BeautifulSoup(html, "html.parser")
  viewState, eventValidation = soup.find(id='__VIEWSTATE')['value'], soup.find(id='__EVENTVALIDATION')['value']
  data = {
  '__VIEWSTATE': viewState,
  '__EVENTVALIDATION': eventValidation,
  'UserId': 'Q14010318',
  'Pwd': 'Q14010318',
  'LoginButton.x': '32',
  'LoginButton.y': '8'
  }
  header = {
  'Referer':'http://180.209.64.18/cxcy/Student/SelItem.aspx?sid=bQV3ZNrjspQ..&screen=tB40zpmAFyI..&gn=buYkhTftTnI..&iz=8dsh2TtxEtk..&gtype=WmcuQlgQCCo..',
  'Upgrade-Insecure-Requests':'1'
  }
  loginResponse = session.post('http://180.209.64.18/cxcy/index.aspx', data=data)
  href = re.findall(r"href='(.*)'", loginResponse.content.decode('gbk')[-300:])[0]
  main = session.get("http://180.209.64.18/cxcy/" + href)
  main.encoding="gbk"
  html = main.content.decode('gbk')
  soup = BeautifulSoup(html, "html.parser")
  #print(soup)
  main = session.get('http://180.209.64.18/cxcy/Student/Item.aspx?sid=bQV3ZNrjspQ..&screen=tB40zpmAFyI..',headers=header)
  main.encoding="gbk"
  html = main.content.decode('gbk')
  soup = BeautifulSoup(html, "html.parser")
  links = soup.find_all("input")
  listlist=[]
  for link in links:
    for string in link.parent.stripped_strings:
      listlist.append(string)
  biglist={}
  list2=[]
  for i in range(len(listlist)):
    if '：'.decode('utf8') in listlist[i]:
      if len(list2)!=0 and '：'.decode('utf8') in list2[0]:
        biglist[list2[0]]=list2[1:]
      list2=[]
      list2.append(listlist[i])
    else:
      list2.append(listlist[i])
  return biglist
# print(ahhhhhhh(1,1,1))
