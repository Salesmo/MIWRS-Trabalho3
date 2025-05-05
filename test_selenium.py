# selenium_scraper.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

def get_flight_data_selenium():
    # Caminho do chromedriver
    driver = webdriver.Chrome()

    # Acessa uma rota pública de tráfego (exemplo: Aeroporto de Congonhas)
    driver.get("https://www.flightradar24.com/data/airports/cgh/departures")

    time.sleep(5)  # Espera o carregamento do conteúdo dinâmico

    dados = []
    linhas = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")

    for linha in linhas[:5]:  # Limita a 5 voos por exemplo
        colunas = linha.find_elements(By.TAG_NAME, "td")
        if len(colunas) >= 6:
            voo = {
                "horário": colunas[0].text,
                "destino": colunas[1].text,
                "companhia": colunas[3].text,
                "número do voo": colunas[4].text,
                "status": colunas[5].text,
            }
            dados.append(voo)

    driver.quit()
    return dados

print(get_flight_data_selenium())