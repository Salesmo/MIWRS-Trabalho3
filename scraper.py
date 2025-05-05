from selenium import webdriver as gs
import chromedriver_autoinstaller
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import json
from collections import defaultdict

print("Programa iniciado.")
print("Instalando driver do Google...")
chromedriver_autoinstaller.install()
print("Driver do Google instalado com sucesso!")

def get_info(cod):
    driver = gs.Chrome()
    print('Google aberto')
    url = f'https://www.flightradar24.com/data/airports/{cod}/arrivals'
    driver.get(url)
    print('Página pesquisada')
    time.sleep(5)
    driver.implicitly_wait(10)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'text-center'))
    )
    print('Página carregada')

    button = driver.find_element(By.CLASS_NAME, 'btn-flights-load')
    for i in range(3):
        try:
            driver.execute_script("arguments[0].scrollIntoView(true);", button)
            time.sleep(1)
            driver.execute_script("arguments[0].click();", button)
            time.sleep(2)
        except Exception as e:
            print("Erro ao clicar:", e)

    agrupados = defaultdict(list)

    voos = driver.find_elements(By.CSS_SELECTOR, 'tr.hidden-xs.hidden-sm.ng-scope')
    for i, voo in enumerate(voos[:100]):
        print("i:", i)
        data_attr = voo.get_attribute("data-date")
        if not data_attr:
            continue  

        partes = data_attr.replace(",", "").split()
        week_day = partes[0]
        month = partes[1]
        day = int(partes[2])
        chave_data = f"{week_day}, {month} {day}"

        tds = voo.find_elements(By.TAG_NAME, "td")
        if len(tds) < 7:
            continue

        horario = tds[0].text.strip()
        codigo = tds[1].text.strip()
        origem = tds[2].find_element(By.CLASS_NAME, "hide-mobile-only").text.strip()
        aeroporto = tds[2].find_element(By.TAG_NAME, "a").text.strip().replace("(", "").replace(")", "")
        companhia = tds[3].text.strip()

        try:
            modelo = tds[4].find_element(By.TAG_NAME, "span").text.strip()
        except:
            modelo = "-"
        try:
            nome = tds[4].find_element(By.TAG_NAME, "a").text.strip().replace("(", "").replace(")", "")
        except:
            nome = "-"

        status_completo = tds[6].text.strip()
        status_split = re.split(r'(\d{2}:\d{2})', status_completo)
        status = status_split[0].strip()
        hora_status = status_split[1] if len(status_split) > 1 else ""

        agrupados[chave_data].append({
            "time": horario,
            "flight": codigo,
            "from": origem,
            "airport": aeroporto,
            "airline": companhia,
            "aircraft": modelo,
            "aircraft-name": nome,
            "status": status,
            "time-status": hora_status
        })

    arrivals = []
    for chave_data, voos in agrupados.items():
        week_day, month_day = chave_data.split(', ')
        month, day = month_day.split()
        arrivals.append({
            "date": {
                "month": month,
                "week-day": week_day,
                "day": int(day)
            },
            "info": voos
        })

    voos_formatados = {
        "Arrivals": arrivals
    }

    with open('voos.json', 'w', encoding='utf-8') as f:
        json.dump(voos_formatados, f, ensure_ascii=False, indent=4)
    print("Arquivo 'voos.json' criado com sucesso!")
    driver.close()
    return json.dumps(voos_formatados, ensure_ascii=False, indent=4)
