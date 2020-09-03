import pandas as pd
import re

def xpath_soup(element):
    # type: (typing.Union[bs4.element.Tag, bs4.element.NavigableString]) -> str
    """
    Generate xpath from BeautifulSoup4 element.
    :param element: BeautifulSoup4 element.
    :type element: bs4.element.Tag or bs4.element.NavigableString
    :return: xpath as string
    :rtype: str
    Usage
    -----
    >>> import bs4
    >>> html = (
    ...     '<html><head><title>title</title></head>'
    ...     '<body><p>p <i>1</i></p><p>p <i>2</i></p></body></html>'
    ...     )
    >>> soup = bs4.BeautifulSoup(html, 'html.parser')
    >>> xpath_soup(soup.html.body.p.i)
    '/html/body/p[1]/i'
    >>> import bs4
    >>> xml = '<doc><elm/><elm/></doc>'
    >>> soup = bs4.BeautifulSoup(xml, 'lxml-xml')
    >>> xpath_soup(soup.doc.elm.next_sibling)
    '/doc/elm[2]'
    """
    components = []
    child = element if element.name else element.parent
    for parent in child.parents:  # type: bs4.element.Tag
        siblings = parent.find_all(child.name, recursive=False)
        components.append(
            child.name if 1 == len(siblings) else '%s[%d]' % (
                child.name,
                next(i for i, s in enumerate(siblings, 1) if s is child)
                )
            )
        child = parent
    components.reverse()
    return '/%s' % '/'.join(components)

def get_complete_dataframe(soup, driver, web):

    class_name_webs = {
        "booking": r'\bsr_item\b',
        "expedia": r'\bimagelayout-left-fullbleed\b',
        "tripadvisor": r'\bresult-card\b',
        "destinia": r'\bavailability_list_widget-hotel-card\b',
        "atrapalo": r'\bcard-result-container\b',
        "logitravel": r'\bmo-results-card-list\b',
        "kayak": r'\bHotels-Results-HotelResultItem\b',
        "skyscanner": r'\bHotelCardsListChunk_HotelCardsListChunk__card__2eXne\b'
    }

    xpath_webs = {
        "trivago": ["/html/body/div[]/main/div[]/div/div[]/div/div/div[]/div[]/div[]/section/ol/li[]/div",
            "/html/body/div[]/main/div[]/div[]/div[]/div/div[]/div[]/div[]/div[]/section/ol/li[]/div"]
    }

    if web not in class_name_webs and web not in xpath_webs:
        print("The website you entered is not part of the accepted sites.")
        return None

    else:
        print("----------------------- GETTING " + web.upper() + " DATAFRAME -----------------------")
        df = pd.DataFrame(columns=['xpath', 'reduced_xpath', 'dom_tree_level', 'x_position', 'y_position', 'height', 'width', 'html_children', 'html_attributes',
        'padding_top', 'padding_right', 'padding_bottom', 'padding_left', 
        'margin_top', 'margin_right', 'margin_bottom', 'margin_left',
        'is_search_result'])

        for div in soup:

            try:
                xpath = xpath_soup(div)
                elem = driver.find_element_by_xpath(xpath)

                reduced_xpath = ''.join([i for i in xpath if not i.isdigit()])

                dom_tree_level = reduced_xpath.count('/')

                location = elem.location
                x_position = location['x']
                y_position = location['y']

                size = elem.size
                height = size['height']
                width = size['width']

                html_children = len(div.findChildren())
                html_attributes = len(div.attrs.keys())

                styles = driver.execute_script('var items = {};' +
                    'var compsty = getComputedStyle(arguments[0]);' +
                    'var len = compsty.length;' +
                    'for (index = 0; index < len; index++)' +
                    '{items [compsty[index]] = compsty.getPropertyValue(compsty[index])};' +
                    'return items;', elem)

                padding_top = styles['padding-top'][:-2]
                padding_right = styles['padding-right'][:-2]
                padding_bottom = styles['padding-bottom'][:-2]
                padding_left = styles['padding-left'][:-2]

                margin_top = styles['margin-top'][:-2]
                margin_right = styles['margin-right'][:-2]
                margin_bottom = styles['margin-bottom'][:-2]
                margin_left = styles['margin-left'][:-2]

                is_search_result = False

                if web in class_name_webs:
                    regexp = re.compile(class_name_webs[web])
                    class_name = elem.get_attribute('class')
                    if regexp.search(class_name):
                        is_search_result = True
                
                elif web in xpath_webs:
                    for x in xpath_webs[web]:
                        is_search_result = is_search_result or (reduced_xpath == x)

                # Para quedarnos con resultados que tengan sentido, eliminamos aquellos <div> cuyo
                # tamaño sea menor a 75x75px (aprox 2cm) y cuya posición en pantalla tenga coordenadas
                # negativas.
                if height >= 75 and width >= 75 and x_position >= 0 and y_position >= 0:
                    df.loc[len(df)] = [xpath, reduced_xpath, dom_tree_level, x_position, y_position, height, width, html_children, html_attributes,
                    padding_top, padding_right, padding_bottom, padding_left,
                    margin_top, margin_right, margin_bottom, margin_left,
                    is_search_result]

            except Exception as e:
                print(e)

        print("----------------------- " + web.upper() + " DATAFRAME COMPLETED -----------------------")
        return df

def get_basic_dataframe(soup, driver, web):

    print("----------------------- GETTING " + web.upper() + " DATAFRAME -----------------------")
    df = pd.DataFrame(columns=['xpath', 'reduced_xpath', 'dom_tree_level', 'x_position', 'y_position', 'height', 'width', 'html_children', 'html_attributes',
    'padding_top', 'padding_right', 'padding_bottom', 'padding_left', 
    'margin_top', 'margin_right', 'margin_bottom', 'margin_left'])

    for div in soup:

        try:
            xpath = xpath_soup(div)
            elem = driver.find_element_by_xpath(xpath)

            reduced_xpath = ''.join([i for i in xpath if not i.isdigit()])

            dom_tree_level = reduced_xpath.count('/')

            location = elem.location
            x_position = location['x']
            y_position = location['y']

            size = elem.size
            height = size['height']
            width = size['width']

            html_children = len(div.findChildren())
            html_attributes = len(div.attrs.keys())

            styles = driver.execute_script('var items = {};' +
                'var compsty = getComputedStyle(arguments[0]);' +
                'var len = compsty.length;' +
                'for (index = 0; index < len; index++)' +
                '{items [compsty[index]] = compsty.getPropertyValue(compsty[index])};' +
                'return items;', elem)

            padding_top = styles['padding-top'][:-2]
            padding_right = styles['padding-right'][:-2]
            padding_bottom = styles['padding-bottom'][:-2]
            padding_left = styles['padding-left'][:-2]

            margin_top = styles['margin-top'][:-2]
            margin_right = styles['margin-right'][:-2]
            margin_bottom = styles['margin-bottom'][:-2]
            margin_left = styles['margin-left'][:-2]

            # Para quedarnos con resultados que tengan sentido, eliminamos aquellos <div> cuyo
            # tamaño sea menor a 75x75px (aprox 2cm) y cuya posición en pantalla tenga coordenadas
            # negativas.
            if height >= 75 and width >= 75 and x_position >= 0 and y_position >= 0:
                df.loc[len(df)] = [xpath, reduced_xpath, dom_tree_level, x_position, y_position, height, width, html_children, html_attributes,
                padding_top, padding_right, padding_bottom, padding_left,
                margin_top, margin_right, margin_bottom, margin_left]

        except Exception as e:
            print(e)

    print("----------------------- " + web.upper() + " DATAFRAME COMPLETED -----------------------")
    return df