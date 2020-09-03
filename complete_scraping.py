from autoselenium import Firefox
from bs4 import BeautifulSoup
import time

from utils import get_complete_dataframe

if __name__ == "__main__":

    extra_websites = {
        "tripadvisor": "https://www.tripadvisor.es/Search?q=a%20coru%C3%B1a&searchSessionId=BB39BB852442BFD4B6451637084EC8C61597766035333ssid&searchNearby=false&sid=0CEE7D56123622C19BC9C8430DB93AE31597766157684&blockRedirect=true&ssrc=h&rf=1",
        # Los enlaces de búsqueda de destinia caducan
        # "destinia": "https://online.destinia.com/online/hotels/search?date_unix=1598303661662323002&sortType=bestbuy",
        "atrapalo": "https://www.atrapalo.com/hoteles/results/eff079579421951a99693159233edf64/1:00:0:0:792eb/",
        # Logitravel bloquea el scraping por ser un robot
        # "logitravel": "https://www.logitravel.com/hotels/results/?type=CIU&code=9613208&check_in=05%2F10%2F2020&check_out=25%2F10%2F2020&rooms=30%2C30",
        "kayak": "https://www.kayak.es/hotels/La-Coruna,Comunidad-Autonoma-de-Galicia,Espana-c50507/2020-10-05/2020-10-25/2adults?sort=rank_a",
        "skyscanner": "https://www.skyscanner.es/hotels/search?entity_id=27543999&checkin=2020-10-05&checkout=2020-10-25&adults=2&rooms=1"
    }

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