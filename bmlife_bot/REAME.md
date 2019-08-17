## BMLIFE Bot

### Description
This is a web crawler used to crawl house data and crime data from internet. 

We implement one function to scrape data from hooli.com and store the downloaded pictures in S3 and the structured data in Postgresql.
We also implement function to scrape crime data from socrata.com. Crime data is stored in local disk.

### Technical details
1. Language: Python 3.6
2. Framework: scrapy + selenium + headless chrome driver
3. Storage: S3 + Postgresql
4. Geo data: Geo data is decoded in realtime by querying opencage with address.

