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
    return store_mapping.get(store_name, store_name)

def main():
    df = pd.read_csv('scraped_data.csv')
    
    # Preprocess store names
    df['source'] = df['source'].apply(preprocess_store)
    df['price'] = df['price'].apply(clean_price)

    sort_options = ['None', 'Sort by Price (ascending)', 'Sort by Price (descending)', 'Sort by Source']
    default_sort_option = 'None'
    sort_option = st.selectbox("Select sorting option:", sort_options, index=sort_options.index(default_sort_option))

    if sort_option == 'Sort by Price (ascending)':
        df_sorted = df.sort_values(by='price', ascending=True)
    elif sort_option == 'Sort by Price (descending)':
        df_sorted = df.sort_values(by='price', ascending=False)
    elif sort_option == 'Sort by Source':
        df_sorted = df.sort_values(by='source')
    else:
        df_sorted = df.copy()

    st.write("Sorted DataFrame:")
    st.write(df_sorted)

    st.markdown("---")

    show_summary = st.checkbox("Show Summary")

    if show_summary:
        st.write("Summary:")
        highest_priced_product = df_sorted.loc[df_sorted['price'].idxmax()]
        st.markdown("**Highest Priced Product:** " + highest_priced_product['name'])
        st.markdown("**Price:** " + str(highest_priced_product['price']))
        st.markdown("**Store:** " + highest_priced_product['source'])

        lowest_priced_product = df_sorted.loc[df_sorted['price'].idxmin()]
        st.markdown("**Lowest Priced Product:** " + lowest_priced_product['name'])
        st.markdown("**Price:** " + str(lowest_priced_product['price']))
        st.markdown("**Store:** " + lowest_priced_product['source'])

        st.markdown("---")

        # Scatter plot        
        scatter_data = pd.DataFrame(columns=['x', 'y', 'Product', 'Store'])
        colors = {'MD Computers': 'red', 'Vedant Computers': 'blue', 'PrimeABGB': 'green'}
        dfs = []  
        for store in df['source'].unique():
            data = df[df['source'] == store]
            temp_df = pd.DataFrame({
                'x': data.index.tolist(),
                'y': data['price'].tolist(),
                'Product': data['name'].tolist(),
                'Store': [store]*len(data)
            })
            dfs.append(temp_df)  
        scatter_data = pd.concat(dfs, ignore_index=True) 
        
        chart = alt.Chart(scatter_data).mark_circle(size=150).encode(
            x=alt.X('x:Q', axis=alt.Axis(title='Product')),  
            y=alt.Y('y:Q', axis=alt.Axis(title='Price')),  
            color=alt.Color('Store:N', scale=alt.Scale(domain=list(colors.keys()), range=list(colors.values()))),  
            tooltip=['Product', 'x', 'y']  
        ).properties(
            width=600,
            height=400
        )

        st.write("Scatter plot:")
        st.altair_chart(chart, use_container_width=True)

if __name__ == '__main__':
    main()