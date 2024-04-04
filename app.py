import streamlit as st
import requests
import urllib.parse
from bs4 import BeautifulSoup
from fake_useragent import UserAgent as ua
from urllib.parse import urlparse, parse_qs
# from time import sleep
  
 
 
  
def main():
  st.title("Search for your product name or ID")

  search_term = st.text_input("Search")
  if st.button("Search"):  
    if len(search_term.strip()) != 0:
      with st.spinner('Loading data...'):
        # sleep(5)  # Sleep for 1 second
        scrape_market(search_term.strip())
    else:
      st.error("Enter a valid search term")
    
  
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
  
  
def scrape_md(encoded_term):
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
    
    product_image_container = md_search_soup.find('div', class_='product-image-container')
    if product_image_container:
      a_tag = product_image_container.find('a')
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

        md_product["name"] = md_product_soup.find("span", class_="more_show")["data-full_title"]
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
    else:
      return {}
  
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
        else:
          product["price"] = i.find('div', class_='product-thumb').find('div', class_='caption').find('div', class_="price").find('span', class_="price-normal").text.strip()
        product["link"] = i.find('div', class_='product-thumb').find('div', class_='caption').find('div', class_="name").find('a')['href']
        
        img_src_set = i.find('div', class_='product-thumb').find('div', class_='image').find('a', class_="product-img").find('div').find('img')['data-srcset']
        srcset_parts = img_src_set.split(', ')
        if '2x' in srcset_parts[1]:
          url, resolution = srcset_parts[1].split(' ')
        else:
          url = i.find('div', class_='product-thumb').find('div', class_='image').find('a', class_="product-img").find('div').find('img')['data-src']
        product["image"] = url
        
        products_list.append(product)
        
        if len(products_list) >= 2:
          break
      
      return products_list
  
  
  except Exception as e:
    st.write("Error: ", e)
    

def card(product, col):
    content = f"""
    <div class="product-card">
        <img src="{product['image']}" alt="Product Image">
        <div class="product-details">
            <h2><a href="{product['link']}">{product['name']}</a></h2>
            <p class="price">{product['price']}</p>
        </div>
    </div>
    """
    col.markdown(content, unsafe_allow_html=True)


def scrape_market(search_term):
  
  encoded_term = urllib.parse.quote_plus(search_term)
  
  scrape_results={}
  
  # flip_product = scrape_flipkart(encoded_term)
  # if flip_product and len(flip_product)>0:
  #   market_list.append(flip_product)
  
  # md_product = scrape_md(encoded_term)
  # if md_product and len(md_product)>0:  
  #   market_list.append(md_product)
  
  vendant_list = scrape_vedant(encoded_term)
  if vendant_list and len(vendant_list)>0:
    scrape_results['vedant'] = vendant_list

  
  parse_data(scrape_results)
  

def parse_data(scrape_results):
    vedant_expander = st.expander("Vedant Computers", expanded=True)
    with vedant_expander:
      if 'vedant' in scrape_results:
        vedant_col = st.columns(2)
        for i in range(len(scrape_results['vedant'])):
            card(scrape_results['vedant'][i], vedant_col[i])
        st.markdown("""<div style="margin-bottom: 20px;"></div>""", unsafe_allow_html=True)
      else:
        st.error("No products found on Vedant Computers")



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