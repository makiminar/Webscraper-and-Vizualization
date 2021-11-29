from os import system

output_dir = 'output_files'

system('rm -rf ' + output_dir)

system('scrapy crawl realitybot')
# system('python3 app.py')
