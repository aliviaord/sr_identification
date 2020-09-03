from pymongo import MongoClient
from bs4 import BeautifulSoup
from lxml import html, etree
import pandas as pd

if __name__ == "__main__":

    # Conectamos con la BBDD de MongoDB Atlas
    client = MongoClient('mongodb+srv://test:test@cluster0.tdrau.mongodb.net/hotels_db?retryWrites=true&w=majority')
    db = client.get_database('hotels_db')
    records = db.hotels_records


    ########################### BOOKING ###########################

    # Abrimos el fichero que contiene el html
    with open("./webpages/web_booking.html", mode="r", encoding="utf8") as booking_file:
        booking_html = booking_file.read()
    booking_tree = html.fromstring(booking_html)

    # Abrimos el fichero que contiene los xpaths de los clasificados como
    # resultados de búsqueda
    booking_df_res = pd.read_csv('./webpages/res_booking.csv', index_col=0)

    print("Hotels in DB before Booking inserts: " + str(records.count_documents({})))

    # Para cada fila del fichero de resultados de búsqueda
    for index, row in booking_df_res.iterrows():
        # Seleccionamos del html el elemento con el xpath que indique la fila
        matching_div = booking_tree.xpath(row['xpath'])[0]

        try:
            # Obtenemos las características necesarias del hotel
            name = matching_div.cssselect('span.sr-hotel__name')[0].text_content().strip()

            location = matching_div.cssselect('a.bui-link')[0].text_content().replace('Mostrar en el mapa', '').strip()

            nights = matching_div.cssselect('div.bui-price-display__label.prco-inline-block-maker-helper')[0].text_content().split(',')[0]
            nights = ''.join([i for i in nights if i.isdigit()]).strip()

            price = matching_div.cssselect('div.bui-price-display__value.prco-inline-block-maker-helper')[0].text_content()
            price = ''.join([i for i in price if i.isdigit()]).strip()

            image = matching_div.cssselect('img.hotel_image')[0].xpath('@src')[0].strip()

            # Creamos un objeto con las características del nuevo hotel
            new_hotel = {
                'name': name,
                'location': location,
                'nights': int(nights),
                'price': int(price),
                'image': image
            }

            # Insertamos el hotel en la BBDD
            records.insert_one(new_hotel)
        
        except Exception as e:
            print(e)

    print("Hotels in DB after Booking inserts: " + str(records.count_documents({})))
    print("----------------------------------------------")

    ########################### EXPEDIA ###########################´

    # Abrimos el fichero que contiene el html
    with open("./webpages/web_expedia.html", mode="r", encoding="utf8") as expedia_file:
        expedia_html = expedia_file.read()
    expedia_tree = html.fromstring(expedia_html)

    # Abrimos el fichero que contiene los xpaths de los clasificados como
    # resultados de búsqueda
    expedia_df_res = pd.read_csv('./webpages/res_expedia.csv', index_col=0)

    print("Hotels in DB before Expedia inserts: " + str(records.count_documents({})))

    # Para cada fila del fichero de resultados de búsqueda
    for index, row in expedia_df_res.iterrows():
        matching_div = expedia_tree.xpath(row['xpath'])[0]

        try:
            # Obtenemos las características necesarias del hotel
            name = matching_div.cssselect('h3')[0].text_content().strip()

            location = matching_div.cssselect('div.overflow-wrap.uitk-spacing.uitk-spacing-padding-blockend-two.uitk-text-secondary-theme')[0].text_content().strip()

            nights = matching_div.cssselect('div.pwa-theme--grey-700.uitk-type-100.uitk-type-regular')[0].text_content()
            nights = ''.join([i for i in nights if i.isdigit()]).strip()

            price = matching_div.cssselect('span.uitk-cell.loyalty-display-price.all-cell-shrink')[1].text_content()
            price = ''.join([i for i in price if i.isdigit()]).strip()

            image = ""

            try:
                image = matching_div.cssselect('img.uitk-image-media')[1].xpath('@src')[0].strip()
            except Exception as e:
                print(e)
            
            # Creamos un objeto con las características del nuevo hotel
            new_hotel = {
                'name': name,
                'location': location,
                'nights': int(nights),
                'price': int(price),
                'image': image
            }

            # Insertamos el hotel en la BBDD
            records.insert_one(new_hotel)
        
        except Exception as e:
            print(e)

    print("Hotels in DB after Expedia inserts: " + str(records.count_documents({})))
    print("----------------------------------------------")

    ########################### TRIVAGO ###########################

    # Abrimos el fichero que contiene el html
    with open("./webpages/web_trivago.html", mode="r", encoding="utf8") as trivago_file:
        trivago_html = trivago_file.read()
    trivago_tree = html.fromstring(trivago_html)

    # Abrimos el fichero que contiene los xpaths de los clasificados como
    # resultados de búsqueda
    trivago_df_res = pd.read_csv('./webpages/res_trivago.csv', index_col=0)

    print("Hotels in DB before Trivago inserts: " + str(records.count_documents({})))

    # Para cada fila del fichero de resultados de búsqueda
    for index, row in trivago_df_res.iterrows():
        matching_div = trivago_tree.xpath(row['xpath'])[0]

        try:
            # Obtenemos las características necesarias del hotel
            name = matching_div.cssselect('span.item-link.name__copytext.name__copytext--small')[0].text_content().strip()

            location = matching_div.cssselect('p.details-paragraph.details-paragraph--location.location-details')[0].text_content().strip()

            nights_and_price = matching_div.xpath(".//em[@data-qa='price-per-stay']")[0].text_content()

            nights = nights_and_price.split('noches')[0]
            nights = ''.join([i for i in nights if i.isdigit()]).strip()

            price = nights_and_price.split('noches')[1]
            price = ''.join([i for i in price if i.isdigit()]).strip()

            image = matching_div.cssselect('div.lazy-image__image-wrapper')[0].xpath('./meta[3]')[0].attrib['content']

            # Creamos un objeto con las características del nuevo hotel
            new_hotel = {
                'name': name,
                'location': location,
                'nights': int(nights),
                'price': int(price),
                'image': image
            }

            # Insertamos el hotel en la BBDD
            records.insert_one(new_hotel)
        
        except Exception as e:
            print(e)

    print("Hotels in DB after Trivago inserts: " + str(records.count_documents({})))
    print("----------------------------------------------")