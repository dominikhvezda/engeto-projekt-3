from bs4 import BeautifulSoup
import requests
import sys
import csv

def terminal_launch() -> tuple:
    try:
        web_page = sys.argv[1]
        save_as = sys.argv[2]
        return web_page, save_as
    except IndexError:
        print(
            "Nebyly zadány správně argumenty. "
            "Prosím zadejte argumenty v následujicím formátu: python Election_Scraper.py <\"URL\"> <\"název souboru.csv\">"
        )
        quit()

def make_soup(web_adress) -> BeautifulSoup:
    try:
        answer = requests.get(web_adress)
        return BeautifulSoup(answer.text, features="html.parser")
    except:
        print("Bylo zadáno nesprávné URL. Ukončuji program...")
        quit()

def url_unit(soup) -> list:
    tagy = soup.find_all("td", {"class": "cislo"})
    hrefs = []
    for tag in tagy:
        href = tag.find('a')['href']
        href = "https://volby.cz/pls/ps2017nss/" + href
        hrefs.append(href)
    return hrefs

def find_city_code(finding_city, cities, codes) -> str:
    dict = {}
    for city, code in zip(cities, codes):
        dict[city] = code
    return dict.get(finding_city)

def city_data_scraping(url) -> tuple[list, list, list]:
    soup = make_soup(url)
    tagy = soup.find_all("td", {"class": "cislo", "headers": ("sa2", "sa3", "sa6")})
    tagy = convert_characters_to_digit([tag.text for tag in tagy])

    pocty_opravnenych_volicu, pocty_vydanych_obalek, pocty_platnych_hlasu = tagy
    return pocty_opravnenych_volicu, pocty_vydanych_obalek, pocty_platnych_hlasu

def get_codes_and_city_names(soup) -> tuple[list, list]:
    tagy1 = soup.find_all("td", {"class": "cislo"})
    city_codes = [tag.text for tag in tagy1]

    tagy2 = soup.find_all("td", {"class": "overflow_name"})
    city_names = [tag.text for tag in tagy2]
    return city_codes, city_names

def parties_scraping(url) -> list:
    soup = make_soup(url)
    tagy = soup.find_all("td", {"class": "overflow_name"})
    return [tag.text for tag in tagy]


def convert_characters_to_digit(characters) -> list:
    return [int(udaj.replace("\xa0", "")) for udaj in characters]

def votes_scraping(url) -> list:
    soup = make_soup(url)
    tagy = soup.find_all("td", {"class": "cislo", "headers": ("t1sa2 t1sb3", "t2sa2 t2sb3")})
    return convert_characters_to_digit([tag.text for tag in tagy])

def make_dict(kod, nazev, opravneni_volici, pocet_obalek, platne_hlasy, strana, pocet_hlasu) -> dict:
    dict = {
        "Kód obce": kod,
        "Název obce": nazev,
        "Voliči v seznamu": opravneni_volici,
        "Vydané obálky": pocet_obalek,
        "Platné hlasy": platne_hlasy
        }
    for strana, pocet_hlasu in zip(strana, pocet_hlasu):
        dict[strana] = pocet_hlasu
    return dict

def save_csv(list_election_results, filename):
    header = list_election_results[0].keys()
    with open(filename, mode="w", encoding="utf-8", newline="") as file:
        entry = csv.DictWriter(file, delimiter=";", fieldnames=header)
        entry.writeheader()
        entry.writerows(list_election_results)
    print()
    print("Data byla úspěšně exportována do souboru", filename)

def get_city_name(url) -> str:
    soup = make_soup(url)
    tagy = soup.find_all("h3")
    print(tagy[-3].text, "Načítám data...", end="")

    city_name = tagy[-3].text.split(" ", maxsplit=1)[1].rstrip()
    return city_name

def main():
    url, jmeno_souboru = terminal_launch()
    soup = make_soup(url)
    url_uzemnich_celku = url_unit(soup)
    vsechny_kody_obci, vsechny_nazvy_obci = get_codes_and_city_names(soup)

    seznam_volebnich_vysledku = []
    for url in url_uzemnich_celku:
        nazev_obce = get_city_name(url)
        kod_obce = find_city_code(nazev_obce, vsechny_nazvy_obci, vsechny_kody_obci)
        pocty_opravnenych_volicu, pocty_vydanych_obalek, pocty_platnych_hlasu = city_data_scraping(url)
        seznam_kandidujicich_stran = parties_scraping(url)
        hlasy_kandidujicich_stran = votes_scraping(url)
        slovnik = make_dict(kod_obce, nazev_obce, pocty_opravnenych_volicu, pocty_vydanych_obalek, pocty_platnych_hlasu, seznam_kandidujicich_stran, hlasy_kandidujicich_stran)
        seznam_volebnich_vysledku.append(slovnik)

    save_csv(seznam_volebnich_vysledku, jmeno_souboru)

if __name__ == "__main__":
    main()