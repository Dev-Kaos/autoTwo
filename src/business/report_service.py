import time
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains


class ReportService:
    def __init__(self, config_service):
        self.config_service = config_service
        # URL base de la lista de casos en ServiceNow
        self.url_servicenow = "https://oncoprod.service-now.com/now/nav/ui/classic/params/target/sn_customerservice_case_list.do"

    def descargar_automaticamente(self, user_corp, pass_sso):
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-extensions")

        # Inicialización del driver
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
                print("Aviso: Link de SSO no detectado o ya logueado.")

            # --- 2. PASO: SELECTOR DE CORREO ON NET ---
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
                print("Login completado exitosamente.")
            except:
                print("Aviso: Pantalla de 'Mantener sesión' no apareció.")

            # --- 6. NAVEGACIÓN CON FILTROS ---
            # Usamos la URL con los parámetros sysparm_query para filtrar por tu grupo GMR_NOC_PROD
            url_con_filtros = (
                "https://oncoprod.service-now.com/now/nav/ui/classic/params/target/"
                "sn_customerservice_case_list.do?sysparm_query=stateNOT%20IN6%2C3%2C7"
                "%5Eassignment_groupSTARTSWITHGMR_NOC_PROD"
                "%5Esys_created_on%3Ejavascript%3Ags.dateGenerate(%272024-10-15%27%2C%2700%3A00%3A01%27)"
                "%5Eshort_descriptionNOT%20LIKEAlert%20Integration"
            )
            print("Aplicando filtros de búsqueda...")
            driver.get(url_con_filtros)

            # Tiempo para que el ASUS A15 y la conexión procesen la consulta pesada
            time.sleep(10)

            # --- 7. EXPORTACIÓN (DENTRO DEL SHADOW DOM) ---
            try:
                print("Accediendo a la capa Shadow DOM de On Net Fibra...")
                driver.switch_to.default_content()

                # Localizamos el componente raíz de Polaris detectado en descargarKPI.py
                host_shadow = wait.until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, 'macroponent-f51912f4c700201072b211d4d8c26010')
                ))

                shadow_root = host_shadow.shadow_root
                iframe_interno = shadow_root.find_element(
                    By.CSS_SELECTOR, 'iframe[id="gsft_main"]')
                driver.switch_to.frame(iframe_interno)
                print("Foco establecido dentro de la tabla filtrada.")

                # Clic derecho en la cabecera 'Número' (name='number')
                th_numero = wait.until(EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, 'th[name="number"]')))
                ActionChains(driver).context_click(th_numero).perform()
                time.sleep(2)

                # Exportar > Excel usando los IDs internos que funcionan en tu empresa
                print("Seleccionando formato de exportación...")
                # ID para el menú 'Exportar'
                wait.until(EC.element_to_be_clickable(
                    (By.CSS_SELECTOR,
                     'div[item_id="d1ad2f010a0a0b3e005c8b7fbd7c4e28"]')
                )).click()

                # ID para la opción 'Excel (.xlsx)'
                wait.until(EC.element_to_be_clickable(
                    (By.CSS_SELECTOR,
                     'div[item_id="f13f0041473012003db6d7527c9a71f0"]')
                )).click()

                # --- 8. DIÁLOGO DE DESCARGA FINAL ---
                print("Esperando procesamiento del servidor...")
                # Esperamos al botón final del cuadro de diálogo
                btn_final = wait.until(
                    EC.element_to_be_clickable((By.ID, "download_button")))
                btn_final.click()
                print("¡Descarga iniciada exitosamente!")

                driver.switch_to.default_content()
                time.sleep(10)
                return True

            except Exception as e:
                print(f"Error en la fase de exportación: {e}")
                driver.save_screenshot("error_final_kcode.png")
                return False

        except Exception:
            print("--- ERROR CRÍTICO EN LA EJECUCIÓN ---")
            print(traceback.format_exc())
            return False
        finally:
            driver.quit()
