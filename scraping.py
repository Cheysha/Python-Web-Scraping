import requests
from bs4 import BeautifulSoup

# setup the page archive and the page counter

subject = "walmart_rx"
pages = []
number_of_pages = 1
current_page = 1

# run until we get a page that is not valid

while True:
    # get page
    page = requests.get(f"https://www.consumeraffairs.com/rx/{subject}.html?page={current_page}", headers={'User-Agent': 'Mozilla/5.0'})

    # get the returned url
    returned_url = page.url

    # escape condish
    if (returned_url == f"https://www.consumeraffairs.com/rx/aarp.html?page={current_page-1}"):
        break
    if (current_page == 10):
        break

    # put page in our page archive
    pages.append(page)
    current_page += 1
    number_of_pages += 1


# dump eaach page to a file in the Archive folder, if the folder does not exist it will be created
for i in range(len(pages)):
    with open(f"Archive/{subject}_{i}.html", "w",encoding="utf-8") as f:
        f.write(pages[i].text)

# print out some info
print(f"Number of pages: {len(pages)}")
