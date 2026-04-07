import time
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ReportService:
    def __init__(self, config_service):
        self.config_service = config_service
        self.url_servicenow = "https://oncoprod.service-now.com/now/nav/ui/classic/params/target/sn_customerservice_case_list.do"

    def descargar_automaticamente(self, user_corp, pass_sso):
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-extensions")

        # AQUÍ SE DEFINE EL DRIVER
        driver = webdriver.Chrome(options=chrome_options)
        wait = WebDriverWait(driver, 25)

        try:
            print(f"Navegando a: {self.url_servicenow}")
            driver.get(self.url_servicenow)

            # --- 1. PASO: CLIC EN LINK SSO ---
            try:
                sso_link = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "//a[contains(@href, 'login_locate_sso.do')]")))
                sso_link.click()
            except:
                print("Aviso: Link de SSO no detectado.")

            # --- 2. PASO: SELECTOR DE CORREO ---
            try:
                sso_input = wait.until(
                    EC.presence_of_element_located((By.ID, "sso_selector_id")))
                sso_input.send_keys(user_corp)
                driver.find_element(
                    By.XPATH, "//button[contains(text(), 'Enviar')]").click()
                time.sleep(3)
            except:
                print("Aviso: Selector de identidad saltado.")

            # --- 3. PASO: MICROSOFT EMAIL ---
            try:
                ms_email = wait.until(
                    EC.presence_of_element_located((By.ID, "i0116")))
                ms_email.clear()
                ms_email.send_keys(user_corp)
                driver.find_element(By.ID, "idSIButton9").click()
                time.sleep(2)
            except:
                print("Aviso: Pantalla de email de Microsoft no detectada.")

            # --- 4. PASO: MICROSOFT PASSWORD ---
            try:
                pass_field = wait.until(EC.any_of(
                    EC.presence_of_element_located((By.ID, "i0118")),
                    EC.presence_of_element_located((By.NAME, "passwd"))
                ))
                pass_field.send_keys(pass_sso)
                wait.until(EC.element_to_be_clickable(
                    (By.ID, "idSIButton9"))).click()
                time.sleep(3)
            except:
                print("Error: No se pudo ingresar la contraseña.")

            # --- 5. PASO: MANTENER SESIÓN ---
            try:
                check_box = wait.until(EC.element_to_be_clickable(
                    (By.ID, "KmsiCheckboxField")))
                if not check_box.is_selected():
                    check_box.click()
                driver.find_element(By.ID, "idSIButton9").click()
            except:
                print("Aviso: Pantalla de 'Mantener sesión' no apareció.")

            # --- 6. REDIRECCIÓN AL REPORTE GMR_NOC_PROD ---
            print("Redirigiendo a la vista final del reporte...")
            url_final = (
                "https://oncoprod.service-now.com/now/nav/ui/classic/params/target/"
                "sn_customerservice_case_list.do?sysparm_query=stateNOT%20IN6%2C3%2C7"
                "%5Eassignment_groupSTARTSWITHGMR_NOC_PROD%5Esys_created_on%3E"
                "javascript%3Ags.dateGenerate(%272024-10-15%27%2C%2700%3A00%3A01%27)"
                "%5Eshort_descriptionNOT%20LIKEAlert%20Integration"
                "&sysparm_first_row=1&sysparm_view=case"
            )

            # Usamos la variable 'driver' que definimos al inicio del método
            driver.get(url_final)
            time.sleep(7)

            # Entrar al frame para poder interactuar con la tabla después
            try:
                driver.switch_to.frame("gsft_main")
                print("Dentro del frame de datos.")
            except:
                pass

            return True

        except Exception:
            print("--- ERROR DETALLADO ---")
            print(traceback.format_exc())
            return False
        finally:
            # driver.quit() # Mantener abierto para validar
            pass
