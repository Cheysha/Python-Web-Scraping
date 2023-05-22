# Scraping is Fun

Python script to scrape consumeraffairs.com for reviews


## Usage
Script works by taking a subject, which will be the consumeraffairs enitity ID, in this example the subject is == "walmart_rx"

```python
    page = requests.get(f"https://www.consumeraffairs.com/rx/{subject}.html?page={current_page}", headers={'User-Agent': 'Mozilla/5.0'})
```
you can also pass in the subject as a command line argument

```bash
python3 cascraper.py walmart_rx
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)