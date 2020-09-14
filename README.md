### Stackoverflow User Reputation Scraper
The gathered dataset comes from the website [stackexchange](https://stackexchange.com/leagues/1/year/stackoverflow/). To extract the first 100 pages of the website run the following command in the `scraper` folder:

```bash
scrapy crawl so_spider -a num_pages=100 -o so_data.csv
```

This will save the data to the file `so_data.csv`.

