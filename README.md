Dokumentace semestrální práce

Zadání: Web scraper vybraných realitních stránek, který bude stahovat údaje o 
prodávané nemovitosti (lokalita, cena, typ nemovitosti, rozloha...) s využitím 
frameworku Scrapy. Získaná data bude exportovat do souborů .csv formátu. 
Aplikace poté bude porovnávat ceny nemovitostí v uživatelem zvolené lokalitě,
typy nemovistostí - např. porovnání cen za m2, porovnání cen bytů s n počtem 
místností  (vizualizace).

Požadavky na software: 
 - Python (2.7 a vyšší)
 - scrapy (verze 2.0 a vyšší)
   

Spuštění aplikace:

- $ python webscraper/vizualization/run_app.py
- go to: http://127.0.0.1:8050/

pozn.: spouští se pouze vizualizační část semestrální práce, scrapování se spustí příkazem: python run_spiders.py

Testování:
 
 - $ pytest (otestuje čištění dat)
 - $ scrapy check  (otestuje webscraper)
 - $ scrapy crawl testingbot (bude scrapovat pouze 1.stránku dané url, výsledná data se nachází v webscraper/output_files/test_realities.csv)
