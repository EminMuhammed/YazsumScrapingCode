
import requests
from bs4 import BeautifulSoup
import pandas as pd

baseurl = "https://www.emlakjet.com/vitrin/"
url_head = "https://www.emlakjet.com"


def get_url(url):
    """
    It sends requests to the url and parse it with beautifulsoup

    Parameters
    ----------
    url: string
    website to be requested

    Returns
    -------
    bs4.BeautifulSoup

    """
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "lxml")
    return soup


def scrape_url(soup):
    """
    collects the a tags on the page
    Parameters
    ----------
    soup: bs4.BeautifulSoup
    page source

    Returns
    -------
    list

    """
    columns = soup.find_all("div", attrs={"class": "styles_gridColumn__1hxWa"})
    url_list = [url_head + col.a.get("href") for col in columns]
    return url_list


def scrape_all_page(last_page, baseurl):
    """
    Collects a tags by switching to other pages

    Parameters
    ----------
    last_page: int
    last page of the site

    baseurl: string
    main link of website

    Returns
    -------
    list
    """
    home_url_list = []
    for page in range(1, last_page + 1):
        print(page)
        mainurl = baseurl + str(page)
        print(mainurl)
        soup = get_url(mainurl)
        home_url_list.append(scrape_url(soup))
        print(home_url_list)
        print("************")
    return home_url_list


def convert_single_list(liste):
    """
    converts nested list to single list
    Parameters
    ----------
    liste: list
    nested list

    Returns
    -------
    list
    """
    single_list = [item for elem in liste for item in elem]
    return single_list


def scrape_property(home_urls):
    """
    collects features

    Parameters
    ----------
    home_urls: list
    list of home links

    Returns
    -------
    list
    """
    home_info = []
    for ln in home_urls:
        soup = get_url(ln)
        title = ""
        price = ""
        property_list = []

        try:
            title = soup.find("h1", attrs={"class": "styles_detailTitle__qBXKm"}).text.strip()
            price = soup.find("div", attrs={"class": "styles_price__1e65F"}).text.strip()
            property_area = soup.find("div", attrs={"class": "styles_properties__12d_v"})
            property_list = [data.text.strip() for data in property_area.find_all("span")]
        except:
            pass

        home_info.append([ln, title, price, property_list])
    return home_info


def save_excel(propertylist, name):
    """
    saves list as excel file

    Parameters
    ----------
    propertylist: list
    the list you want to save
    name: string
    name to excel file
    Returns
    -------
    None
    """
    df = pd.DataFrame(propertylist)
    df.columns = ["url", "title", "price", "properties"]
    df.to_excel(f"{name}.xlsx")


urls = convert_single_list(scrape_all_page(3, baseurl))

home_features = scrape_property(urls)

save_excel(home_features, "home")
