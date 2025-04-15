
```python
import scrapy
from scrapy import Request
from hashlib import sha256
import re


class DivarSpider(scrapy.Spider):
    name = "divar_apartment"
    allowed_domains = ["divar.ir"]
    custom_settings = {
        "CONCURRENT_REQUESTS": 1,
        "DOWNLOAD_DELAY": 8.57,  # 7 requests per minute
        "FEED_EXPORT_ENCODING": "utf-8",
        "FEED_FORMAT": "csv",
        "FEED_URI": "Divar_nasimshahr_buy_apartment.csv",
    }

    def start_requests(self):
        base_url = "https://divar.ir/s/nasimshahr/buy-apartment"
        query_params = "price=750000000-1300000000&sort=sort_date"
        start_url = f"{base_url}?{query_params}"

        for page in range(1, 23):  # Pages 1 to 22
            if page == 1:
                url = start_url
            else:
                url = f"{start_url}&page={page}"
            yield Request(url, callback=self.parse)

    def parse(self, response):
        for post in response.css("div.kt-post-card__body"):
            # Extract item URL
            item_relative_url = post.xpath("../@href").get()
            if not item_relative_url:
                continue

            item_url = response.urljoin(item_relative_url)
            url_digest = sha256(item_url.encode("utf-8")).hexdigest()

            # Extract and process child texts
            child_texts = []
            for child in post.xpath(".//*"):
                text = child.xpath("string()").get()
                if text:
                    cleaned_text = re.sub(r"\s+", " ", text.strip())
                    child_texts.append(cleaned_text)

            yield {
                "child_texts": ", ".join(child_texts),
                "item_url": item_url,
                "url_digest": url_digest,
            }

```



To solve this problem, we need to convert an existing web scraping script using Requests and BeautifulSoup into a more efficient and maintainable version using the Scrapy framework. The goal is to scrape apartment listings from Divar.ir, handle pagination, manage request rate limits, and save the data to a CSV file.

### Approach
1. **Scrapy Framework**: Utilize Scrapy for efficient web scraping, which handles asynchronous requests and provides built-in features for managing request rates and concurrency.
2. **Pagination Handling**: Generate requests for each page dynamically, appending the correct query parameters to the URL.
3. **Rate Limiting**: Configure Scrapy to send requests at a controlled rate to avoid being blocked by the server.
4. **Data Extraction**: Use Scrapy selectors to parse HTML content and extract required fields such as listing URLs, their SHA256 hashes, and text content from child elements.
5. **Data Storage**: Save the extracted data into a CSV file with proper encoding and structure.

### Solution Code
```python
import scrapy
from scrapy import Request
from hashlib import sha256
import re


class DivarSpider(scrapy.Spider):
    name = "divar_apartment"
    allowed_domains = ["divar.ir"]
    custom_settings = {
        "CONCURRENT_REQUESTS": 1,
        "DOWNLOAD_DELAY": 8.57,  # 7 requests per minute
        "FEED_EXPORT_ENCODING": "utf-8",
        "FEED_FORMAT": "csv",
        "FEED_URI": "Divar_nasimshahr_buy_apartment.csv",
    }

    def start_requests(self):
        base_url = "https://divar.ir/s/nasimshahr/buy-apartment"
        query_params = "price=750000000-1300000000&sort=sort_date"
        start_url = f"{base_url}?{query_params}"

        for page in range(1, 23):  # Pages 1 to 22
            if page == 1:
                url = start_url
            else:
                url = f"{start_url}&page={page}"
            yield Request(url, callback=self.parse)

    def parse(self, response):
        for post in response.css("div.kt-post-card__body"):
            # Extract item URL
            item_relative_url = post.xpath("../@href").get()
            if not item_relative_url:
                continue

            item_url = response.urljoin(item_relative_url)
            url_digest = sha256(item_url.encode("utf-8")).hexdigest()

            # Extract and process child texts
            child_texts = []
            for child in post.xpath(".//*"):
                text = child.xpath("string()").get()
                if text:
                    cleaned_text = re.sub(r"\s+", " ", text.strip())
                    child_texts.append(cleaned_text)

            yield {
                "child_texts": ", ".join(child_texts),
                "item_url": item_url,
                "url_digest": url_digest,
            }
```

### Explanation
1. **Scrapy Spider Setup**: The spider is named `divar_apartment` and configured to handle the domain `divar.ir`.
2. **Custom Settings**: 
   - `CONCURRENT_REQUESTS` set to 1 to send requests sequentially.
   - `DOWNLOAD_DELAY` set to approximately 8.57 seconds to allow 7 requests per minute, adhering to the site's rate limits.
   - `FEED_EXPORT` settings to save the output as a UTF-8 encoded CSV file.
3. **Start Requests**: Generates URLs for the first 22 pages, appending the `page` parameter correctly to handle pagination.
4. **Parse Method**: 
   - Extracts the URL of each apartment listing from the parent element of the post div.
   - Computes the SHA256 hash of the listing URL.
   - Collects text from all descendant elements of each post, cleans the text by removing extra whitespace, and joins them into a single string.
5. **Data Yielding**: Yields a dictionary for each listing containing the cleaned text, URL, and its hash, which Scrapy automatically writes to the CSV file.

This approach ensures efficient and maintainable scraping with proper handling of pagination and rate limits, leveraging Scrapy's capabilities for robust web scraping.



### revised


### Answer
Here's how to parameterize and call the spider with different configurations, along with execution examples:

```python
import scrapy
from scrapy import Request
from hashlib import sha256
import re

class DivarSpider(scrapy.Spider):
    name = "divar_apartment"
    allowed_domains = ["divar.ir"]
    
    def __init__(self, base_url=None, query_params=None, pages=22, output_file=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set defaults if not provided
        self.base_url = base_url or "https://divar.ir/s/nasimshahr/buy-apartment"
        self.query_params = query_params or "price=750000000-1300000000&sort=sort_date"
        self.pages = int(pages)
        
        # Configure dynamic output filename
        self.custom_settings = {
            "CONCURRENT_REQUESTS": 1,
            "DOWNLOAD_DELAY": 8.57,
            "FEED_EXPORT_ENCODING": "utf-8",
            "FEED_FORMAT": "csv",
            "FEED_URI": output_file or self._generate_filename(),
        }

    def _generate_filename(self):
        """Generate filename from URL parameters"""
        clean_path = self.base_url.split("/s/")[-1].replace("/", "_")
        clean_query = self.query_params.split("&")[0].replace("=", "-")
        return f"Divar_{clean_path}_{clean_query}.csv"

    def start_requests(self):
        start_url = f"{self.base_url}?{self.query_params}"
        for page in range(1, self.pages + 1):
            yield Request(
                url=f"{start_url}&page={page}" if page > 1 else start_url,
                callback=self.parse
            )

    def parse(self, response):
        # ... (same parsing logic as original code) ...
```

**Sample Execution Commands:**

1. **Basic usage with default parameters:**
```bash
scrapy crawl divar_apartment
```

2. **Custom location and price range:**
```bash
scrapy crawl divar_apartment \
  -a base_url="https://divar.ir/s/tehran/buy-apartment" \
  -a query_params="price=500000000-1000000000&sort=sort_date" \
  -a pages=10 \
  -a output_file="tehran_affordable.csv"
```

3. **Different city and custom pages:**
```bash
scrapy crawl divar_apartment \
  -a base_url="https://divar.ir/s/karaj/buy-apartment" \
  -a pages=5 \
  -o karaj_listings.csv
```

4. **Commercial properties instead of apartments:**
```bash
scrapy crawl divar_apartment \
  -a base_url="https://divar.ir/s/isfahan/commercial-properties" \
  -a query_params="sort=sort_date" \
  -a pages=15 \
  -o isfahan_commercial.csv
```

**Key Parameters:**
- `base_url`: The main URL path (e.g., `/tehran/buy-apartment`)
- `query_params`: Filter parameters (price ranges, sorting, etc.)
- `pages`: Number of pages to scrape (default: 22)
- `output_file`: Custom output filename (optional)

**Rate Limiting Note:** The spider maintains the 7-requests-per-minute limit through the `DOWNLOAD_DELAY` setting. Adjust if the website's policy changes.

This parameterized version allows for easy customization of:
- Target location/property type via `base_url`
- Price filters and sorting via `query_params`
- Pagination depth through `pages`
- Output file naming convention

The spider will automatically generate meaningful filenames based on the parameters if no custom output filename is specified.
