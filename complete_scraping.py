from autoselenium import Firefox
from bs4 import BeautifulSoup
import time

from utils import get_complete_dataframe

if __name__ == "__main__":

    with open('./inputs/websites.txt','r') as inf:
        extra_websites = eval(inf.read())

    for name, url in extra_websites.items():

        # Acceso a la web correspondiente
        driver = Firefox(headless=True)
        # driver = Firefox()
        driver.get(url)
        driver.maximize_window()
        time.sleep(3)

        # Recuperamos el código fuente del body
        body_web = driver.execute_script("return document.body")
        source_web = body_web.get_attribute('innerHTML')

        # Obtenemos la sopa
        soup_web = BeautifulSoup(source_web, 'lxml')
        
        # Guardamos los divs y sus características en un archivo csv
        df_web = get_complete_dataframe(soup_web.find_all("div"), driver, name)
        if df_web is not None:
            df_web.to_csv("./dataframes/df_" + name + ".csv", header=True)

        # Cerramos el navegador
        time.sleep(2)
        driver.close()