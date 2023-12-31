from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np
import regex as re
import plotly.graph_objs as go

# Step 1: Parse the HTML File
with open("results.html", "r") as file:
    soup = BeautifulSoup(file, "lxml")

listings = []

# Base URL
base_url = "https://www.carfax.com"

# Step 2: Extract Information
for div in soup.find_all("div", class_="srp-listing-content"):
    for article in soup.find_all("article", class_="srp-list-item"):
        #print("=========================================")
        #print("Article:")
        #print(article.prettify())

        # Extract the VIN
        vin = article["data-vin"]

        # Locate the Header Tag and Extract Title and Link
        header = article.find("header", class_="srp-list-item__header")
        if header:
            link_tag = header.find("a", href=True)
            title = link_tag.get_text(strip=True)
            #link = link_tag['href']
            # Concatenate with base URL if the link is relative
            #if not link.startswith("http"):
            #    link = base_url + link
            link = base_url + "/vehicle/" + vin

        else:
            title, link = None, None
            print("ERROR: no title or tag found")

        # Locate the Price Tag and Extract Price
        price_tag = article.find("div", class_="srp-list-item__price srp-list-item__section")
        if price_tag:
            price_tag = price_tag.get_text(strip=True).replace('Price:', '')
            if "$" in price_tag:
                price_tag = price_tag.split("$")
                price = int(price_tag[1].replace(',', ''))  # Remove commas for a clean number
            else:
                price = price_tag
        else:
            price = None
            print("ERROR: no price tag found")
        
        # Locate the Accident Tag and Extract Accident
        accident_tag = article.find("span", class_="title title--noAccident")
        if accident_tag:
            has_accident = False
            has_damage = False
            condition = accident_tag.get_text(strip=True)
            condition_lower = condition.lower()
            print(condition)
            if "no " not in condition_lower:
                if "accident" in condition_lower:
                    has_accident = True
                if "damage" in condition_lower:
                    has_damage = True
        else:
            print("ERROR: no accident tag found")
            condition = None
            has_accident, has_damage = False, False

        # Locate the Mileage Tag and Extract Mileage
        mileage = None
        for info_tag in article.find_all("span", class_="srp-list-item__basic-info-value"):
            info_tag = info_tag.get_text(strip=True)
            if "Mileage" in info_tag:
                # Use regex to extract only the number from the mileage string
                mileage_match = re.search(r'\d[\d,]*', info_tag)
                if mileage_match:
                    mileage = int(mileage_match.group().replace(',', ''))  # Remove commas for a clean number
                break
            
        if mileage == None:
            print("ERROR: no mileage tag found")

        # Inside your loop for extracting listing information
        image_div = article.find("div", class_="srp-list-item__image")
        if image_div:
            image_tag = image_div.find("img")
            if image_tag and 'src' in image_tag.attrs:
                image_url = image_tag['src']
            else:
                print("ERROR: no image tag found")
                image_url = "https://static.carfax.com/uclassets/images/srp-noimage.webp"  # Use a default image if no img tag is found
        else:
            print("ERROR: no image div found")
            image_url = "https://static.carfax.com/uclassets/images/srp-noimage.webp"  # Use a default image if no image div is found



        # Store the Extracted Information
        listing_info = {
            'VIN': vin,
            'Title': title,
            'Price': price,
            'Mileage': mileage,
            'Has_Accident': has_accident,
            'Has_Damage': has_damage,
            'Condition': condition,
            'URL': link,
            'Image_URL': image_url
        }
        listings.append(listing_info)

# Now you have a list of dictionaries with each car's details
#print(listings)

# Step 3: Run a linear regression on the listings
# Filter out entries without numeric price and convert price and mileage to numeric values
filtered_listings = []
for entry in listings:
    if type(entry['Price']) == int:  # Check if the price is numeric
        filtered_listings.append(entry)

    if entry['Has_Accident'] == True:
        print(entry)

# Separate listings into two groups: with accidents and without accidents
listings_with_accidents = [d for d in filtered_listings if d['Has_Accident'] == True]
listings_without_accidents = [d for d in filtered_listings if d['Has_Accident'] == False]

# Prepare data for linear regression
def prepare_data(data):
    X = np.array([d['Mileage'] for d in data]).reshape(-1, 1)  # Mileage
    y = np.array([d['Price'] for d in data])  # Price
    return X, y

X_with_accidents, y_with_accidents = prepare_data(listings_with_accidents)
X_without_accidents, y_without_accidents = prepare_data(listings_without_accidents)

# Perform linear regression
model_with_accidents = LinearRegression().fit(X_with_accidents, y_with_accidents)
model_without_accidents = LinearRegression().fit(X_without_accidents, y_without_accidents)

# Get the coefficients
coef_with_accidents = model_with_accidents.coef_[0]
coef_without_accidents = model_without_accidents.coef_[0]

print("Coefficient for cars with accidents:", coef_with_accidents)
print("Coefficient for cars without accidents:", coef_without_accidents)

# Get the intercepts
intercept_with_accidents = model_with_accidents.intercept_
intercept_without_accidents = model_without_accidents.intercept_

print("Intercept for cars with accidents:", intercept_with_accidents)
print("Intercept for cars without accidents:", intercept_without_accidents)

# Step 4: Plot the data using plotly to generate an interactive scatterplot visualization

def create_scatter_trace(listings, name, color):
    x = [listing['Mileage'] for listing in listings]
    y = [listing['Price'] for listing in listings]
    text = [f"<strong>listing['Title']</strong><br>Price: {listing['Price']}<br>Mileage: {listing['Mileage']}<br>Condition: {listing['Condition']}<br>VIN: {listing['VIN']}<br>URL: {listing['URL']}" for listing in listings]
    return go.Scatter(x=x, y=y, mode='markers', name=name, marker_color=color, text=text, hoverinfo='text')

# Create scatter traces
trace_with_accidents = create_scatter_trace(listings_with_accidents, 'With Accidents', 'red')
trace_without_accidents = create_scatter_trace(listings_without_accidents, 'Without Accidents', 'blue')

# Get the overall range of mileage
all_mileage = [listing['Mileage'] for listing in listings_with_accidents + listings_without_accidents]
min_mileage = min(all_mileage)
max_mileage = max(all_mileage)
x_range = np.linspace(min_mileage, max_mileage, 100)

# Create lines of best fit
line_with_accidents = go.Scatter(x=x_range, y=model_with_accidents.intercept_ + model_with_accidents.coef_[0] * x_range, mode='lines', name='Best Fit With Accidents', line=dict(color='red', dash='dash'))
line_without_accidents = go.Scatter(x=x_range, y=model_without_accidents.intercept_ + model_without_accidents.coef_[0] * x_range, mode='lines', name='Best Fit Without Accidents', line=dict(color='blue', dash='dash'))

# Combine traces
data = [trace_with_accidents, trace_without_accidents, line_with_accidents, line_without_accidents]

# Create layout
layout = go.Layout(title='Car Listings: Mileage vs Price', xaxis=dict(title='Mileage'), yaxis=dict(title='Price'), hovermode='closest')

# Create figure and plot
fig = go.Figure(data=data, layout=layout)
fig.show()