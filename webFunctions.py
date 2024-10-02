from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import dockerFunctions as dF
class host:
    def __init__(self, entityName:str, email:str, webSite:str, nextDateToScan:str):
        self.entityName = entityName
        self.email = email
        self.webSite = webSite
        self.nextDateToScan = nextDateToScan
        self.daysInterval = 0
        self.weeksInterval = 0
        self.monthsInterval = 0

    def set_interval(self, days:int=0, weeks:int=0, months:int=0):
        self.daysInterval = days
        self.weeksInterval = weeks
        self.monthsInterval = months
        
    def update_next_date_to_scan(self, days:int=None, weeks:int=None, months:int=None):
        # Usar los valores por defecto si no se proporcionan
        if days is None:
            days = self.daysInterval
        if weeks is None:
            weeks = self.weeksInterval
        if months is None:
            months = self.monthsInterval
        
        # Convertir la fecha actual a un objeto datetime
        current_date = datetime.strptime(self.nextDateToScan, "%Y-%m-%d")
        # Añadir días, semanas y meses
        new_date = current_date + timedelta(days=days, weeks=weeks) + relativedelta(months=months)
        # Actualizar la fecha
        self.nextDateToScan = new_date.strftime("%Y-%m-%d")



def waitForElement(key, identifier: str, driver):
    try:
        result = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((key, identifier))
        )
        return result
    except Exception as e:
        print(f"Error: {e}")
        result = None  # o manejar el error de otra forma



if __name__ == "__main__":
    dF.runComposeUp()
    while True:

        optionSelection = input("""Seleccione una opción:
                1. Borrar un host de la tabla hostsToScann
                2. Mostrar todos los hosts de la tabla hostsToScann
                3. Crear un nuevo host en la tabla hostsToScann""")
        if optionSelection.isdigit():
            if int(optionSelection) <1 or int(optionSelection) > 3:
                print("Opción no válida. Por favor, seleccione una opción entre 1 y 3.")
                continue
            else:
                optionSelection = int(optionSelection)
                if optionSelection == 1:
                    print("Seleccione el ID del host que desea borrar:")
                    hostID = input()
                    pass
                elif optionSelection == 2:
                    pass
                elif optionSelection == 3:
                    print("Ingrese los datos del host que desea agregar:")
                    entityName = input("Nombre del host: ")
                    email = input("Correo electrónico: ")
                    webSite = input("Sitio web: ")
                    nextDateToScan = input("Fecha de próxima escaneo: ")
                    host = host(entityName, email, webSite, nextDateToScan)
                    host.set_interval(days=0, weeks=0, months=0)
                    host.update_next_date_to_scan()
                    pass