from os import system

system('cd webscraper')
system('python3 run_spiders.py')
system('cd ../vizualization')
system('python3 run_clean_data.py')
