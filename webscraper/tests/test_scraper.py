# -*- coding: utf-8 -*-

import os
import pytest
from webscraper.webscraper.spiders import realitybot


def test_exists():
    """checks if the file file exists in the correct repository"""
    assert os.path.isfile('/home/marketa/Projects/PyCharmProjects/PYT/semestral_work/webscraper/webscraper/spiders'
                          '/realitybot.py')

# pozn. - unit testy na Scraper se dělají obtížně a většinou nalezené postupy byly vytvořit si fake_html_response a
# na to volat funkce scraperu nebo využívat tzv. Spider Contracts, což je integrovaná
