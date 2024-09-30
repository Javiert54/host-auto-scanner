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
import subprocess
load_dotenv()
# Inicializa el cliente Docker

client = docker.from_env()

ACTIVATION_CODE = os.getenv('ACTIVATION_CODE')
USERNAME = os.getenv('USERNAME')
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


def buildDockerfileImage(image_name:str, client=client):
    try:
        client.images.get(image_name)
        print(f"La imagen '{image_name}' ya existe.")
    except docker.errors.ImageNotFound:
        print(f"La imagen '{image_name}' no existe. Construyendo la imagen...")
        # Construir la imagen
        image, logs = client.images.build(path=".", tag=image_name)
        for log in logs:
            print(log.get('stream', ''))

def removeContainer(containerName:str, client=client):
    try:
        container = client.containers.get(containerName)
        # Detener el contenedor (opcional, si está en ejecución)
        container.stop()
        # Eliminar el contenedor
        container.remove()
    except Exception as e:
        print(f'ERROR. o se ha podido borrar el contenedor:\n  {e}')

def runContainer(imageName:str, containerName:str, client=client):
    container = client.containers.run(
        imageName,  # Imagen del contenedor
        detach=True,  # Ejecuta el contenedor en segundo plano
        ports={'8834/tcp': 8834},  # Mapea el puerto 80 del contenedor al puerto 8080 del host
        name = containerName
    )
    while container.status != 'running':
        container.reload()
        time.sleep(1)
    return container

def waitForElement(key, identifier: str):
    try:
        result = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((key, identifier))
        )
        return result
    except Exception as e:
        print(f"Error: {e}")
        result = None  # o manejar el error de otra forma
            
def runComposeUp(ymlFilePath:str=".",  build:bool=False, client=client):
    """
    Ejecuta los servicios definidos en un archivo YAML de Docker Compose.
    Args:
        ymlFilePath (str): Ruta completa al archivo YAML.
        build (bool, optional): Si es True, se construyen las imágenes antes de iniciar los contenedores. Defaults to False.
    """

    command = ["docker-compose", "-f", ymlFilePath, "up", "-d"]
    if build:
        command.append("--build")
    try:
        output = subprocess.run(command, check=True, capture_output=True)
        print(f"Servicios iniciados desde {ymlFilePath}")
        print(output.stdout.decode('utf-8'))
    except Exception as e:
        print(f"Error al iniciar los servicios: {str(e)}")
    


if  __name__ == "__main__":


    # print(client.containers.list())
    carpeta_script = os.path.dirname(os.path.abspath(__file__)) #Obtenemos la ruta de mi script
    # buildDockerfileImage('nessus')
    removeContainer("nessusContainer")
    
    runComposeUp(os.path.join(carpeta_script, "docker-compose.yml"), build=True)
    # container = runContainer("nessus", "nessusContainer")
    # Ejecuta el contenedor de nessus

    time.sleep(3)
    driver.get(URL)
    time.sleep(1)
    button = waitForElement(By.CSS_SELECTOR, '[data-name="continue"]')
    while button is None:
        button = waitForElement(By.CSS_SELECTOR, '[data-name="continue"]')
    time.sleep(1)
    button[0].click()
    try:
        waitForElement(By.CSS_SELECTOR, '[data-type="essentials"]')[0].click()
        waitForElement(By.XPATH, "//button[text()='Continue']")[0].click()
        waitForElement(By.XPATH, "//button[text()='Skip']")[0].click()
        waitForElement(By.NAME, 'code')[0].send_keys(ACTIVATION_CODE)
        waitForElement(By.CSS_SELECTOR, '[data-name="btn-continue"]')[2].click()
        waitForElement(By.CSS_SELECTOR, '[data-name="continue"]')[0].click()
    except Exception:
        waitForElement(By.CSS_SELECTOR, '[data-value="ESSENTIALS"]')[0].click()    
        waitForElement(By.CLASS_NAME, 'secondary')[0].click()
        waitForElement(By.CSS_SELECTOR, '[data-field="activation"]')[0].send_keys(ACTIVATION_CODE)
        secondary = waitForElement(By.CSS_SELECTOR, '[data-name="continue"]')[0].click()



    waitForElement(By.CSS_SELECTOR, '[data-field="username"]')[0].send_keys(USERNAME)
    waitForElement(By.CSS_SELECTOR, '[data-field="password"]')[0].send_keys(USERPASSWORD)   
    waitForElement(By.CLASS_NAME, 'secondary')[0].click()
    
    print("Usuario Registrado.\n")
while True:
    pass

