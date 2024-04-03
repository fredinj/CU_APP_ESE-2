import streamlit as st
import requests
import urllib.parse
from bs4 import BeautifulSoup
from fake_useragent import UserAgent as ua
from urllib.parse import urlparse, parse_qs


# flip = {"name": "Combo of 2 Pack Running Shoes For Men  (Blue, Grey)", "price": "₹586", "rating": "3.6", "image": "https://rukminim2.flixcart.com/image/832/832/xif0q/shoe/h/b/h/10-rng-551-blu-514-gry-10-bruton-blue-grey-original-imagracyughuwe4w.jpeg?q=70&crop=false", "link":"https://www.flipkart.com/bruton-combo-2-pack-running-shoes-men/p/itm9672718d7ebee?q=blue+shoes&qH=72cf29364577a0b7"}
# flip2 = {"name": "Combo of 2 Pack Running Shoes For Men  (Blue, Grey)", "price": "₹586", "rating": "3.6", "image": "https://rukminim2.flixcart.com/image/832/832/xif0q/shoe/h/b/h/10-rng-551-blu-514-gry-10-bruton-blue-grey-original-imagracyughuwe4w.jpeg?q=70&crop=false", "link":"https://www.flipkart.com/bruton-combo-2-pack-running-shoes-men/p/itm9672718d7ebee?q=blue+shoes&qH=72cf29364577a0b7"}
# flip3 = {"name": "Combo of 2 Pack Running Shoes For Men  (Blue, Grey)", "price": "₹586", "rating": "3.6", "image": "https://rukminim2.flixcart.com/image/832/832/xif0q/shoe/h/b/h/10-rng-551-blu-514-gry-10-bruton-blue-grey-original-imagracyughuwe4w.jpeg?q=70&crop=false", "link":"https://www.flipkart.com/bruton-combo-2-pack-running-shoes-men/p/itm9672718d7ebee?q=blue+shoes&qH=72cf29364577a0b7"}

# markets = [flip, flip2, flip3]

# search_term = st.text_input("Search")


# if st.button("Search"):
#   scrape_market(search_term)
  
  
  
def main():
  st.title("Search for your product name or ID")

  search_term = st.text_input("Search")
  if st.button("Search"):  
    scrape_market(search_term)
    
    
  
def scrape_market(search_term):
  
  encoded_term = urllib.parse.quote_plus(search_term)
  # flip_product = scrape_flipkart(encoded_term)
  
  market_list = []
  
  market_list.append(scrape_md(encoded_term))
  vedant_product = scrape_vedant(encoded_term)
  if vedant_product and len(vedant_product)>0:
    market_list.append(vedant_product)

  
  
  parse_data(market_list)
  
  
def scrape_flipkart(encoded_term):
  ua_fake = ua().random
  custom_headers = {"User-Agent":ua_fake, 
                  "Accept-Encoding":"gzip, deflate", 
                  "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                  "DNT":"1",
                  "Connection":"close", 
                  "Upgrade-Insecure-Requests":"1"}
  
  flipkart_search_url = f"https://www.flipkart.com/search?q={encoded_term}&as-show=off&as=off"
  
  try:
    flipkart_search_response = requests.get(flipkart_search_url, headers= custom_headers)
    flipkart_search_soup = BeautifulSoup(flipkart_search_response.text, 'html.parser')
    
    file_path = "flipkart_search_response.html"
    # Open the file in write mode
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(flipkart_search_soup.prettify())
        
    # matched_element = flipkart_search_soup.find('a', class_="s1Q9rs")
    matched_element = flipkart_search_soup.find('a', href=lambda href: href and "/p/" in href)
    
    flipkart_product_url = "https://www.flipkart.com" + matched_element['href']
    
    # print(flipkart_product_url)
    
    parsed_url = urlparse(flipkart_product_url)
    query_params = parse_qs(parsed_url.query)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
    flipkart_parsed_url = f'{base_url}?q={encoded_term}'
    
    if query_params.get("spotlightTagId"):
      flipkart_parsed_url += f'&spotlightTagId={query_params.get("spotlightTagId")[0]}'

    if query_params.get("qH"):
      flipkart_parsed_url += f'&qH={query_params.get("qH")[0]}'
      
      
    flipkart_product_response = requests.get(flipkart_parsed_url, headers= custom_headers)
    flipkart_product_soup = BeautifulSoup(flipkart_product_response.text, 'lxml')

    file_path = "flipkart_product_response.html"
    # Open the file in write mode
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(flipkart_product_soup.prettify())
        
    flip_product = {}
    
    flip_product["name"] = flipkart_product_soup.find("span", class_="B_NuCI").text
    flip_product["price"] = flipkart_product_soup.find("div", class_="_30jeq3 _16Jk6d").text
    flip_product["rating"] = flipkart_product_soup.find("div", class_="_3LWZlK").text
    flip_product["image"] = flipkart_product_soup.find("img", class_="_396cs4 _2amPTt _3qGmMb")['src']
    flip_product["link"] = flipkart_parsed_url
    
    return flip_product
    
    
  except Exception as e:
    st.write("Error: ", e)
  
  
def scrape_md(encoded_term):
  ua_fake = ua().random
  custom_headers = {"User-Agent":ua_fake, 
                  "Accept-Encoding":"gzip, deflate", 
                  "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                  "DNT":"1",
                  "Connection":"close", 
                  "Upgrade-Insecure-Requests":"1"}

  search_term = "rtx 3060"
  encoded_term = urllib.parse.quote_plus(search_term)

  md_search_url = f"https://mdcomputers.in/index.php?search={encoded_term}&submit_search=&route=product%2Fsearch"
  
  try:
    md_search_response = requests.get(md_search_url, headers= custom_headers)
    md_search_soup = BeautifulSoup(md_search_response.text, 'html.parser')

    file_path = "md_search_response.html"
    # Open the file in write mode
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(md_search_soup.prettify())
    
    right_block = md_search_soup.find('div', class_='right-block right-b')
    if right_block:
    # Find the h4 tag within the div
      h4_tag = right_block.find('h4')
      if h4_tag:
        a_tag = h4_tag.find('a')
        if a_tag:
          # Extract the text within the a tag
          md_product_url = a_tag['href']

        # matched_element = md_search_soup.find('div', href=lambda href: href and "/p/" in href)
    
          md_product_response = requests.get(md_product_url, headers= custom_headers)
          md_product_soup = BeautifulSoup(md_product_response.text, 'lxml')

          file_path = "md_product_response.html"
          # Open the file in write mode
          with open(file_path, 'w', encoding='utf-8') as file:
              file.write(md_product_soup.prettify())
              
              
          md_product = {}

          md_product["name"] = md_product_soup.find("span", class_="product_name").text
          md_product["price"] = md_product_soup.find("span", id="price-special").text

          rating_div = md_product_soup.find("span", class_="rating-point")
          if rating_div:
            md_product["rating"] = rating_div.text
          # md_product["rating"] = md_product_soup.find("span", class_="rating-point").text

          image_div = md_product_soup.find("div", class_="large-image")
          if image_div:
            md_product["image"] = "https:"+image_div.find("img")['src']
          # md_product["image"] = "https:"+md_product_soup.find("img", class_="large-image  ")['src']

          md_product["link"] = md_product_url
          
          return md_product
  
  except Exception as e:
    st.write("Error: ", e)


def scrape_vedant(encoded_term):
  ua_fake = ua().random
  custom_headers = {"User-Agent":ua_fake, 
                  "Accept-Encoding":"gzip, deflate", 
                  "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                  "DNT":"1",
                  "Connection":"close", 
                  "Upgrade-Insecure-Requests":"1"}

  search_term = "rtx 3060"
  encoded_term = urllib.parse.quote_plus(search_term)

  vedant_search_url = f'https://www.vedantcomputers.com/index.php?route=product/search&search={encoded_term}'

  try:
    vedant_search_response = requests.get(vedant_search_url, headers= custom_headers)
    vedant_search_soup = BeautifulSoup(vedant_search_response.text, 'html.parser')

    file_path = "vedant_search_response.html"
    # Open the file in write mode
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(vedant_search_soup.prettify())
        
    product_card = vedant_search_soup.find('div', class_='name')
    if product_card:
      # name_div = product_card.find('div', class_='name')
      a_tag = product_card.find('a')
      vedant_product_url = a_tag['href']
      
      
      vedant_product_response = requests.get(vedant_product_url, headers= custom_headers)
      vedant_product_soup = BeautifulSoup(vedant_product_response.text, 'lxml')

      file_path = "vedant_product_response.html"
      # Open the file in write mode
      with open(file_path, 'w', encoding='utf-8') as file:
          file.write(vedant_product_soup.prettify())
          
      vedant_product = {}

      vedant_product["name"] = vedant_product_soup.find("div", class_="title page-title").text
      vedant_product["price"] = vedant_product_soup.find("div", class_="product-price-new").text

      stars = vedant_product_soup.find_all('span', class_='fa fa-stack')  
      if len(stars)>0:
        vedant_product["rating"] = len(stars)
        
      img_container = vedant_product_soup.find('div', class_='swiper-slide')
      img = img_container.find('img')
      if img:
        vedant_product["image"] = img['src']
        
      vedant_product["link"] = vedant_product_url
      
      return vedant_product
    
    else:
      return {}
  
  
  except Exception as e:
    st.write("Error: ", e)
    
    
  
def parse_data(market_list):
    cols = st.columns(len(market_list), gap="large")

    for idx, col in enumerate(cols):
        product = market_list[idx]
        with col:
            st.markdown(f'<a href="{product["link"]}" target="_blank">{product["name"]}</a>', unsafe_allow_html=True)
            if "image" in product:
                st.image(product["image"], width=200)
            else:
                st.write("Image not available")
            
            if "rating" in product:
                st.write(f"Rating: {product['rating']}")
            else:
                st.write("Rating: N/A")
            
            if "price" in product:
                st.write(f"Price: {product['price']}")
            else:
                st.write("Price not available")

          
          
          
          
          
          
          
if __name__ == "__main__":
  st.set_page_config(
    page_title="Advanced Python Project" # page_icon=""
  )
  
  main()