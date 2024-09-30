import docker
import time
from selenium.webdriver.edge.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
from dotenv import load_dotenv
import dockerFunctions as dF
import webFunctions as wF
load_dotenv()
# Inicializa el cliente Docker

client = docker.from_env()

ACTIVATION_CODE = os.getenv('ACTIVATION_CODE')
USERNAME_NESSUS = os.getenv('USERNAME_NESSUS')
USERPASSWORD = os.getenv('PASSWORD')
browser_options = browser_options = webdriver.ChromeOptions()

#  --- PARA USAR SIN INTERFAZ GRÁFICA ---
# browser_options.add_argument("--headless")  # Ejecuta en modo headless
# browser_options.add_argument("--disable-gpu")  # Necesario para Windows
#  --- PARA USAR SIN INTERFAZ GRÁFICA ---
browser_options.add_argument('--ignore-certificate-errors')
browser_options.add_argument('--allow-insecure-localhost')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=browser_options, keep_alive=True)


# Abre la página web con el formulario
URL = 'https://127.0.0.1:8834'
            
if  __name__ == "__main__":

    carpeta_script = os.path.dirname(os.path.abspath(__file__)) #Obtenemos la ruta de mi script
    dF.removeContainer("nessusContainer")
    
    dF.runComposeUp(os.path.join(carpeta_script, "docker-compose.yml"), build=True)
    # Ejecuta el archivo de docker-compose

    time.sleep(3)
    driver.get(URL)
    time.sleep(1)
    button = wF.waitForElement(By.CSS_SELECTOR, '[data-name="continue"]', driver)
    while button is None:
        button = wF.waitForElement(By.CSS_SELECTOR, '[data-name="continue"]', driver)
    time.sleep(1)
    button[0].click()
    try:
        wF.waitForElement(By.CSS_SELECTOR, '[data-type="essentials"]', driver)[0].click()
        wF.waitForElement(By.XPATH, "//button[text()='Continue']", driver)[0].click()
        wF.waitForElement(By.XPATH, "//button[text()='Skip']", driver)[0].click()
        wF.waitForElement(By.NAME, 'code', driver)[0].send_keys(ACTIVATION_CODE)
        wF.waitForElement(By.CSS_SELECTOR, '[data-name="btn-continue"]', driver)[2].click()
        wF.waitForElement(By.CSS_SELECTOR, '[data-name="continue"]', driver)[0].click()
    except Exception as e:
        print("------- Error en el login -------")
        print("------- Error en el login -------")
        print("------- Error en el login -------")
        print(f"Error: {e}\n")
        wF.waitForElement(By.CSS_SELECTOR, '[data-value="ESSENTIALS"]', driver)[0].click()    
        wF.waitForElement(By.CLASS_NAME, 'secondary', driver)[0].click()
        wF.waitForElement(By.CSS_SELECTOR, '[data-field="activation"]', driver)[0].send_keys(ACTIVATION_CODE)
        secondary = wF.waitForElement(By.CSS_SELECTOR, '[data-name="continue"]', driver)[0].click()



    wF.waitForElement(By.CSS_SELECTOR, '[data-field="username"]', driver)[0].send_keys(USERNAME_NESSUS)
    wF.waitForElement(By.CSS_SELECTOR, '[data-field="password"]', driver)[0].send_keys(USERPASSWORD)   
    wF.waitForElement(By.CLASS_NAME, 'secondary', driver)[0].click()
    
    print("Usuario Registrado.\n")
while True:
    pass

