from collections import Counter
from bs4 import BeautifulSoup
import pandas as pd

from utils import xpath_soup

if __name__ == "__main__":

    website_name = "booking"

    df_res = pd.read_csv('./dataframes/res_' + website_name + '.csv', index_col = 0)
    sr_xpaths = df_res.xpath.tolist()

    soup = BeautifulSoup(open('./webpages/web_' + website_name + '.html', mode = "r", encoding = "utf8"), "html.parser")

    all_children = []

    for element in soup.find_all():
        xpath = xpath_soup(element)

        match = list(filter(xpath.startswith, sr_xpaths))
        if match != []:
            subxpath = xpath.replace(match[0], '')
            if subxpath != '':
                all_children.append(subxpath)

    counter_subxpath = Counter(all_children)

    max_keys = [k for k,v in counter_subxpath.items() if v > len(sr_xpaths) * 0.75]
    max_dict = {i:counter_subxpath[i] for i in counter_subxpath if i in max_keys}

    res = []
    for k in max_keys:
        if not any(item.startswith(k + '/') for item in max_dict.keys()):
            res.append(k)

    print(res)