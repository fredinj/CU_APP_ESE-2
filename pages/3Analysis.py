import pandas as pd
import streamlit as st
import re
import altair as alt

def clean_price(price):
    # Remove currency symbol and commas
    price = re.sub('[₹,]', '', price)
    # Convert to float
    return float(price)

def preprocess_store(store_name):
    # Dictionary mapping original store names to new names
    store_mapping = {'md': 'MD Computers', 'vedant': 'Vedant Computers', 'prime': 'PrimeABGB'}
    # Return the new name if found, otherwise return the original name
    return store_mapping.get(store_name, store_name)

def main():
    df = pd.read_csv('scraped_data.csv')
    
    # Preprocess store names
    df['source'] = df['source'].apply(preprocess_store)

    # Sorting options
    sort_options = ['None', 'Sort by Price (ascending)', 'Sort by Price (descending)', 'Sort by Source']
    default_sort_option = 'Sort by Price (ascending)'  # Set default sorting option
    sort_option = st.selectbox("Select sorting option:", sort_options, index=sort_options.index(default_sort_option))

    if sort_option == 'Sort by Price (ascending)' or sort_option == 'Sort by Price (descending)':
        df['price'] = df['price'].apply(clean_price)  # Clean the 'price' column

    if sort_option == 'Sort by Price (ascending)':
        df_sorted = df.sort_values(by='price', ascending=True)
    elif sort_option == 'Sort by Price (descending)':
        df_sorted = df.sort_values(by='price', ascending=False)
    elif sort_option == 'Sort by Source':
        df_sorted = df.sort_values(by='source')
    else:
        df_sorted = df.copy()  # Assigning original DataFrame when sorting option is 'None'

    st.write("Sorted DataFrame:")
    st.write(df_sorted)

    st.markdown("---")

    # Checkbox for showing summary
    show_summary = st.checkbox("Show Summary")

    if show_summary:
        st.write("Summary:")
        # Display highest priced product and store
        highest_priced_product = df_sorted.loc[df_sorted['price'].idxmax()]
        st.markdown("**Highest Priced Product:** " + highest_priced_product['name'])
        st.markdown("**Price:** " + str(highest_priced_product['price']))
        st.markdown("**Store:** " + highest_priced_product['source'])

        # Display lowest priced product and store
        lowest_priced_product = df_sorted.loc[df_sorted['price'].idxmin()]
        st.markdown("**Lowest Priced Product:** " + lowest_priced_product['name'])
        st.markdown("**Price:** " + str(lowest_priced_product['price']))
        st.markdown("**Store:** " + lowest_priced_product['source'])



        st.markdown("---")

        # Scatter plot
        scatter_data = pd.DataFrame(columns=['x', 'y', 'Product', 'Store'])
        colors = {'MD Computers': 'red', 'Vedant Computers': 'blue', 'PrimeABGB': 'green'}
        dfs = []  # list to hold all temporary dataframes
        for store in df['source'].unique():
            data = df[df['source'] == store]
            temp_df = pd.DataFrame({
                'x': data.index.tolist(),
                'y': data['price'].tolist(),
                'Product': data['name'].tolist(),
                'Store': [store]*len(data)
            })
            dfs.append(temp_df)  # append the temporary dataframe to the list
        scatter_data = pd.concat(dfs, ignore_index=True)  # concatenate all dataframes in the list
        
        # Create the scatter plot using Altair
        chart = alt.Chart(scatter_data).mark_circle(size=150).encode(
            x=alt.X('x:Q', axis=alt.Axis(title='Product')),  # Set x-axis label as "Product"
            y=alt.Y('y:Q', axis=alt.Axis(title='Price')),  # Set y-axis label as "Price"
            color=alt.Color('Store:N', scale=alt.Scale(domain=list(colors.keys()), range=list(colors.values()))),  # color encoding for stores
            tooltip=['Product', 'x', 'y']  # tooltip with product name, x, and y values
        ).properties(
            width=600,
            height=400
        )

        st.write("Scatter plot:")
        st.altair_chart(chart, use_container_width=True)

if __name__ == '__main__':
    main()
