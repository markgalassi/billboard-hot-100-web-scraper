#! /usr/bin/env python3

# credit to Jaimes Subroto for writing the original program that
# worked with the 2018 billboard html format.  it has changed
# completely in 2023, so this is a mostly-rewritten version that
# handles the new format

from urllib.request import urlopen as uRequest
from bs4 import BeautifulSoup as soup

def main():
    url = 'https://www.billboard.com/charts/hot-100'
    # url = 'https://web.archive.org/web/20180415100832/https://www.billboard.com/charts/hot-100/'

    # Opening up connection, grabbing the page
    uClient = uRequest(url)
    page_html = uClient.read() # Offloads content into a variable
    uClient.close() # Close the client

    open('page_saved.html', 'w').write(page_html.decode('utf-8'))

    # HTML parsing
    page_soup = soup(page_html, "html.parser")

    # Grabs all information related to the top 100 songs
    containers = page_soup.select('ul[class*=o-chart-results-list-row]') # *= means contains
    outf = 'billboard_hot_100.csv'
    with open(outf, 'w') as fp:
        headers = 'Song, Artist, Last Week, Peak Position, Weeks on Chart\n'
        fp.write(headers)
        # Loops through each container
        for container in containers:
            handle_single_row(container, fp)
    print(f'\nWeb scraped data saved to {outf}')

def handle_single_row(container, fp):
    all_list_items = container.find_all('li')
    title_and_artist = all_list_items[4]
    # try to separate out the title and artist.  title should be an
    # <h3> element, artist is a <span> element
    title = title_and_artist.find('h3').text.strip()
    artist = title_and_artist.find('span').text.strip()
    # now the rest of the columns
    last_week = all_list_items[7].text.strip()
    peak_pos = all_list_items[8].text.strip()
    weeks_on_chart = all_list_items[9].text.strip()
    # we have enough to write an entry in the csv file
    csv_line = f'"{title}", "{artist}", {last_week}, {peak_pos}, {weeks_on_chart}'
    print(csv_line)
    fp.write(csv_line + '\n')


if __name__ == '__main__':
    main()
