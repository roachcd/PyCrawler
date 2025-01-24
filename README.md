# PyCrawler
A simple web crawler with search functionality for python.

For convience, multiple test files are included showing how to use PyCrawler.

# Getting Started
## Crawling a site
The crawl function will return an array that the search function can search through. Saving your crawl to a pickle file is recommended.

```python
import PyCrawler
data = PyCrawler.crawl(rootPages[], depth, verbose, delay)
```
**Root pages** is an array of pages to begin your crawl at. <br>
**Depth** is an integer of how many layers of subpages to search through. <br>
**Verbose** is a boolean defining if you want the library to print data about the crawl to the terminal. <br>
**Delay** is a float defining how many seconds to wait between page searches as a courtesy to the site being searched. <br>

## Searching your crawl
The search function will return an array that is sorted by the most similar to least similar page, where array[0] is the most similar.
```python
import PyCrawler
data = PyCrawler.search(string, data)
```
**String** is a string of the text that you are looking for in your crawled data. <br>
**Data** is your crawled data that is given by ```data=PyCrawler.crawl()```
