from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def waitForElement(key, identifier: str, driver):
    try:
        result = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((key, identifier))
        )
        return result
    except Exception as e:
        print(f"Error: {e}")
        result = None  # o manejar el error de otra forma