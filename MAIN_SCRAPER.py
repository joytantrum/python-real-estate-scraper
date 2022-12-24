import requests
import pandas as pd
from bs4 import BeautifulSoup
import matplotlib
from matplotlib import pyplot as plt
from matplotlib.ticker import FuncFormatter
import csv


class Scraper:
    def __init__(self, town):
        # Initialize values
        self.headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}
        self.town = town
        self.avg_data = {'Location': [town], 'Average Price': [], 'Average Price per SQFT': []}

    def get_page(self):
        # check HTTP response status codes to find if HTTP request has been successfully completed
        page = requests.get(url=self.url, headers=self.headers)
        status = ''
        if page.status_code >= 100 and page.status_code <= 199:
            status = ('Informational response')
        if page.status_code >= 200 and page.status_code <= 299:
            status = ('Successful response')
        if page.status_code >= 300 and page.status_code <= 399:
            status = ('Redirect')
        if page.status_code >= 400 and page.status_code <= 499:
            status = ('Client error')
        if page.status_code >= 500 and page.status_code <= 599:
            status = ('Server error')
        return status

    def get_data(self):
        # Scrape data
        towns = {"charleston": 8, "folly beach": 22, "isle of palms": 35, "john's island": 40, "james island": 37,
                 "mount pleasant": 49, "north charleston": 52, "daniel island": 188, "ALL": '8,22,35,40,37,49,52,188'}
        data = {'Address': [], 'Location': [], 'Price': [], 'Beds': [], 'Baths': [], 'Sqft': [], 'Price per Sqft': []}

        for i in range(1, 22):
            self.url = f'https://www.marshallwalker.com/listings/index/page:{i}/class:1/status:1,3,6/city:{towns[self.town]}/br:0/br_e:0/fba:0/fba_e:0/hba:0/hba_e:0#real-estate-listings'
            page = requests.get(url=self.url, headers=self.headers)
            soup = BeautifulSoup(page.content, 'html.parser')
            properties = soup.find_all('div', class_='summary-right')
            for prop in properties:

                address = prop.select('div.summary-right h3>a')[0].text
                data['Address'].append(address)

                price = prop.find('div', class_='s-price').text.replace("\t", "").replace('$', '').replace(',', '')
                self.p = price
                if 'R' in price:
                    self.p = price.split('R')[0]
                if 'I' in price:
                    self.p = price.split('I')[0]
                data['Price'].append(int(self.p))

                location = prop.select('small.text-muted')[0].text
                data['Location'].append(location)

                details = prop.find_all("div", class_='s-cut s-common')
                clean_details = details[1].text.strip()
                beds = clean_details[:4]
                data['Beds'].append(beds)

                baths = clean_details[6:-11]
                data['Baths'].append(baths)

                sqft = clean_details[-9:].strip()
                if 'S' in clean_details[-9:]:
                    sqft = clean_details[-9:].split('S')[0].replace(',', '')
                if 'n/a' in clean_details[-9:]:
                    sqft = clean_details[-9:].split('n/a')[0].replace(' ', '1').replace(',', '')
                data['Sqft'].append(int(sqft))

                price_per_sqft = int(self.p) / int(sqft)
                data['Price per Sqft'].append(int(price_per_sqft))
        return data

    def create_dataframe(self):
        # Write scraped data to pandas dataframe
        data = self.get_data()
        df = pd.DataFrame(data, columns=['Address', 'Location', 'Price', 'Beds', 'Baths', 'Sqft'])
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', None)
        return df

    def write_to_csv(self, filename):
        # Write scraped data to csv file
        data = self.get_data()
        df = pd.DataFrame(data, columns=['Address', 'Location', 'Price', 'Beds', 'Baths', 'Sqft'])
        csv = df.to_csv(filename + '_listings.csv')
        return csv

    def get_avg_price_data(self):
        # average home price (price sum / amount of listings)
        # average home price per square foot ((price sum / sum of sqft) / amount of listings))
        data = self.get_data()
        avg_price = round(sum(data['Price']) / int(len(data['Address'])), 2)
        avg_price_per_sqft = round(sum(data['Price per Sqft']) / int(len(data['Address'])), 2)
        self.avg_data['Average Price'].append(avg_price)
        self.avg_data['Average Price per SQFT'].append(avg_price_per_sqft)
        return self.avg_data

    def avg_dataframe(self):
        # Write scraped averages data to pandas dataframe
        data = self.get_avg_price_data()
        df = pd.DataFrame(data, columns=['Location', 'Average Price', 'Average Price per SQFT'])
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', None)
        return df

    def avg_data_to_csv(self):
        # Write scraped average data to csv file
        avg_data = self.avg_data
        df = pd.DataFrame(avg_data, columns=['Location', 'Average Price', 'Average Price per SQFT'])
        csv = df.to_csv('AVG_DATA.csv', index=False)
        return csv

    def add_to_avg_csv(self):
        # Add the average data of a new city to the csv file
        X = Scraper("charleston")
        new_data = X.get_avg_price_data()
        d = {k: str(v[0]) for k, v in new_data.items()}
        with open('AVG_DATA.csv', 'a') as obj:
            writer_object = csv.DictWriter(obj, fieldnames=self.avg_data)
            writer_object.writerow(d)
            obj.close()

    def avg_price_graph(self):
        # Create bar graph from csv file
        data = pd.read_csv('AVG_DATA.csv')
        fig, ax = plt.subplots()
        plt.ticklabel_format(style='plain')
        ax.barh(data['Location'].values, data['Average Price'].values)
        ax.set_ylabel('Location', weight='bold')
        ax.set_xlabel('Price in USD', weight='bold')
        ax.set_title('Average Home Price', weight='bold')
        ax.get_xaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
        fig.tight_layout()
        return plt.show()

    def avg_price_perSQFT_graph(self):
        # Create bar graph from csv file
        data = pd.read_csv('AVG_DATA.csv')
        fig, ax = plt.subplots()
        plt.ticklabel_format(style='plain')
        ax.barh(data['Location'].values, data['Average Price per SQFT'].values)
        ax.set_ylabel('Location', weight='bold')
        ax.set_xlabel('Price in USD', weight='bold')
        ax.set_title('Average Price per Square Foot', weight='bold')
        ax.get_xaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
        fig.tight_layout()
        return plt.show()


def main():
    # Function to call the class
    X = Scraper("isle of palms")

    # Returns page status
    # page_status = X.get_page()

    # Runs the scraper & returns the data dictionary
    #main_scraper = X.get_data()

    # Writes listing data to pandas dataframe
    #main_df = X.create_dataframe()

    # Writes listings data to csv file
    # csv_file = X.write_to_csv("folly beach")

    # Grabs the average data and returns the avg_data dictionary
    avg_price_vals = X.get_avg_price_data()
    print(avg_price_vals)

    # Writes averages data to pandas dataframe
    # avg_df = X.avg_dataframe()

    # Writes the average data to csv file
    #avg_data = X.avg_data_to_csv()

    # Writes a new line of average data to same csv file
    #add_avg = X.add_to_avg_csv()

    # Returns the graph for average prices
    #plot = X.avg_price_graph()

    # Returns the graph for average prices per SQFT
    #SQFT_plot = X.avg_price_perSQFT_graph()



if __name__ == '__main__':
    main()