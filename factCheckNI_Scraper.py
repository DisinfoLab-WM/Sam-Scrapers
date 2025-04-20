import xml.etree.ElementTree as ET
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json

def parse_rss_feed(rss_url, output_file="FactCheckNI_Articles.json"):
    response = requests.get(rss_url)
    root = ET.fromstring(response.content)

    channel = root.find("channel")
    items = channel.findall("item")

    data = {"articles": {}}

    for i, item in enumerate(items):
        title = item.find("title").text.strip()
        link = item.find("link").text.strip()
        creator = item.find("{http://purl.org/dc/elements/1.1/}creator")
        author = creator.text.strip() if creator is not None else "Unknown"

        # Parse and convert the pubDate
        pub_date_str = item.find("pubDate").text.strip()
        pub_date = datetime.strptime(pub_date_str, "%a, %d %b %Y %H:%M:%S %z")
        unix_timestamp = int(pub_date.timestamp())
        formatted_date = pub_date.strftime("%Y-%m-%d %H:%M:%S")

        # Extract article text from <content:encoded>
        description = item.find("description")
        if description is not None:
            soup = BeautifulSoup(description.text, "html.parser")
            print(soup.get_text().split("\n"))
            text = soup.get_text().split("\n")[0].strip()
        else:
            text = ""
        
        data["articles"][str(i)] = {
            "title": title,
            "text": text,
            "author": author,
            "date_published": formatted_date,
            "unix_date_published": unix_timestamp,
            "organization_country": "United Kingdom",
            "site_name": "FactCheckNI",
            "url": link,
            "language": "en"
        }

    # Write to file
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


rss_url = "https://factcheckni.org/feed/"  
parse_rss_feed(rss_url)
