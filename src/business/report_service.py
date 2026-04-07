import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ReportService:
    def __init__(self):
        # URL de la lista de casos que me pasaste
        self.url_listado = "https://oncoprod.service-now.com/now/nav/ui/classic/params/target/sn_customerservice_case_list.do%3Fsysparm_nostack%3Dtrue%26sysparm_query%3DstateNOT%2520IN6%252C3%252C7%255Eassignment_groupSTARTSWITHGMR_NOC_PROD%255Esys_created_on%253Ejavascript%3Ags.dateGenerate(%25272024-10-15%2527%252C%252700%3A00%3A01%2527)%255Eshort_descriptionNOT%2520LIKEAlert%2520Integration%26sysparm_first_row%3D1%26sysparm_view%3Dcase"

    def descargar_automaticamente(self, usuario, clave):
        # --- CONFIGURACIÓN DE NAVEGADOR ---
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        # Opcional: Definir carpeta de descarga específica
        # prefs = {"download.default_directory": os.getcwd()}
        # chrome_options.add_experimental_option("prefs", prefs)

        driver = webdriver.Chrome(service=Service(
            ChromeDriverManager().install()), options=chrome_options)
        wait = WebDriverWait(driver, 30)  # Espera de hasta 30 segundos
        actions = ActionChains(driver)

        try:
            # 1. IR AL LOGIN
            driver.get(self.url_listado)

            # 2. PROCESO DE LOGIN (Ajustar IDs según el portal de On Net)
            print("Introduciendo credenciales...")
            # Estos IDs suelen cambiar con SSO, si falla, Selenium te avisará
            wait.until(EC.presence_of_element_located(
                (By.ID, "user_id"))).send_keys(usuario)
            driver.find_element(By.ID, "password").send_keys(clave)
            driver.find_element(By.ID, "sysverb_login").click()

            # 3. PAUSA PARA EL SSO / MFA
            print(
                "⚠️ Por favor, aprueba el acceso en tu celular (MFA) si es necesario...")
            # Esperamos a que la URL cambie o aparezca un elemento del listado
            wait.until(EC.presence_of_element_located((By.ID, "gsft_main")))
            print("✅ Sesión iniciada correctamente.")

            # 4. ENTRAR AL IFRAME (ServiceNow vive dentro de marcos)
            driver.switch_to.frame("gsft_main")
            print("Dentro del iframe principal.")

            # 5. CLIC DERECHO EN LA ETIQUETA (El ID que encontraste)
            # Reemplaza 'ID_DE_TU_ETIQUETA' por el ID real que hallaste
            id_columna = "hdr_sn_customerservice_case"
            etiqueta_objetivo = wait.until(
                EC.element_to_be_clickable((By.ID, id_columna)))

            actions.context_click(etiqueta_objetivo).perform()
            print("🖱️ Menú contextual abierto.")

            # 6. NAVEGAR POR EL MENÚ CONTEXTUAL
            # Buscamos la opción 'Exportar' (Export)
            opcion_exportar = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//*[contains(text(), 'Exportar')]"))
            )
            opcion_exportar.click()
            print("Seleccionado: Exportar.")

            # 7. SELECCIONAR EXCEL
            opcion_excel = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//*[contains(text(), 'Excel (.xlsx)')]"))
            )
            opcion_excel.click()
            print("Seleccionado: Formato Excel.")

            # 8. ESPERAR AL BOTÓN DE DESCARGA FINAL (Popup de ServiceNow)
            # Volvemos al contenido principal si el popup sale fuera del iframe
            # driver.switch_to.default_content()

            btn_descargar = wait.until(
                EC.element_to_be_clickable((By.ID, "download_button"))
            )
            btn_descargar.click()
            print("📥 ¡Descarga iniciada!")

            # Espera final para asegurar que el archivo baje
            time.sleep(10)
            return True

        except Exception as e:
            print(f"❌ Error durante la automatización: {e}")
            return False
