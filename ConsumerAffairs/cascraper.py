import requests
from bs4 import BeautifulSoup

# setup the page archive and the page counter
subject = "walmart_rx"
pages = []
reviews = []
number_of_pages = 1
current_page = 1

# run until we get a page that is not valid
while True:
    url = f"https://www.consumeraffairs.com/rx/{subject}.html?page={current_page}"

    # get page
    page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

    # get the returned url
    returned_url = page.url

    # escape condition, also, 1st page does not abide by the rules
    if (returned_url != url and current_page != 1):
        break
    if (current_page == 100):
        break

    # put page in our pages list
    pages.append(page)
    current_page += 1
    number_of_pages += 1

# print out some info
print(f"Number of pages: {len(pages)}")

# if we have no pages, exit
if len(pages) == 0:
    print("No pages found")
    exit()

# loop through all pages and get the reviews
for page in pages:
    soup = BeautifulSoup(page.content, 'html.parser')
    soup_results = soup.find_all('div', class_='rvw-bd') # these are the reviews in the page
    for item in soup_results:
        reviews.append(item.find_all('p'))

# write to file
'''
with open(f"../Reviews/ConsumerAffairs/{subject}_reviews.txt", "w", encoding="utf-8") as f:
    for review in reviews:
        f.write('*: ' + review[0].text)
        f.write("\n")
'''
print(f"Number of pages: {len(pages)}")
print(f"Number of reviews: {len(reviews)}")


