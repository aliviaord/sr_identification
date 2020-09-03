from autoselenium import Firefox
from bs4 import BeautifulSoup
import time

from utils import get_basic_dataframe

if __name__ == "__main__":

    websites = {
        "booking": "https://www.booking.com/searchresults.es.html?aid=1784973&label=affnetawin-index_pub-85386_site-kea05lyd9702l1pj0mspi_plc-_ts-_clkid-18120_1598363158_c8c9870de1ee166f0bb893ef0f29b75b_pname-VigLink+Content&sid=bd0f3e68b6951f44c80832c58e8a3d90&sb=1&sb_lp=1&src=index&src_elem=sb&error_url=https%3A%2F%2Fwww.booking.com%2Findex.es.html%3Faid%3D1784973%3Blabel%3Daffnetawin-index_pub-85386_site-kea05lyd9702l1pj0mspi_plc-_ts-_clkid-18120_1598363158_c8c9870de1ee166f0bb893ef0f29b75b_pname-VigLink%2520Content%3Bsid%3Dbd0f3e68b6951f44c80832c58e8a3d90%3Bsb_price_type%3Dtotal%26%3B&ss=A+Coru%C3%B1a%2C+Espa%C3%B1a&is_ski_area=&checkin_year=2020&checkin_month=10&checkin_monthday=5&checkout_year=2020&checkout_month=10&checkout_monthday=25&group_adults=2&group_children=0&no_rooms=1&b_h4u_keep_filters=&from_sf=1&ss_raw=a+coru%C3%B1a&ac_position=1&ac_langcode=es&ac_click_type=b&dest_id=1364&dest_type=region&place_id_lat=43.04738&place_id_lon=-8.635193&search_pageview_id=a54f60cbeb2d0019&search_selected=true&region_type=free_region&search_pageview_id=a54f60cbeb2d0019&ac_suggestion_list_length=5&ac_suggestion_theme_list_length=0",
        "expedia": "https://www.expedia.es/Hotel-Search?adults=2&d1=2020-10-05&d2=2020-10-25&destination=La%20Coru%C3%B1a%2C%20Galicia%2C%20Espa%C3%B1a&endDate=2020-10-25&latLong=43.371498%2C-8.39773&regionId=2028&rooms=1&semdtl=&sort=RECOMMENDED&startDate=2020-10-05&theme=&useRewards=false&userIntent",
        "trivago": "https://www.trivago.es/?aDateRange%5Barr%5D=2020-10-05&aDateRange%5Bdep%5D=2020-10-25&aPriceRange%5Bfrom%5D=0&aPriceRange%5Bto%5D=0&iRoomType=7&aRooms%5B0%5D%5Badults%5D=2&cpt2=315876%2F200&hasList=1&hasMap=1&bIsSeoPage=0&sortingId=1&slideoutsPageItemId=&iGeoDistanceLimit=20000&address=&addressGeoCode=&offset=0&ra=&overlayMode=",
        "tripadvisor": "https://www.tripadvisor.es/Search?q=a%20coru%C3%B1a&searchSessionId=BB39BB852442BFD4B6451637084EC8C61597766035333ssid&searchNearby=false&sid=0CEE7D56123622C19BC9C8430DB93AE31597766157684&blockRedirect=true&ssrc=h&rf=1",
        # Los enlaces de búsqueda de destinia caducan
        # "destinia": "https://online.destinia.com/online/hotels/search?date_unix=1598303661662323002&sortType=bestbuy",
        "atrapalo": "https://www.atrapalo.com/hoteles/results/eff079579421951a99693159233edf64/1:00:0:0:792eb/",
        # Logitravel bloquea el scraping por ser un robot
        # "logitravel": "https://www.logitravel.com/hotels/results/?type=CIU&code=9613208&check_in=05%2F10%2F2020&check_out=25%2F10%2F2020&rooms=30%2C30",
        "kayak": "https://www.kayak.es/hotels/La-Coruna,Comunidad-Autonoma-de-Galicia,Espana-c50507/2020-10-05/2020-10-25/2adults?sort=rank_a",
        "skyscanner": "https://www.skyscanner.es/hotels/search?entity_id=27543999&checkin=2020-10-05&checkout=2020-10-25&adults=2&rooms=1"
    }

    for name, url in websites.items():

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
        df_web = get_basic_dataframe(soup_web.find_all("div"), driver, name)
        if df_web is not None:
            df_web.to_csv("./dataframes/df_" + name + "_basic.csv", header=True)

        # Cerramos el navegador
        time.sleep(2)
        driver.close()