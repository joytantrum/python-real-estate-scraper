import requests
import pandas as pd
from bs4 import BeautifulSoup

class Scraper:
    def __init__(self, town):
        # Initialize values
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
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
        data = {'Address': [], 'Location': [], 'Price': [], 'Beds': [], 'Baths': [], 'Sqft': []}

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
                    sqft = clean_details[-9:].split('S')[0]
                if 'n/a' in clean_details[-9:]:
                    sqft = clean_details[-9:].split('n/a')[0].replace(' ', '1')
                data['Sqft'].append(sqft)
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

def main():
    # Function to call the class
    X = Scraper('charleston')
    page_status = X.get_page()
    main_scraper = X.get_data()
    data_fr = X.create_dataframe()
    csv_file = X.write_to_csv('charleston')




if __name__ == '__main__':
    main()