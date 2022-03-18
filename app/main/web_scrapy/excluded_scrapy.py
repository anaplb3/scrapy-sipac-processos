from bs4 import BeautifulSoup
from app.main.web_scrapy.sipac_selenium import open
from selenium import webdriver
from app.main.model.model import Excluded


def get_excluded_page_source(tipo_auxilio, campus, mes):
    resultados_selenium = open(tipo_auxilio, campus, mes)

    driver = webdriver.Chrome("C:\chromedriver") 
    driver.get(resultados_selenium[1])

    try:
        driver.find_element_by_xpath(
            "/html/body/div/div/div[2]/form/table/tbody/tr[3]/td/table/tbody/tr[13]/td/table/tbody/tr/td[3]/a/img"
        ).click()

        driver.close
        return driver.page_source
    except Exception:
        return None
 

def get_table_data_with_excluded(page_source):
    ex_soup = BeautifulSoup(page_source, 'html.parser')

    body = ex_soup.body

    tables = body.select('#corpo > table > tbody > tr:nth-child(3) > td > div.conteudo > table:nth-child(10)')
    table_imp = tables[0]
    return table_imp.find_all('tr')

def create_excluded_model(excluded_tr):
    excluded_list = []
    
    for excluded in excluded_tr:
        excluded_td = excluded.find_all('td')
        temp_array_for_data = []

        for index, value in enumerate(excluded_td):
            
            # Getting registration
            if (index == 2):
                temp_array_for_data.append(value.p.text)
            # Getting reason to be excluded
            elif (index == 5):
                temp_array_for_data.append(value.p.text)

        excluded_list.append(Excluded(temp_array_for_data[0], temp_array_for_data[1]))        

    return excluded_list

def get_excluded_list(tipo_auxilio, campus, mes):
    page_source = get_excluded_page_source(tipo_auxilio, campus, mes)
    if page_source is None:
        []
    else:
        excluded_tr = get_table_data_with_excluded(page_source)
        return create_excluded_model(excluded_tr)
