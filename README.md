Dokumentace semestrální práce

Zadání: Web scraper vybraných realitních stránek, který bude stahovat údaje o 
prodávané nemovitosti (lokalita, cena, typ nemovitosti, rozloha...) s využitím 
frameworku Scrapy. Získaná data bude exportovat do souborů .csv formátu. 
Aplikace poté bude porovnávat ceny nemovitostí v uživatelem zvolené lokalitě,
typy nemovistostí - např. porovnání cen za m2, porovnání cen bytů s n počtem 
místností  (vizualizace).

Požadavky na software: 
 - Python 2.7 a vyšší
 - scrapy
 - $ pip install scrapy / $ conda install -c conda-forge scrapy
   (je nutno mit alespon verzi 2.0)

Spuštění aplikace:

- $ cd webscraper/vizualization
- $ python3 run_app.py
- http://127.0.0.1:8050/

pozn.: spouští se pouze vizualizační část semestrální práce, jelikož scrapování dat trvá něco přes hodinu
a předpokládám, že nebudete chtít sedět hodinu u počítače a čekat než doběhne program.


Testování:
 
 - $ pytest (v webscraper složce projektu, otestuje čištění dat)
 - $ scrapy check  (otestuje webscraper)
 - $ scrapy crawl testbot (bude scrapovat pouze 1.stránku dané url, výsledná data se nachází v webscraper/webscraper/output_files/test_realities.csv)
