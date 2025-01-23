import PyCrawler
import pickle

with open('data.pkl', 'rb') as f:
    data = pickle.load(f)

res = PyCrawler.search("tkinter", data)
print(res)