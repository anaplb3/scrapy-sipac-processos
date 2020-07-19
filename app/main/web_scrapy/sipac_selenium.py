from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
from ..bd.repository import environment_config


def find_tipo_processo(tipo_processo, campus):
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


def setting_selenium():
    if environment_config()["debug"]:
        return webdriver.Chrome("C:\chromedriver")
    else:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(executable_path=os.environ.get(
            "CHROMEDRIVER_PATH"), chrome_options=chrome_options)
        return driver


def open(tipo_processo, campus, mes):
    driver = setting_selenium()
    auxilio = find_tipo_processo(tipo_processo, campus)

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
    is_auxilio = auxilio in assunto
    if auxilio == "ALIMENTAÇÃO":
        is_auxilio = (auxilio in assunto) and (
            "EMERGENCIAL" not in assunto) and ("RESIDENTES" not in assunto)
    is_campus = find_campus(assunto, campus)
    is_mes = mes in assunto
    return is_auxilio and is_campus and is_mes


def find_campus(text, campus):
    auxilio_list = text.split(" ")
    for word in auxilio_list:
        if word == campus:
            return True
    return False
