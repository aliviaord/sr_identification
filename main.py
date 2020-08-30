from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver

from autoselenium import Firefox
from bs4 import BeautifulSoup
import time

from utils import get_complete_dataframe

if __name__ == "__main__":

    ########################### BOOKING ###########################

    # Acceso a la web correspondiente
    driver = Firefox(headless=True)
    # driver = Firefox()
    driver.get('https://www.booking.com/')
    driver.maximize_window()
    time.sleep(2)

    # Aceptar las cookies
    try:
        driver.find_element_by_id('onetrust-accept-btn-handler').click()
    except NoSuchElementException:
        driver.find_element_by_class_name('bui-button--wide').click()

    # Esperamos a que cargue la barra de búsqueda
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'ss')))

    # Rellenado del formulario
    destino = "A Coruña"
    fecha_inicio = 42
    fecha_fin = 62

    # Introducimos destino
    driver.find_element_by_id('ss').send_keys(destino)
    time.sleep(2)

    # Seleccionamos el primer destino del listado de sugeridos
    driver.find_elements_by_class_name('c-autocomplete__item')[0].click()

    # Pasamos una página del calendario
    driver.find_elements_by_class_name('bui-calendar__control--next')[0].click()

    # Seleccionamos día de ida y de vuelta
    driver.find_elements_by_class_name('bui-calendar__date')[fecha_inicio].click()
    driver.find_elements_by_class_name('bui-calendar__date')[fecha_fin].click()
    time.sleep(2)

    # Pulsamos el botón de búsqueda
    driver.find_element_by_class_name('sb-searchbox__button').click()
    time.sleep(5)

    # Recuperamos el código fuente del body
    body_booking = driver.execute_script("return document.body")
    source_booking = body_booking.get_attribute('innerHTML')

    # Obtenemos la sopa
    soup_booking = BeautifulSoup(source_booking, 'lxml')

    df_booking = get_complete_dataframe(soup_booking.find_all("div"), driver, "booking")
    if df_booking is not None:
        df_booking.to_csv("./dataframes/df_booking.csv", header=True)

    # Cerramos el navegador
    time.sleep(2)
    driver.close()


    ########################### EXPEDIA ###########################

    # Acceso a la web correspondiente
    driver = Firefox(headless=True)
    # driver = Firefox()
    driver.get('https://www.expedia.es/')
    driver.maximize_window()
    time.sleep(2)

    # Aceptar las cookies
    driver.find_element_by_css_selector('button.uitk-button.uitk-button-small.uitk-button-fullWidth.uitk-button-has-text.uitk-button-secondary').click()

    # Esperamos a que cargue la barra de búsqueda
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.wizardOverHeroImage.all-x-padding-six')))

    # Rellenado del formulario
    destino = "A Coruña"
    fecha_inicio = 36
    fecha_fin = 56

    # Introducimos destino
    driver.find_elements_by_class_name('uitk-faux-input')[0].click()
    driver.find_element_by_id('location-field-destination').send_keys(destino)
    time.sleep(2)

    # Seleccionamos el primer destino del listado de sugeridos
    driver.find_elements_by_css_selector('li.uitk-typeahead-result-item.has-subtext')[0].click()

    # Seleccionamos día de ida y de vuelta
    driver.find_elements_by_class_name('uitk-faux-input')[1].click()
    time.sleep(2)
    driver.find_elements_by_css_selector('td.uitk-new-date-picker-day-number')[fecha_inicio].click()
    driver.find_elements_by_css_selector('td.uitk-new-date-picker-day-number')[fecha_fin].click()
    driver.find_element_by_css_selector('button.uitk-button.uitk-button-small.uitk-button-has-text.uitk-button-primary.uitk-flex-item.uitk-flex-shrink-0.dialog-done').click()
    time.sleep(2)

    # Pulsamos el botón de búsqueda
    driver.find_elements_by_css_selector('button.uitk-button.uitk-button-large.uitk-button-fullWidth.uitk-button-has-text.uitk-button-primary')[1].click()
    time.sleep(5)

    # Recuperamos el código fuente del body
    body_expedia = driver.execute_script("return document.body")
    source_expedia = body_expedia.get_attribute('innerHTML')

    # Obtenemos la sopa
    soup_expedia = BeautifulSoup(source_expedia, 'lxml')

    df_expedia = get_complete_dataframe(soup_expedia.find_all("div"), driver, "expedia")
    if df_expedia is not None:
        df_expedia.to_csv("./dataframes/df_expedia.csv", header=True)

    # Cerramos el navegador
    time.sleep(2)
    driver.close()


    ########################### TRIVAGO ###########################

    # Acceso a la web correspondiente
    driver = Firefox(headless=True)
    # options = Options()
    # options.headless = True
    # driver = webdriver.Firefox(options=options)
    driver.get('https://www.trivago.es/')
    driver.maximize_window()
    time.sleep(2)

    # Aceptar las cookies
    driver.find_element_by_id('onetrust-accept-btn-handler').click()

    # Esperamos a que cargue la barra de búsqueda
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'form.js-dealform.dealform.dealform--no-detail')))

    # Rellenado del formulario
    destino = "A Coruña"
    fecha_inicio = 7
    fecha_fin = 27

    # Introducimos destino
    driver.find_element_by_id('querytext').send_keys(destino)
    time.sleep(2)

    # # Seleccionamos el primer destino del listado de sugeridos
    # driver.find_elements_by_css_selector('li.uitk-typeahead-result-item.has-subtext')[0].click()

    # Pasamos una página del calendario
    driver.find_elements_by_class_name('js-dealform-button-calendar')[0].click()
    driver.find_elements_by_class_name('cal-btn-next')[0].click()
    driver.find_elements_by_class_name('cal-btn-next')[0].click()
    time.sleep(2)

    # Seleccionamos día de ida y de vuelta
    driver.find_elements_by_css_selector('td.cal-day-wrap')[fecha_inicio].click()
    driver.find_elements_by_css_selector('td.cal-day-wrap')[fecha_fin].click()
    driver.find_element_by_class_name('btn--apply-config').click()
    time.sleep(2)

    # Pulsamos el botón de búsqueda
    driver.find_element_by_class_name('search-button').click()
    time.sleep(5)

    # Recuperamos el código fuente del body
    body_trivago = driver.execute_script("return document.body")
    source_trivago = body_trivago.get_attribute('innerHTML')

    # Obtenemos la sopa
    soup_trivago = BeautifulSoup(source_trivago, 'lxml')

    df_trivago = get_complete_dataframe(soup_trivago.find_all("div"), driver, "trivago")
    if df_trivago is not None:
        df_trivago.to_csv("./dataframes/df_trivago.csv", header=True, index=True)

    # Cerramos el navegador
    time.sleep(2)
    driver.close()