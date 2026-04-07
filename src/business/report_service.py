from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import os


class ReportService:
    def __init__(self):
        self.url_onnet = "https://oncoprod.service-now.com/now/nav/ui/classic/params/target/sn_customerservice_case_list.do%3Fsysparm_nostack%3Dtrue%26sysparm_query%3DstateNOT%2520IN6%252C3%252C7%255Eassignment_groupSTARTSWITHGMR_NOC_PROD%255Esys_created_on%253Ejavascript%3Ags.dateGenerate(%25272024-10-15%2527%252C%252700%3A00%3A01%2527)%255Eshort_descriptionNOT%2520LIKEAlert%2520Integration%26sysparm_first_row%3D1%26sysparm_view%3Dcase"

    def descargar_reporte_selenium(self):
        # 1. Configurar opciones de Chrome
        chrome_options = Options()
        # Esto es para que el navegador NO se cierre al terminar el script
        chrome_options.add_experimental_option("detach", True)

        # 2. Inicializar el Driver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)

        try:
            # 3. Ir a la página
            driver.get(self.url_onnet)

            # --- INTERVENCIÓN HUMANA ---
            print("Esperando a que Manuel inicie sesión...")
            # Aquí el script se detiene hasta que tú hagas el login en la ventana que se abrió
            # y presiones Enter en la consola de Python/VS Code.
            input("CUANDO HAYAS LOGUEADO Y VEAS LA LISTA, PRESIONA ENTER AQUÍ...")

            # 4. Forzar la descarga en formato Excel
            # Agregamos el parámetro EXCEL a la URL para que ServiceNow dispare la descarga
            url_descarga = self.url_onnet.replace(
                "sn_customerservice_case_list.do", "sn_customerservice_case_list.do?EXCEL")

            print("Iniciando descarga...")
            driver.get(url_exportar)

            # Esperamos unos segundos para que el archivo baje
            time.sleep(10)
            print("✅ El archivo debería estar en tu carpeta de Descargas.")

        except Exception as e:
            print(f"Ocurrió un error: {e}")
        finally:
            # Si quieres que se cierre solo, quita el comentario de abajo
            # driver.quit()
            pass
