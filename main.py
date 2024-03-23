# Web pageのクローラーを開発する
# Start page: http://scp-jp.wikidot.com/scp-series-jp
# hrefが"/scp-XXX-jp"のリンクを全て取得する

import requests
from bs4 import BeautifulSoup
import os
import re
import datasets

# Start page
url = "http://scp-jp.wikidot.com/scp-series-jp"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
main_content = soup.find("div", id="main-content")
scp_links = main_content.find_all("a", href=re.compile("/scp-[0-9]{3}-jp"))
# Get only href
scp_paths = [scp_url["href"] for scp_url in scp_links]
# scp_text_list
# id: str
# text: str
scp_text_list: list[dict[str, str]] = []

for scp_path in scp_paths:
    # scp_path -> /scp-999-jp
    print(scp_path)
    url = f"http://scp-jp.wikidot.com{scp_path}"
    # Save to file ./data/scp-XXX-jp.txt
    # Determine the filename from scp_path
    filename = scp_path.split("/")[-1]
    # Check already downloaded
    if os.path.exists(f"./data/{filename}.txt"):
        print(f"Already downloaded: {filename}")
        # Add text to scp_text_list
        with open(f"./data/{filename}.txt", "r") as f:
            scp_text = f.read()
            scp_text_list.append({"id": filename, "text": scp_text})
        continue
    scp_response = requests.get(url)
    scp_soup = BeautifulSoup(scp_response.text, "html.parser")
    scp_content = scp_soup.find("div", id="page-content")
    # Get only plain text
    scp_text = scp_content.get_text()
    with open(f"./data/{filename}.txt", "w") as f:
        f.write(scp_text)
        # Add text to scp_text_list
        scp_text_list.append({"id": filename, "text": scp_text})

print(len(scp_text_list))

scp_jp_dataset = datasets.Dataset.from_list(scp_text_list)

print(scp_jp_dataset)

scp_jp_dataset.push_to_hub("yuiseki/scp-jp-plain")
