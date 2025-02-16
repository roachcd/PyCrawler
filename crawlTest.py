import PyCrawler
import pickle

pages = ["https://docs.python.org/3/library/"]

data = PyCrawler.crawl(pages, 2, True, 0)

with open('data.pkl', 'wb') as f:
    pickle.dump(data, f)