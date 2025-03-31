from bs4 import BeautifulSoup
import re

def parse_detail_page(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    title_div = soup.find('h1', class_=re.compile(r'\btitle\b'))
    cart_button = soup.find('input', id='form-action-addToCart')
    # soup.find_all("input", {"id":re.compile(r"qty\-\d+")})
    
    if title_div and cart_button:
        title = title_div.get_text(strip=True)
        status = 'OUT OF STOCK' if cart_button.has_attr('disabled') else 'IN STOCK'
        print(f"{title}: {status}")
        return (title, status)
    else:
        print("--------------- Something went wrong -------------")
        print(html_content)
        return None
    

def parse_browse_page(html_content, interested_items):
    """
    Parse the HTML content from the page and print information about
    the items of interest.
    """
    soup = BeautifulSoup(html_content, 'html.parser')

    cards = soup.find_all('article', class_=re.compile(r'\bcard\b'),
                        attrs={'data-test': True})

    for card in cards:
        badge_div = card.find('div', class_='ss__badge')
        title_div = card.find('h3', class_=re.compile(r'\bcard-title\b'))
        price_div = card.find('span', attrs={'data-product-price-with-tax': True})

        badge = 'NO' if badge_div and badge_div.get_text(strip=True) == 'Out of Stock' else 'YES'
        title = title_div.get_text(strip=True) if title_div else ''
        price = price_div.get_text(strip=True) if price_div else ''

        if title in interested_items:
            print(f"{title} | {price} | {badge}")
