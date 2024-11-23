# Käyttöohje

## Asennus ja käynnistys

Kun olet kloonannut repositorion omalle koneellesi, luo virtuaaliympäristö ja aktivoi se projekti juurihakemistossa seuraavilla komennoilla:

```bash
python -m venv venv
source venv/bin/activate
```

Tämän jalkein asenna projectin riipuvuudet komennolla:

```bash
pip install -r requirements.txt
```

Sovelluksen voi tämän jälkeen käynnistää komennolla

```bash
python -m main
```	

## Testit

Jos haluat ajaa sovellukselle yksikkötestejä, sen voi tehdä komennolla

```bash
pytest
```

Testikattavuusraportin voi muodostaa komennolla

```bash
coverage run -m pytest
coverage report
```

## Sovelluksen käyttö
Kun sovellus käynnistetään, se luo käyttäjälle luolaston karttavisualisaation.