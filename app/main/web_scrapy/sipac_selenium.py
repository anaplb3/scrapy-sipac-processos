from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
from ..bd.repository import environment_config
from app.main.model.aid_enum import Aid


def find_tipo_processo(tipo_processo):
    if tipo_processo == "auxilio_emergencial":
        return "EMERGENCIAL"
    elif tipo_processo == "auxilio_alimentacao_residencia":
        return "RESIDÊNCIA"
    elif tipo_processo == "auxilio_alimentacao":
        return "ALIMENTAÇÃO"
    elif tipo_processo == "auxilio_moradia":
        return "MORADIA"
    elif tipo_processo == "auxilio_residencia_rumf":
        return "RUMF"
    elif tipo_processo == "auxilio_residencia_rufet":
        return "RUFET"
    elif tipo_processo == "auxilio_residentes":
        return "RESIDENTES"
    elif tipo_processo == "auxilio_emergencial_complementar":
        return "ALIMENTAÇÃO COMPLEMENTAR"
    elif tipo_processo == "auxilio_creche":
        return "PRÉ-ESCOLAR"
    elif tipo_processo == "(FAIXA I)":
        return Aid.AUXILIO_TRANSPORTE_FAIXA_I.value


def setting_selenium():
    if environment_config()["debug"]:
        return webdriver.Chrome("C:\chromedriver")
    else:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        
        driver = webdriver.Chrome(executable_path=os.environ.get(
            "CHROMEDRIVER_PATH"), chrome_options=chrome_options)
        return driver


def open(tipo_processo, campus, mes):
    driver = setting_selenium()
    auxilio = find_tipo_processo(tipo_processo)

    print("auxilio = {} | campus = {} | mes = {}".format(
        auxilio, campus, mes))
    url = "https://sipac.ufpb.br/public/jsp/processos/consulta_processo.jsf"
    nome_interessado = "prape"

    driver.get(url)
    button = driver.find_element_by_xpath(
        "/html/body/div/div/div[2]/form/table/tbody/tr[2]/td[1]/input")
    button.click()
    time.sleep(1)

    driver.find_element_by_xpath(
        "/html/body/div/div/div[2]/form/table/tbody/tr[2]/td[2]/input").send_keys(nome_interessado)
    driver.find_element_by_xpath(
        "/html/body/div/div/div[2]/form/table/tfoot/tr/td/input").click()

    time.sleep(1)

    table = driver.find_element(By.CLASS_NAME, "listagem")
    index = 1
    achou = True
    while(achou):
        if index >= 10:
            print("index maior que 10. parando de buscar.")
            return None
        time.sleep(1)
        table = driver.find_element(By.CLASS_NAME, "listagem")
        rows = table.find_elements(By.TAG_NAME, "tr")
        for row in rows:
            assunto = row.text
            if find_auxilio(assunto, auxilio, campus, mes):
                print("auxílio encontrado = {}".format(assunto))
                achou = False
                row.find_element(By.TAG_NAME, "img").click()
                driver.close
                return driver.page_source, driver.current_url
        index += 1
        driver.find_element_by_name(
            "documentoForm:j_id_jsp_1859633818_26").click()


def find_auxilio(assunto, auxilio, campus, mes):
    if "FOLHA DE PAGAMENTO" in assunto:
        return False
    is_auxilio = check_aid_in_text(auxilio, assunto)
    '''if auxilio == "ALIMENTAÇÃO":
        is_auxilio = (auxilio in assunto) and (
            "EMERGENCIAL" not in assunto) and ("RESIDENTES" not in assunto)'''

    if auxilio == "PRÉ-ESCOLAR":
        is_campus = True
    else:
        is_campus = find_campus(assunto, campus)

    is_mes = mes in assunto
    return is_auxilio and is_campus and is_mes


def find_campus(text, campus):
    auxilio_list = text.split(" ")
    for word in auxilio_list:
        if word == campus:
            return True
    return False

def check_transport_aid_range(assunto, range):
    if (Aid.AUXILIO_TRANSPORTE.value in assunto) and (range in assunto):
        return True

def check_food_aid_special_case(aid, text):
    return (aid in text) and (
            "EMERGENCIAL" not in text) and ("RESIDENTES" not in text)

def check_aid_in_text(aid, text):
    if (is_transport_aid(aid)):
        return check_transport_aid_range(text, aid)
    elif (is_food_aid(aid)):
        return check_food_aid_special_case(aid, text)
    else:
        return aid in text

def is_transport_aid(aid):
    return (aid == Aid.AUXILIO_TRANSPORTE_FAIXA_I.value) or (aid == Aid.AUXILIO_TRANSPORTE_FAIXA_II.value) or (aid == Aid.AUXILIO_TRANSPORTE_FAIXA_III.value)

def is_food_aid(aid):
    return aid == Aid.AUXILIO_ALIMENTACAO.value