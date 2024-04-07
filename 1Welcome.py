import streamlit as st

def main():
    st.title("Welcome to the Product Scraping and Analysis App")
    st.write(
        """
        This app allows you to search for products across multiple online stores 
        (Vedant Computers, MD Computers, and PrimeABGB) and analyze the scraped data.
        """
    )

    st.write("### How to Use:")
    st.write(
        """
        1. Navigate to the **Search Page** to search for a product by its name or ID.
        2. Once you've performed a search, the app will display the search results from various stores.
        3. You can then navigate to the **Analysis Page** to analyze the scraped data, including sorting options, summary statistics, and visualizations.
        """
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.write("### Limitations of Web Scraping:")
    st.write(
        """
        Web scraping, while a powerful tool, has its limitations and challenges:

        1. **Legal Issues:** Scraping websites without permission may violate terms of service or copyright laws, leading to legal consequences.
        
        2. **Dynamic Content:** Websites with dynamic content generated through JavaScript or AJAX may be challenging to scrape as the content may load asynchronously.

        3. **Anti-Scraping Measures:** Many websites implement anti-scraping measures to prevent automated access. This includes rate limiting, CAPTCHAs, IP blocking, and other techniques.

        4. **Data Structure Changes:** Websites frequently update their structure, which can break existing scraping scripts and require constant maintenance.

        5. **Data Quality:** Scraped data may contain errors or inconsistencies, especially if the website's HTML structure changes or if the scraper encounters unexpected data formats.

        6. **Ethical Considerations:** Scraping large amounts of data from a website can put strain on its servers, potentially causing disruptions or impacting the user experience for other visitors.

        """
    )
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.write("###### Stores Used:")
    col1, col2, col3 = st.columns(3)
    col1.markdown("[Vedant Computers](https://www.vedantcomputers.com)")
    col2.markdown("[PrimeABGB](https://www.primeabgb.com)")
    col3.markdown("[MD Computers](https://www.mdcomputers.in)")
if __name__ == "__main__":
    main()
