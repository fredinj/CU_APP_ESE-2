import streamlit as st
import requests
import urllib.parse
from bs4 import BeautifulSoup
from fake_useragent import UserAgent as ua
from urllib.parse import urlparse, parse_qs
import re
import pandas as pd
from time import sleep
# import math

# adjustable search number limit on sidebar
# save for analysis button
# make analysis
# sort products based on price
#  maybe (scatter) plots based on price and different colors for different stores
 
 
  
def main():
  st.title("Search for your product name or ID")

  st.sidebar.header("Settings")
  item_count = st.sidebar.slider("Number of Products to Display", min_value=1, max_value=6, value=4)
  
  scrape_results={}

  search_term = st.text_input("Search")
  if st.button("Search"):  
    if len(search_term.strip()) != 0:
      with st.spinner('Loading data...'):
        # sleep(5)  # Sleep for 1 second
        scrape_results = scrape_markets(search_term.strip(), item_count)
        
        parse_data(scrape_results)
        
    else:
      st.error("Enter a valid search term")
      


def scrape_markets(search_term, item_count):
  
  # get from setup later
  # item_count = 4  
  
  encoded_term = urllib.parse.quote_plus(search_term)
  
  scrape_results={}
  
  # flip_product = scrape_flipkart(encoded_term)
  # if flip_product and len(flip_product)>0:
  #   market_list.append(flip_product)
  
  # md_product = scrape_md(encoded_term)
  # if md_product and len(md_product)>0:  
  #   market_list.append(md_product)
  
  vendant_list = scrape_vedant(encoded_term, item_count)
  if vendant_list and len(vendant_list)>0:
    scrape_results['vedant'] = vendant_list
    
  md_list = scrape_md(encoded_term, item_count)
  if md_list and len(md_list)>0:
    scrape_results['md'] = md_list
    
  prime_list = scrape_prime(encoded_term, item_count)
  if prime_list and len(prime_list)>0:
    scrape_results['prime'] = prime_list

  return scrape_results
  
  
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
    
    if matched_element:
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
  

def scrape_md(encoded_term, item_count):
  ua_fake = ua().random
  custom_headers = {"User-Agent":ua_fake, 
                  "Accept-Encoding":"gzip, deflate", 
                  "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                  "DNT":"1",
                  "Connection":"close", 
                  "Upgrade-Insecure-Requests":"1"}

  md_search_url = f"https://mdcomputers.in/index.php?search={encoded_term}&submit_search=&route=product%2Fsearch"
  
  try:
    md_search_response = requests.get(md_search_url, headers= custom_headers)
    md_search_soup = BeautifulSoup(md_search_response.text, 'html.parser')

    file_path = "md_search_response.html"
    # Open the file in write mode
    with open(file_path, 'w', encoding='utf-8') as file:
      file.write(md_search_soup.prettify())
      
    products_container_list = md_search_soup.find('div', class_="products-list")
    if not products_container_list:
      return []

    products_list_inner = products_container_list.find_all('div', class_="product-layout", recursive=False)

    products_list_inner = [i.find('div', class_="product-item-container", recursive=False) for i in products_list_inner]
  
  
    products_list=[]

    for i in products_list_inner:
      product={}
      
      product['name'] = i.find('div', class_="right-block").find('h4').find('a').text.strip()
      product['link'] = i.find('div', class_="right-block").find('h4').find('a')['href']
      product['price'] = i.find('div', class_='right-block').find('div', class_="price").find('span').text.strip()
      
      if i.find('div', class_="left-block").find('div', class_='product-image-container').find('a').find('img').has_attr('data-src'):
        product['image'] = "https:" + i.find('div', class_="left-block").find('div', class_='product-image-container').find('a').find('img')['data-src']
      elif i.find('div', class_="left-block").find('div', class_='product-image-container').find('a').find('img').has_attr('src'):
        product['image'] = "https:" + i.find('div', class_="left-block").find('div', class_='product-image-container').find('a').find('img')['src']
      else:
        product['image'] = ""
      
      products_list.append(product)
      
      if len(products_list) >= item_count:
        break
    
    return products_list
  
  except Exception as e:
    st.write("Error: ", e)
  

def scrape_vedant(encoded_term, item_count):  
  ua_fake = ua().random
  custom_headers = {"User-Agent":ua_fake, 
                  "Accept-Encoding":"gzip, deflate", 
                  "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                  "DNT":"1",
                  "Connection":"close", 
                  "Upgrade-Insecure-Requests":"1"}

  vedant_search_url = f'https://www.vedantcomputers.com/index.php?route=product/search&search={encoded_term}'

  try:
    vedant_search_response = requests.get(vedant_search_url, headers= custom_headers)
    vedant_search_soup = BeautifulSoup(vedant_search_response.text, 'html.parser')

    file_path = "vedant_search_response.html"
    # Open the file in write mode
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(vedant_search_soup.prettify())
        
    main_products_wrapper = vedant_search_soup.find('div', class_='main-products-wrapper')
    p_tag = main_products_wrapper.find('p')
    if p_tag:
      if p_tag.text == "There is no product that matches the search criteria.":
        return []
        # print("no product found")  

    else:
      
      product_grid = vedant_search_soup.find('div', class_="main-products product-grid")
      if product_grid:
        product_div = product_grid.find_all('div', class_='product-layout has-extra-button')
          
      products_list = []
      for i in product_div:
        product = {}
        product["name"] = i.find('div', class_='product-thumb').find('div', class_='caption').find('div', class_="name").find('a').text.strip()
        
        if i.find('div', class_='product-thumb').find('div', class_='caption').find('div', class_="price").find('span', class_="price-new"):
          product["price"] = i.find('div', class_='product-thumb').find('div', class_='caption').find('div', class_="price").find('span', class_="price-new").text.strip()
        elif i.find('div', class_='product-thumb').find('div', class_='caption').find('div', class_="price").find('span', class_="price-normal"):
          product["price"] = i.find('div', class_='product-thumb').find('div', class_='caption').find('div', class_="price").find('span', class_="price-normal").text.strip()
        else:
          product["price"] = "N/A"
          
        product["link"] = i.find('div', class_='product-thumb').find('div', class_='caption').find('div', class_="name").find('a')['href']
        
        img_src_set = i.find('div', class_='product-thumb').find('div', class_='image').find('a', class_="product-img").find('div').find('img')['data-srcset']
        srcset_parts = img_src_set.split(', ')
        if '2x' in srcset_parts[1]:
          url, resolution = srcset_parts[1].split(' ')
        else:
          url = i.find('div', class_='product-thumb').find('div', class_='image').find('a', class_="product-img").find('div').find('img')['data-src']
        product["image"] = url
        
        products_list.append(product)
        
        if len(products_list) >= item_count:
          break
      
      return products_list
  
  
  except Exception as e:
    st.write("Error: ", e)
    

def scrape_prime(encoded_term, item_count):
  ua_fake = ua().random
  custom_headers = {"User-Agent":ua_fake, 
                  "Accept-Encoding":"gzip, deflate", 
                  "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                  "DNT":"1",
                  "Connection":"close", 
                  "Upgrade-Insecure-Requests":"1"}

  prime_search_url = f'https://www.primeabgb.com/?s={encoded_term}&post_type=product'

  try:
    prime_search_response = requests.get(prime_search_url, headers= custom_headers)
    prime_search_soup = BeautifulSoup(prime_search_response.text, 'html.parser')

    file_path = "prime_search_response.html"
    # Open the file in write mode
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(prime_search_soup.prettify())
        
    site_wrapper = prime_search_soup.find('div', class_='site-wrapper')

    primary_div = site_wrapper.find('div', id='main-content').find('div', class_='container').find('div', class_='row').find('div', id="primary")

    if primary_div.find('div', class_="bapf_no_products"):
      return []

    products_grid = primary_div.find('div', class_="products", recursive=False).find_all('div', class_="product", recursive=False)

    products_list = []

    for i in products_grid:
      product = {}
      product['name'] = i.find('div', class_="product-wrapper").find('div', class_="product-info").find("div", class_="product-title-rating").find("h3", class_="product-title").find('a').text.strip()
      product['link'] = i.find('div', class_="product-wrapper").find('div', class_="product-info").find("div", class_="product-title-rating").find("h3", class_="product-title").find('a')['href']
      
      
      if i.find('div', class_="product-wrapper").find('div', class_="product-info").find("div", class_="product-price-buttons").find('div', class_="product-price").find('span', class_="woocommerce-Price-amount amount"):
        product['price'] = i.find('div', class_="product-wrapper").find('div', class_="product-info").find("div", class_="product-price-buttons").find('div', class_="product-price").find('span', class_="woocommerce-Price-amount amount").find('bdi').text.strip()
      else:
        product['price'] = "N/A"
      
      product['image'] = i.find('div', class_="product-wrapper").find('div', class_="product-image").find('a').find('img')['src']
      
      products_list.append(product)
      
      if len(products_list) >= item_count:
        break
      
    return products_list
  
  except Exception as e:
    st.write("Error: ", e)


def card(product, col):
    content = f"""
    <div class="product-card" style="margin: 20px;">
        <img src="{product['image']}" alt="Product Image">
        <div class="product-details">
            <h2><a href="{product['link']}">{product['name']}</a></h2>
            <p class="price">{product['price']}</p>
        </div>
    </div>
    """
    col.markdown(content, unsafe_allow_html=True)
 

def parse_data(scrape_results):
  items_per_row = 2
  item_count = 0

  vedant_expander = st.expander("Vedant Computers", expanded=True)
  with vedant_expander:
    # st.markdown("---")
    if 'vedant' in scrape_results:
      for i in range(0, len(scrape_results['vedant']), items_per_row):
        with st.container():
          vedant_col = st.columns(items_per_row)
          for j in range(items_per_row):
            if i + j < len(scrape_results['vedant']):
              card(scrape_results['vedant'][i + j], vedant_col[j])
              item_count += 1
              if item_count >= 2:
                # st.markdown("""<div style="margin-bottom: 20px;"></div>""", unsafe_allow_html=True)
                item_count = 0
    else:
        st.error("No products found on Vedant Computers")
        
        
  md_expander = st.expander("MD Computers", expanded=True)
  with md_expander:
    # st.markdown("---")
    if 'md' in scrape_results:
      for i in range(0, len(scrape_results['md']), items_per_row):
        with st.container():
          md_col = st.columns(items_per_row)
          for j in range(items_per_row):
            if i + j < len(scrape_results['md']):
              card(scrape_results['md'][i + j], md_col[j])
              item_count += 1
              if item_count >= 2:
                # st.markdown("""<div style="margin-bottom: 20px;"></div>""", unsafe_allow_html=True)
                item_count = 0
    else:
        st.error("No products found on MD Computers")

  
  prime_expander = st.expander("PrimeABGB", expanded=True)
  with prime_expander:
    # st.markdown("---")
    if 'prime' in scrape_results:
      for i in range(0, len(scrape_results['prime']), items_per_row):
        with st.container():
          prime_col = st.columns(items_per_row)
          for j in range(items_per_row):
            if i + j < len(scrape_results['prime']):
              card(scrape_results['prime'][i + j], prime_col[j])
              item_count += 1
              if item_count >= 2:
                # st.markdown("""<div style="margin-bottom: 20px;"></div>""", unsafe_allow_html=True)
                item_count = 0
    else:
        st.error("No products found on PrimeABGB")
          
  all_products = []

  for source, products in scrape_results.items():
      for product in products:
          product['source'] = source
          all_products.append(product)

  # Save the DataFrame to a CSV file
  df = pd.DataFrame(all_products)
  df.to_csv('scraped_data.csv', index=False)
  st.sidebar.success("Data saved for analysis")
  



if __name__ == "__main__":
  st.set_page_config(
    page_title="Advanced Python Project" # page_icon=""
  )
  st.markdown(
  """
  <style>
    .product-card {
      border: 1px solid #ccc;
      border-radius: 8px;
      padding: 10px;
      box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
      width: 250px; /* Fixed width */
      height: auto; /* Allow height to adjust based on content */
      margin: 0 auto; /* Center the card */
      overflow: hidden; /* Ensure contents don't overflow */
      display: flex; /* Use flexbox for layout */
      flex-direction: column; /* Stack child elements vertically */
    }

    .product-card img {
      max-width: 100%;
      height: auto;
      border-radius: 8px;
      flex-shrink: 0; /* Prevent image from shrinking */
    }

    .product-details {
      flex-grow: 1; /* Allow details to expand to fill remaining space */
      text-align: center;
    }

    .product-details h2 {
      margin: 10px 0;
      font-size: 1.2em;
    }

    .product-details a {
      text-decoration: none;
      color: #c5cbc9;
    }

    .product-details a:hover {
      color: #007bff;
    }

    .product-details p.price {
      font-size: 1.1em;
      color: #2d86c5;
      margin: 5px 0;
    }
  </style>
  """,
  unsafe_allow_html=True
  )
  
  main()