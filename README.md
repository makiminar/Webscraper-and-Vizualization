Dokumentace semestrální práce

Zadání: Web scraper vybraných realitních stránek, který bude stahovat údaje o 
prodávané nemovitosti (lokalita, cena, typ nemovitosti, rozloha...) s využitím 
frameworku Scrapy. Získaná data bude exportovat do souborů .csv formátu. 
Aplikace poté bude porovnávat ceny nemovitostí v uživatelem zvolené lokalitě,
typy nemovistostí - např. porovnání cen za m2, porovnání cen bytů s n počtem 
místností  (vizualizace).

Instalační příručka: 
 nutné mít nainstalovaný Python a Scrapy
 - pip install scrapy / conda install -c conda-forge scrapy
   (je nutno mit alespon verzi 2.0)

Spuštění:
zatím ve fázi, kdy se musí v kódu ručně měnit url a output file v terminálu.
- scrapy runspider spirders/realitybot.py -o outputs/reality-vysocina.csv -t csv 
- (ze složky semestral_work/webscraper/webscraper)
- v kódu pak přidat "vysocina-kraj" do url

Uprava: 
 - pyinstaller run_spider.py
 
Pro vizualizaci je potreba mit nainstalovany Dash:
 - pip install dash

python3 app.py
