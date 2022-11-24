from bs4 import BeautifulSoup
from unidecode import unidecode

def get_registro_solicitud (html:str):
    html=html.replace("<br>", "")
    soup = BeautifulSoup(html,"html.parser")
    rows=soup.find_all('tr')
    values=rows[1]
    columns=values.find_all("td")
    iterator = map(lambda data:unidecode(data.string), columns)
    return list(iterator)

if __name__ == '__main__':
    html=''
    list=get_registro_solicitud(html)
    print(list)
    for value  in list:
        print(type(value))
        print(str(value))