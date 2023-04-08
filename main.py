
import time
from pathlib import Path
import sys
import os
scripts_directory = Path(os.path.abspath(__file__).replace(f"{os.path.basename(__file__)}", '') + f"/gscraper")
sys.path.insert(1,str(scripts_directory))
import playwright_scrapper


def run(query,num_questions_to_scraper,headless_mode=True):
    playwright_scrapper.scrapper_g(query,num_questions_to_scraper,headless_mode)


print(run(query='what is a list of exercises',num_questions_to_scraper=20))
