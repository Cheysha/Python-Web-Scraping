import requests
from bs4 import BeautifulSoup

# setup the page archive and the page counter

subject = "aarp"
pages = []
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

    # put page in our page archive
    pages.append(page)
    current_page += 1
    number_of_pages += 1


# dump eaach page to a file in the Archive folder, if the folder does not exist it will be created
for i in range(len(pages)):
    with open(f"../Archive/ConsumerAffairs/{subject}_{i}.html", "w",encoding="utf-8") as f:
        f.write(pages[i].text)

# print out some info
print(f"Number of pages: {len(pages)}")