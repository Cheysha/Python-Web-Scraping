# Scraping is Fun

A Python Library that is designed to scrape websites for reveiw data

## Working Sites

Following sites are supported:

- ConsumerAffairs.com
-- server will return last valid page if you go too hig or low, check if current page is also the last page, break if true




## Usage
Script works by taking a subject, which will be the consumeraffairs enitity ID, in this example the subject is == "walmart_rx"

```python
    page = requests.get(f"https://www.consumeraffairs.com/rx/{subject}.html?page={current_page}", headers={'User-Agent': 'Mozilla/5.0'})
```

the script will then store all pages it finds with reveiws, in the Archive folder

the parsing script will take a subject, and find all relevent html documents in the Archive folder,
it will then scrape all reviews it finds and log them in the Revies folder

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)