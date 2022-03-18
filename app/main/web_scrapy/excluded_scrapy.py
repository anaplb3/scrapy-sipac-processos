from bs4 import BeautifulSoup
from app.main.web_scrapy.sipac_selenium import open
from selenium import webdriver
from app.main.model.model import Excluded
from app.main.bd import repository
import psycopg2

class ExcludedScrappyService:

    def __init__(self):
        self.campus_id = None
        self.aid_id = None
        self.aid_month = None

    def set_campus_and_aid_id_and_month(self, tipo_auxilio, campus, mes):
        cursor = self.get_cursor()
        self.campus_id = repository.get_campus_id(cursor, campus)
        self.aid_id = repository.get_auxilio_id(
            cursor, self.campus_id, tipo_auxilio)
        self.aid_month = mes
    
    def get_cursor(self):
        cfg = repository.environment_config()
        connection = psycopg2.connect(
            cfg["database_url"], sslmode=cfg["sslmode"])
        return connection.cursor()

    def get_excluded_page_source(self, tipo_auxilio, campus, mes):
        self.set_campus_and_aid_id_and_month(tipo_auxilio, campus, mes)
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
    

    def get_table_data_with_excluded(self, page_source):
        ex_soup = BeautifulSoup(page_source, 'html.parser')

        body = ex_soup.body

        tables = body.select('#corpo > table > tbody > tr:nth-child(3) > td > div.conteudo > table:nth-child(10)')
        table_imp = tables[0]
        return table_imp.find_all('tr')

    def create_excluded_model(self, excluded_tr):
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

            # TO DO: substituir id's pelo nome
            excluded_list.append(Excluded(
                temp_array_for_data[0], 
                temp_array_for_data[1],
                self.campus_id,
                self.aid_id,
                self.aid_month))        

        return excluded_list

    def get_excluded_list(self, tipo_auxilio, campus, mes):
        page_source = self.get_excluded_page_source(tipo_auxilio, campus, mes)
        if page_source is None:
            []
        else:
            excluded_tr = self.get_table_data_with_excluded(page_source)
            return self.create_excluded_model(excluded_tr)
