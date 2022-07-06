from bs4 import BeautifulSoup
import requests
import re
import streamlit as st
import pandas as pd
import plotly.express as px

# To run: python3 -m streamlit run product_price_analysis.py


def newegg_search(search_term, only_search_five_pages=True):
    # In stock search_terms sold by newegg
    url = f"https://www.newegg.com/p/pl?d=${search_term}&N=4131"
    page = requests.get(url).text
    doc = BeautifulSoup(page, "html.parser")

    # Get the number of pages
    page_text = doc.find(class_="list-tool-pagination-text").strong
    pages = int(str(page_text).split("/")[-2].split(">")[-1][:-1])
    if pages >= 5 and only_search_five_pages:
        pages = 5

    items_found = []
    latest_iteration = st.empty()  # Progress Bar
    i = 0
    bar = st.progress(i)
    for page in range(1, pages+1):
        # Progress bar
        latest_iteration.text(f'Scraping newegg.com page {i+1}')
        bar.progress((i + 1)/pages)
        i += 1

        # Get the html from newegg.com using requests library and BeautifulSoup
        url = f"https://www.newegg.com/p/pl?d=${search_term}&N=4131&page={page}"
        page = requests.get(url).text
        doc = BeautifulSoup(page, "html.parser")

        div = doc.find(
            class_="item-cells-wrap border-cells items-grid-view four-cells expulsion-one-cell")
        items = div.find_all(text=re.compile(search_term))

        for item in items:
            parent = item.parent
            if parent.name != "a":
                continue

            link = parent['href']
            # Find the first parent with classname: item-container
            next_parent = item.find_parent(class_="item-container")
            try:
                price = next_parent.find(class_="price-current").strong.string
                items_found.append({"name": item, "price": int(
                    price.replace(",", "")), "link": link})
            except:
                pass

    items_found = sort_list_by_price(items_found)
    return items_found


def sort_list_by_price(item_list):
    sorted_items = sorted(item_list, key=lambda x: x['price'])
    return sorted_items


def main():
    st.title('Newegg Graphics Card Scraper')
    with st.form("my_form"):
        st.write(
            'Enter a graphics card name in the search field below to scrape newegg.com, visualize the products found in a table, then show the product price distribution in a histogram.')
        st.write('example: "3070"')
        product_name = st.text_input('Search for a product', '3070')
        scrape_5_pages = st.checkbox(
            'Only scrape the first 5 pages (more takes longer).')

        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
    
    if submitted:
        newegg_items_found = newegg_search(product_name, scrape_5_pages)
        sorted_newegg_items = sort_list_by_price(newegg_items_found)
        df = pd.DataFrame(sorted_newegg_items)

        st.write(df)
        histogram = px.histogram(df, x="price", title="Product Price Distribution")
        st.plotly_chart(histogram)    


main()
