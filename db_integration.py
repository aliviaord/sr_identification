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
    booking_df_res = pd.read_csv('./dataframes/res_booking.csv', index_col=0)

    print("Hotels in DB before Booking inserts: " + str(records.count_documents({})))

    # Para cada fila del fichero de resultados de búsqueda
    for index, row in booking_df_res.iterrows():
        # Seleccionamos del html el elemento con el xpath que indique la fila
        matching_div = booking_tree.xpath(row['xpath'])[0]

        try:
            # Obtenemos las características necesarias del hotel
            
            name = matching_div.xpath(".//div[2]/div[1]/div[1]/div[1]/h3/a/span[1]")[0].text_content().strip()

            location = matching_div.xpath(".//div[2]/div[1]/div[1]/div[2]/a")[0].text_content().replace('Mostrar en el mapa', '').strip()

            
            nights = matching_div.xpath(".//div[2]/div[3]/div/div/div/div/div[2]/div[1]/div[1]/div")[0].text_content().split(',')[0]
            nights = ''.join([i for i in nights if i.isdigit()]).strip()

            price = matching_div.xpath(".//div[2]/div[3]/div/div/div/div/div[2]/div[1]/div[2]/div/span")[0].text_content()
            price = ''.join([i for i in price if i.isdigit()]).strip()

            image = matching_div.xpath(".//div[1]/a/img")[0].xpath('@src')[0].strip()

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
    expedia_df_res = pd.read_csv('./dataframes/res_expedia.csv', index_col=0)

    print("Hotels in DB before Expedia inserts: " + str(records.count_documents({})))

    # Para cada fila del fichero de resultados de búsqueda
    for index, row in expedia_df_res.iterrows():
        matching_div = expedia_tree.xpath(row['xpath'])[0]

        try:
            # Obtenemos las características necesarias del hotel
            name = matching_div.xpath(".//div/div[1]/h3")[0].text_content().strip()

            location = matching_div.xpath(".//div/div[1]/div/div/div[2]")[0].text_content().strip()

            nights = matching_div.xpath(".//div/div[2]/div/div[2]/div/div/div[2]/div")[0].text_content()
            nights = ''.join([i for i in nights if i.isdigit()]).strip()

            price = matching_div.xpath(".//div/div[2]/div/div[2]/div/div/div[1]/span/span[2]")[0].text_content()
            price = ''.join([i for i in price if i.isdigit()]).strip()

            image = ""

            try:
                image = matching_div.xpath(".//section/div/span/div[1]/div/div[2]/figure/div/img")[0].xpath('@src')[0].strip()
            except Exception as e:
                print("Image not shown")
            
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
    trivago_df_res = pd.read_csv('./dataframes/res_trivago.csv', index_col=0)

    print("Hotels in DB before Trivago inserts: " + str(records.count_documents({})))

    # Para cada fila del fichero de resultados de búsqueda
    for index, row in trivago_df_res.iterrows():
        matching_div = trivago_tree.xpath(row['xpath'])[0]

        try:
            # Obtenemos las características necesarias del hotel
            
            name = matching_div.xpath(".//article/div[1]/div[2]/div/div/h3/span")[0].text_content().strip()

            location = matching_div.xpath(".//article/div[1]/div[2]/div/div/div[2]/div/p")[0].text_content().strip()

            nights_and_price = matching_div.xpath(".//article/div[1]/div[2]/section/div[1]/article/div/p/em[2]")[0].text_content()

            nights = nights_and_price.split('noches')[0]
            nights = ''.join([i for i in nights if i.isdigit()]).strip()

            price = nights_and_price.split('noches')[1]
            price = ''.join([i for i in price if i.isdigit()]).strip()

            image = matching_div.xpath(".//article/div[1]/div[1]/div[2]/div/meta[3]")[0].attrib['content']

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