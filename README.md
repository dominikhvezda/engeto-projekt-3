# engeto-projekt-3
# ELECTIONS SCRAPER
Vítám Vás, u svého třetího projektu do ENGETO python akademie.
Tento skript je navržen tak, aby sbíral data o volbách do Poslanecké sněmovny v roce 2017 v České republice. Prostřednictvím oficiálního webu s výsledky voleb: https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ ukládá data do CSV souboru. Chcete-li tento program spustit, vyberte volební obvod, ze kterého chcete sbírat data (např. pro obvod Benešov vyberte následující URL: https://www.volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=2&xnumnuts=2101) a zadejte název souboru s příponou csv.

# KNIHOVNY
Seznam knihoven je uvedený v souboru _requirements.txt_. Instalace knihoven proběhne následujícím příkazem:
```
pip install -r requirements.txt
```

# UKÁZKA PROJEKTU
Chceme-li informace například z obvodu Benešov, v příkazové řádce zadáme následující příkaz:
```
python election_scraper.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101" "volby_Benesov.csv"
```
V repozitáři se následně vytvoří soubor _csv_ s výsledky voleb.
