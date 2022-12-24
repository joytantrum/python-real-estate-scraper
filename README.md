# python-real-estate-scraper
web scraping project to grab listing data and compare home prices.

# Prerequisites
- [Python](https://www.python.org)
- [Requests](https://pypi.org/project/requests/)
- [Pandas](https://pandas.pydata.org/docs/getting_started/install.html)
- [BeautifulSoup](https://pypi.org/project/beautifulsoup4/)
- [Matplotlib](https://matplotlib.org/stable/users/installing/index.html)
- [CSV](https://pypi.org/project/python-csv/)

# Set up
download & install python 3 from the official site.

run the following in the terminal to install required libraries: 
```bash
  pip3 install -r requirements.txt
```

download the source code from the repository and run as a .py file.
```bash
  python3 MAIN_SCRAPER.py
```
# How it works
This scraper class grabs listing data from the [Marshall Walker](https://www.marshallwalker.com/) real estate agency website. I initally wrote this class to include the most popular towns in the Charleston area, but more data can be scraped by adjusting the towns parameter.

To scrape data from your chosen location, adjust the town parameter in the main function. 

To create the pandas dataframe of your chosen location, call the create_dataframe() method. Your output should look like this:
<p align="center">
  <img src="img/sample_dataframe.png" width="500" title="sample">
</p>
