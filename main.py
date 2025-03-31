from utils import *

item_urls = [
    "https://us.jellycat.com/amuseables-teapot/",
    "https://us.jellycat.com/amuseables-bouquet-of-flowers/",
    "https://us.jellycat.com/amuseables-brie/",
    "https://us.jellycat.com/amuseables-toilet-roll/",
    "https://us.jellycat.com/bartholomew-bear-bathrobe/",
    "https://us.jellycat.com/amuseables-bubble-tea/",
    "https://us.jellycat.com/theo-turkey/",
]


def scrape_and_write_to_file(url):
    scraper = Scraper()
    html = scraper.get(url)
    with open("output.txt", "w", encoding="utf-8") as f:
        f.write(html)
    scraper.quit()


def read_file_and_parse():
    with open("output.txt", "r", encoding="utf-8") as file:
        html_content = file.read()

    parse_detail_page(html_content)


if __name__ == "__main__":
    scraper = Scraper()

    with open("output.txt", "w", encoding="utf-8") as f:
        for url in item_urls:
            html = scraper.get(url)
            if html == "":
                continue
            item_name, status = parse_detail_page(html)
            f.write(f"{item_name},{status}\n")
