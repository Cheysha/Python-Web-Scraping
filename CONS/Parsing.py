from bs4 import BeautifulSoup
import os

#subject is entity id as used by consumeraffairs.com  (e.g. https://www.consumeraffairs.com/rx/walmart_rx.html)
subject = "aarp"

pages = []
reviews = []

# loop through all pages in archive and only add ones that contain our subject name in the title
for filename in os.listdir("../Archive/ConsumerAffairs"):
    if subject in filename:
        with open(f"../Archive/ConsumerAffairs/{filename}", "r",encoding="utf-8") as f:
            pages.append(f.read())

if len(pages) == 0:
    print("No pages found")
    exit()

for page in pages:
    soup = BeautifulSoup(page, 'html.parser')
    soup_results = soup.find_all('div', class_='rvw-bd') # these are the reviews in the page
    for item in soup_results:
        reviews.append(item.find_all('p'))

# write to file
with open(f"../Reviews/ConsumerAffairs/{subject}_reviews.txt", "w", encoding="utf-8") as f:
    for review in reviews:
        f.write('*: '+ review[0].text)
        f.write("\n")

print(f"Number of pages: {len(pages)}")
print(f"Number of reviews: {len(reviews)}")


