from bs4 import BeautifulSoup
import os

subject = "walmart_rx"

pages = []
reviews = []

# loop through all pages in archive and only add ones that contain our subject name in the title
for filename in os.listdir("Archive"):
    if subject in filename:
        with open(f"Archive/{filename}", "r",encoding="utf-8") as f:
            pages.append(f.read())

if len(pages) == 0:
    print("No pages found")
    exit()


for page in pages:
    soup = BeautifulSoup(page, 'html.parser')
    # find all divs with class=rw-bd, all p elements in that div are reviews
    r = soup.find_all('div', class_='rvw-bd')
    for i in r:
        reviews.append(i.find_all('p'))

# write to file
with open(f"Reviews/{subject}_reviews.txt", "w", encoding="utf-8") as f:
    for review in reviews:
        f.write(str(review))
        f.write("\n")



