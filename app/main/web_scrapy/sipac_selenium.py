from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
from ..bd.repository import environment_config


def find_tipo_processo(tipo_processo, campus):
    if tipo_processo == "auxilio_emergencial":
        return "PAGAMENTO DE BOLSISTAS DE AUXÍLIO EMERGENCIAL ALIMENTAÇÃO COVID19 - CAMPUS {} - PRAPE (R$ 250,00). REFERENTE: {}."
    elif tipo_processo == "auxilio_alimentacao_residencia":
        if campus == "IV":
            return "PAGAMENTO DE BOLSISTAS DE BOLSA AUXÍLIO-ALIMEN RES FDS CAMPUS {} PRAPE (R$ 410,00). REFERENTE: {}."
        else:
            return "PAGAMENTO DE BOLSISTAS DE BOLSA AUXÍLIO-ALIMEN RES FDS CAMPUS {} PRAPE (R$ 260,00). REFERENTE: {}."
    elif tipo_processo == "auxilio_alimentacao":
        return "PAGAMENTO DE BOLSISTAS DE BOLSA AUXÍLIO-ALIMENTAÇÃO CAMPUS {} PRAPE (R$ 240,00). REFERENTE: {}"
    elif tipo_processo == "auxilio_moradia":
        return "PAGAMENTO DE BOLSISTAS DE BOLSA AUXÍLIO-MORADIA CAMPUS {} PRAPE (R$ 570,00). REFERENTE: {}"


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
    res = find_tipo_processo(tipo_processo, campus)

    auxilio = res.format(campus, mes)
    print("auxilio = {}".format(auxilio))
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

    table = driver.find_element(By.CLASS_NAME, "listagem").text
    index = 1
    while (not auxilio in table):
        if index >= 10:
            return None
        driver.find_element_by_name(
            "documentoForm:j_id_jsp_1859633818_26").click()
        time.sleep(1)
        table = driver.find_element(By.CLASS_NAME, "listagem").text
        index += 1

    table = driver.find_element(By.CLASS_NAME, "listagem")
    rows = table.find_elements(By.TAG_NAME, "tr")
    for row in rows:
        if (auxilio in row.text):
            row.find_element(By.TAG_NAME, "img").click()
            driver.close
            return driver.page_source, driver.current_url
