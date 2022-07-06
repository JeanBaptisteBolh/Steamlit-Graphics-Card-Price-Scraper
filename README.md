# Steamlit-Graphics-Card-Price-Scraper
This project opens a streamlit session which prompts the user to enter the name of a graphics card.  It then scrapes newegg.com for price info for the graphics card and displays the price variation in a histogram using plotly/streamlit.

To run:

1. Install poetry by following these intructions: 
https://python-poetry.org/docs/

2. Clone this repository by running the following command:
```git clone https://github.com/JeanBaptisteBolh/Steamlit-Graphics-Card-Price-Scraper.git```

3. Navigate to the now cloned project in terminal.

4. Install project dependencies by running:
```poetry install```

5. Enter the project virtual environment shell:
```poetry shell```

6. Finally, run this command to run the project.  This will open a browser window/tab:
```python3 -m streamlit run product_price_analysis.py```
