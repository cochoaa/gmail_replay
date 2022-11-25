from bs4 import BeautifulSoup
from unidecode import unidecode

def get_registro_solicitud (html:str):
    html=html.replace("<br>", "")
    soup = BeautifulSoup(html,"html.parser")
    rows=soup.find_all('tr')
    values=rows[1]
    column_tags=values.find_all("td")
    iterator = map(lambda  data: ('' if data.string==None else unidecode(data.string)), column_tags)
    return list(iterator)

if __name__ == '__main__':
    html=''
    list=get_registro_solicitud(html)
    print(list)
    for value  in list:
        print(type(value))
        print(str(value))