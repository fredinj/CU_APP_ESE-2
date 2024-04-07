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

    st.write("### Get Started:")
    st.write("Use the sidebar to navigate between the Search and Analysis pages.")

if __name__ == "__main__":
    main()
