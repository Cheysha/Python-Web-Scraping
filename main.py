import requests
from bs4 import BeautifulSoup

pages = []
number_of_pages = 1
current_page = 1

# increment page number until we stop getting valid pages
# server will return last valid page if you go too hig or low, check if current page is also the last page, break if true

# right now this just grabs every <p> can be narrowed down so it only grabs the reviews, also needs to be a juypter notebook

while True:
    # get page
    page = requests.get(f"https://www.consumeraffairs.com/rx/aarp.html?page={current_page}", headers={'User-Agent': 'Mozilla/5.0'})

    # get the returned url
    returned_url = page.url

    if (returned_url == f"https://www.consumeraffairs.com/rx/aarp.html?page={current_page-1}"):
        break

    # put page in our page archive
    pages.append(page)
    current_page += 1
    number_of_pages += 1

print(f"Number of pages: {len(pages)}")
print(number_of_pages)

for page in pages:
    soup = BeautifulSoup(page.content, 'html.parser')
    r = soup.find_all('p')
    print(r)





