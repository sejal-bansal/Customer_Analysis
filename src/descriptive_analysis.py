# -*- coding: utf-8 -*-
"""Descriptive Analysis.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1WmtQ0IdhaW27lHyxSqWkrdJG1LXDf-Ha

# Descriptive Analysis of Customer Purchase Attributes

This notebook conducts a detailed descriptive analysis of customer attributes to uncover patterns and trends in the dataset. These insights will serve as a foundation for customer segmentation and product recommendation tasks in subsequent notebooks.

Key steps in this notebook include:
- Analyzing demographic and physical attributes (e.g., age, size, body type).
- Identifying trends in preferences, such as favorite colors.
- Generating summary statistics and visualizations for better understanding.

# Dataset Overview


The analysis in this notebook utilizes four key datasets, each contributing essential information about customers, products, orders, and reviews. Below is a detailed description of each dataset:

## 1. Customer Dataset (`customer.csv`)
- **Description**: Contains demographic and physical attributes of customers.
- **Key Columns**:
  - `user_id`: Unique identifier for each customer.
  - `user_age`: Age of the customer.
  - `user_color`: Customer's favorite color.
  - `user_size`: Preferred clothing size.
  - `user_body_type`: Customer's body type (e.g., hourglass, apple).
  - `user_height`: Height of the customer (converted to inches for analysis).
  - `user_weight`: Weight of the customer (cleaned and converted to numeric format).

## 2. Product Dataset (`product.csv`)
- **Description**: Provides details about the products available for purchase.
- **Key Columns**:
  - `product_id`: Unique identifier for each product.
  - `product_name`: Name of the product.
  - `category`: Product category (e.g., dresses, sweaters, skirts).
  - `price`: Price of the product.
  - `rating`: Average customer rating for the product.

## 3. Order Dataset (`order.csv`)
- **Description**: Includes details about customer orders and purchases.
- **Key Columns**:
  - `order_id`: Unique identifier for each order.
  - `customer_id`: ID of the customer who placed the order.
  - `product_id`: ID of the purchased product.
  - `order_date`: Date the order was placed.
  - `paid_amt`: Total amount paid for the order.

## 4. Reviews Dataset (`reviews.csv`)
- **Description**: Contains feedback provided by customers for their purchased products.
- **Key Columns**:
  - `review_id`: Unique identifier for each review.
  - `product_id`: ID of the product being reviewed.
  - `customer_id`: ID of the customer who wrote the review.
  - `review_content`: The text content of the review.
  - `star_rating`: The rating provided by the customer (e.g., 1-5 stars).
  - `review_date`: Date when the review was submitted.

## Relationships Between Datasets
- **Customer Dataset**: Provides demographic and physical attributes used for segmentation and preference analysis.
- **Product Dataset**: Offers insights into product popularity and customer preferences based on categories and ratings.
- **Order Dataset**: Links customers to their purchase history and enables analysis of spending patterns, seasonal trends, and customer behavior.
- **Reviews Dataset**: Adds qualitative and quantitative feedback, helping to evaluate customer sentiment and identify product satisfaction levels.

This combination of datasets forms the foundation for deriving insights into customer demographics, product preferences, purchasing behaviors, and customer feedback.
"""

import pandas as pd

customer_df = pd.read_csv('./data/processed/customer.csv')
total_customers = len(customer_df)
print(f"Total customers: {total_customers}")

#Check for unique values in each column
unique_values = customer_df.nunique()
print("\nUnique values in each column:")
print(unique_values)

"""# Color Preferences Analysis
This section examines customer preferences for colors:
- The most and least popular colors are identified.
- Trends in color preferences across different customer segments are explored.

"""

#Color preferences analysis
color_preferences = customer_df['user_color'].value_counts()
print("\nColor Preferences:")
print(color_preferences)

"""# Size Distribution
This section analyzes the distribution of clothing sizes preferred by customers:
- Provides a breakdown of the most commonly selected sizes.
- Identifies outliers or unusual patterns in size preferences.

"""

#User size distribution
size_distribution = customer_df['user_size'].value_counts()
print("\nUser Size Distribution:")
print(size_distribution)

"""# Body Type Analysis
This section reviews the distribution of customer body types:
- Highlights the most frequent body types in the dataset.
- Provides insights into potential product tailoring opportunities.

"""

#Body type distribution
body_type_distribution = customer_df['user_body_type'].value_counts()
print("\nUser Body Type Distribution:")
print(body_type_distribution)

"""# Age Analysis
This section focuses on customer age distribution:
- Calculates summary statistics (e.g., mean, median, standard deviation).
- Visualizes the age distribution to identify trends (e.g., age groups that dominate the dataset).

"""

import plotly.express as px
import plotly.graph_objects as go


# Ensure 'user_age' is numeric
customer_df['user_age'] = pd.to_numeric(customer_df['user_age'], errors='coerce')

# Summary Statistics for 'user_age'
age_stats = customer_df['user_age'].describe()
print("Summary Statistics for 'user_age':")
print(age_stats)

# Visualize Age Distribution using a Histogram
hist_fig = px.histogram(
    customer_df,
    x='user_age',
    title='Age Distribution of Customers',
    labels={'user_age': 'Age'},
    nbins=20,
    template='plotly_white'
)
hist_fig.update_layout(xaxis_title='Age', yaxis_title='Count')
hist_fig.show()

"""# Results and Insights
This section summarizes the findings from the descriptive analysis:
- Key trends in customer preferences (e.g., popular colors, sizes, body types).
- Demographic insights (e.g., age group trends).
- Implications for product design and marketing strategies.

"""

# Convert 'user_height' from format 5'7" to inches
def height_to_inches(height):
    if isinstance(height, str) and "'" in height:
        feet, inches = height.split("'")
        feet = int(feet.strip())
        inches = int(inches.replace('"', '').strip()) if inches else 0
        return feet * 12 + inches
    return None

customer_df['user_height'] = customer_df['user_height'].apply(height_to_inches)
customer_df['user_weight'] = pd.to_numeric(customer_df['user_weight'].str.replace(' lbs.', ''), errors='coerce')

# Summary Statistics for 'user_height' and 'user_weight'
height_stats = customer_df['user_height'].describe()
weight_stats = customer_df['user_weight'].describe()
print("Summary Statistics for 'user_height':")
print(height_stats)
print("\nSummary Statistics for 'user_weight':")
print(weight_stats)

# Visualize Height Distribution
height_hist_fig = px.histogram(
    customer_df,
    x='user_height',
    title='Height Distribution of Customers',
    labels={'user_height': 'Height (in inches)'},
    nbins=20,
    template='plotly_white'
)
height_hist_fig.update_layout(xaxis_title='Height (in inches)', yaxis_title='Count')
height_hist_fig.show()

# Visualize Weight Distribution
weight_hist_fig = px.histogram(
    customer_df,
    x='user_weight',
    title='Weight Distribution of Customers',
    labels={'user_weight': 'Weight (in lbs)'},
    nbins=20,
    template='plotly_white'
)
weight_hist_fig.update_layout(xaxis_title='Weight (in lbs)', yaxis_title='Count')
weight_hist_fig.show()

""" **User Size Distribution Bar Chart**:
   - Compares the frequency of preferred clothing sizes, sorted by popularity.
"""

# Visualize User Size Distribution as a Bar Chart
size_distribution = customer_df['user_size'].value_counts().reset_index()
size_distribution.columns = ['user_size', 'count']


size_bar_fig = px.bar(
    size_distribution,
    x='user_size',
    y='count',
    title='User Size Distribution',
    labels={'user_size': 'User Size', 'count': 'Count'},
    template='plotly_white'
)
size_bar_fig.update_layout(
    xaxis_title='User Size',
    yaxis_title='Count',
    xaxis={'categoryorder': 'total descending'}  # Sort by count
)
size_bar_fig.show()

""" **Filtered Size Distribution Bar Chart**:
   - Focuses on commonly chosen sizes by filtering out less frequent categories.

"""

# Visualize User Size Distribution
size_distribution = customer_df['user_size'].value_counts().reset_index()
size_distribution.columns = ['user_size', 'count']
filtered_size_distribution = size_distribution[size_distribution['count'] > 50]


size_bar_fig = px.bar(
    filtered_size_distribution,
    x='user_size',
    y='count',
    title='User Size Distribution',
    labels={'user_size': 'User Size', 'count': 'Count'},
    template='plotly_white'
)
size_bar_fig.update_layout(
    xaxis_title='User Size',
    yaxis_title='Count',
    xaxis={'categoryorder': 'total descending'}
)
size_bar_fig.show()

"""**Average Height and Weight by Body Type Bar Chart**:
   - Illustrates the relationship between body types and physical attributes (height and weight).

"""

# Grouping by 'user_body_type'
body_type_grouped = customer_df.groupby('user_body_type')[['user_height', 'user_weight']].mean().reset_index()
body_type_trend_fig = px.bar(
    body_type_grouped,
    x='user_body_type',
    y=['user_height', 'user_weight'],
    title='Average Height and Weight by Body Type',
    labels={'value': 'Average', 'variable': 'Measurement', 'user_body_type': 'Body Type'},
    template='plotly_white',
    barmode='group'
)
body_type_trend_fig.update_layout(yaxis_title='Average Measurement', xaxis_title='Body Type')
body_type_trend_fig.show()

# Load the product dataset
product_df = pd.read_csv('./data/processed/product.csv')

# Total number of products
total_products = len(product_df)
print(f"Total products: {total_products}")

# Missing Values
missing_values = product_df.isnull().sum()
print("\nMissing Values in Each Column:")
print(missing_values)

# Unique Values
unique_values = product_df.nunique()
print("\nUnique Values in Each Column:")
print(unique_values)

# Price Analysis
# Summary Statistics for 'product_price'
price_stats = product_df['product_price'].describe()
print("Summary Statistics for 'product_price':")
print(price_stats)

# Visualize Price Distribution
price_hist_fig = px.histogram(
    product_df,
    x='product_price',
    title='Price Distribution of Products',
    labels={'product_price': 'Product Price'},
    nbins=20,
    template='plotly_white'
)
price_hist_fig.update_layout(xaxis_title='Product Price', yaxis_title='Count')
price_hist_fig.show()

# Category Distribution
category_distribution = product_df['product_category'].value_counts().reset_index()
category_distribution.columns = ['product_category', 'count']


# Visualize Category Distribution as a Bar Chart
category_bar_fig = px.bar(
    category_distribution,
    x='product_category',
    y='count',
    title='Product Category Distribution',
    labels={'product_category': 'Product Category', 'count': 'Count'},
    template='plotly_white'
)
category_bar_fig.update_layout(xaxis_title='Product Category', yaxis_title='Count')
category_bar_fig.show()

import plotly.express as px

# Calculate Category Distribution
category_distribution = product_df['product_category'].value_counts().reset_index()
category_distribution.columns = ['product_category', 'count']

# Filter categories with more than 10 counts
category_distribution_filtered = category_distribution[category_distribution['count'] > 20]

# Visualize Category Distribution as a Bar Chart
category_bar_fig = px.bar(
    category_distribution_filtered,
    x='product_category',
    y='count',
    title='Product Category Distribution',
    labels={'product_category': 'Product Category', 'count': 'Count'},
    template='plotly_white'
)
category_bar_fig.update_layout(xaxis_title='Product Category', yaxis_title='Count')
category_bar_fig.show()

# Average Price by Category
avg_price_by_category = product_df.groupby('product_category')['product_price'].mean().reset_index()

# Visualize Average Price by Category
avg_price_fig = px.bar(
    avg_price_by_category,
    x='product_category',
    y='product_price',
    title='Average Price by Product Category',
    labels={'product_category': 'Product Category', 'product_price': 'Average Price'},
    template='plotly_white'
)
avg_price_fig.update_layout(xaxis_title='Product Category', yaxis_title='Average Price')
avg_price_fig.show()

# Identify Top and Bottom Priced Products
most_expensive = product_df.nlargest(5, 'product_price')[['product_name', 'product_category', 'product_price']]
least_expensive = product_df.nsmallest(5, 'product_price')[['product_name', 'product_category', 'product_price']]

print("\nTop 5 Most Expensive Products:")
print(most_expensive)

print("\nTop 5 Least Expensive Products:")
print(least_expensive)

# Load the order dataset
order_df = pd.read_csv('./data/processed/order.csv')

# Total number of orders
total_orders = len(order_df)
print(f"Total orders: {total_orders}")

# Missing Values
missing_values = order_df.isnull().sum()
print("\nMissing Values in Each Column:")
print(missing_values)

# Unique Values
unique_values = order_df.nunique()
print("\nUnique Values in Each Column:")
print(unique_values)

# Paid Amount Analysis
# Summary Statistics for 'paid_amt'
paid_amt_stats = order_df['paid_amt'].describe()
print("\nSummary Statistics for 'paid_amt':")
print(paid_amt_stats)

# Visualize Paid Amount Distribution
paid_amt_hist_fig = px.histogram(
    order_df,
    x='paid_amt',
    title='Paid Amount Distribution',
    labels={'paid_amt': 'Paid Amount'},
    nbins=20,
    template='plotly_white'
)
paid_amt_hist_fig.update_layout(xaxis_title='Paid Amount', yaxis_title='Count')
paid_amt_hist_fig.show()

# Order Volume Trends Over Time
# Convert 'order_date' to datetime
order_df['order_date'] = pd.to_datetime(order_df['order_date'], errors='coerce')

# Group by month and year for trend analysis
order_df['year_month'] = order_df['order_date'].dt.to_period('M').astype(str)
monthly_order_trends = order_df.groupby('year_month').size().reset_index(name='order_count')

filtered_trends = monthly_order_trends[
    (monthly_order_trends['year_month'] >= '2023-01') &
    (monthly_order_trends['year_month'] <= '2024-01')
]

# Visualize Order Trends Over Time
order_trends_time_fig = px.line(
    filtered_trends,
    x='year_month',
    y='order_count',
    title='Order Volume Trends Over Time',
    labels={'year_month': 'Year-Month', 'order_count': 'Order Count'},
    template='plotly_white'
)
order_trends_time_fig.update_layout(xaxis_title='Year-Month', yaxis_title='Order Count')
order_trends_time_fig.show()

# Revenue Trends Over Time
monthly_revenue_trends = order_df.groupby('year_month')['paid_amt'].sum().reset_index()
filtered_trends = monthly_revenue_trends[
    (monthly_revenue_trends['year_month'] >= '2023-01') &
    (monthly_revenue_trends['year_month'] <= '2024-01')
]

# Visualize Revenue Trends Over Time
revenue_trends_fig = px.line(
    filtered_trends,
    x='year_month',
    y='paid_amt',
    title='Revenue Trends Over Time',
    labels={'year_month': 'Year-Month', 'paid_amt': 'Total Revenue'},
    template='plotly_white'
)
revenue_trends_fig.update_layout(xaxis_title='Year-Month', yaxis_title='Total Revenue')
revenue_trends_fig.show()

# Customer Spending Analysis

avg_spending_by_customer = order_df.groupby('customer_userid')['paid_amt'].sum()/order_df.groupby('customer_userid')['paid_amt'].count()
avg_spending_by_customer = avg_spending_by_customer.reset_index()
avg_spending_by_customer.columns = ['customer_userid', 'avg_spending']

# Visualize Top Customers by Spending
top_customers = avg_spending_by_customer.nlargest(20, 'avg_spending')
top_customers_fig = px.bar(
    top_customers,
    x='customer_userid',
    y='avg_spending',
    title='Average Spending of Customers',
    labels={'customer_userid': 'Customer UserID', 'avg_spending': 'Total Spent'},
    template='plotly_white'
)
top_customers_fig.update_layout(xaxis_title='Customer UserID', yaxis_title='Total Spent')
top_customers_fig.show()

avg_spending_by_customer = order_df.groupby('customer_userid')['paid_amt'].sum()/order_df.groupby('customer_userid')['paid_amt'].count()
avg_spending_by_customer = avg_spending_by_customer.reset_index()
avg_spending_by_customer.columns = ['customer_userid', 'avg_spending']
avg_spending_by_customer.sort_values(by='avg_spending', ascending=False)

"""**Product Popularity Bar Chart**:
    - Shows the most purchased products, emphasizing high-demand items.
"""

product_df = pd.read_csv('./data/processed/product.csv')

# Calculate total revenue for each product based on product_id
product_revenue = order_df.groupby('product_id')['paid_amt'].sum().reset_index()
product_revenue.columns = ['product_id', 'total_revenue']

# Get the top 20 products by revenue
top_products = product_revenue.nlargest(20, 'total_revenue')

# Merge with product_df to get product_name
top_products = top_products.merge(product_df[['product_id', 'product_name']], on='product_id', how='left')

# Visualize Top 20 Products by Revenue with Product Names
top_products_fig = px.bar(
    top_products,
    x='product_name',  # Use product_name instead of product_id for display
    y='total_revenue',
    title='Top Selling Products',
    labels={'product_name': 'Product Name', 'total_revenue': 'Total Revenue'},
    template='plotly_white'
)
top_products_fig.update_layout(xaxis_title='Product Name', yaxis_title='Total Revenue')
top_products_fig.show()

"""**Category Popularity Bar Chart**:
    - Compares product categories based on total sales, providing insights into customer preferences.

"""

# Merge order_df with product_df to include product_category
merged_df = order_df.merge(product_df[['product_id', 'product_category']], on='product_id', how='left')

# Calculate total revenue for each category
top_selling_categories = merged_df.groupby('product_category')['paid_amt'].sum().reset_index()
top_selling_categories.columns = ['product_category', 'total_revenue']

# Sort and get top 10 categories
top_selling_categories = top_selling_categories.nlargest(10, 'total_revenue')

# Visualize Top Selling Categories
fig = px.bar(
    top_selling_categories,
    x='product_category',
    y='total_revenue',
    title='Top Selling Categories',
    labels={'product_category': 'Product Category', 'total_revenue': 'Total Revenue'},
    template='plotly_white'
)
fig.update_layout(xaxis_title='Product Category', yaxis_title='Total Revenue')
fig.show()

# Load the reviews dataset
reviews_df = pd.read_csv('./data/processed/reviews.csv')

# Initial Analysis
# Total number of reviews
total_reviews = len(reviews_df)
print(f"Total reviews: {total_reviews}")

# Missing Values
missing_values = reviews_df.isnull().sum()
print("\nMissing Values in Each Column:")
print(missing_values)

# Unique Values
unique_values = reviews_df.nunique()
print("\nUnique Values in Each Column:")
print(unique_values)

"""**Rating Distribution Bar Chart**:
   - Highlights the distribution of product ratings to identify trends in customer satisfaction.

"""

# Star Ratings Analysis
# Summary Statistics for 'star_ratings'
star_ratings_stats = reviews_df['star_ratings'].describe()
print("\nSummary Statistics for 'star_ratings':")
print(star_ratings_stats)

# Visualize Star Ratings as Pie Chart
star_ratings_pie_data = reviews_df['star_ratings'].value_counts().reset_index()
star_ratings_pie_data.columns = ['star_rating', 'count']

star_ratings_pie_fig = px.pie(
    star_ratings_pie_data,
    names='star_rating',
    values='count',
    title='Star Ratings Distribution',
    template='plotly_white'
)
star_ratings_pie_fig.show()

"""**Review Trends Over Time Line Chart**:
   - Displays the frequency of product reviews over time, highlighting periods of high customer engagement.

"""

reviews_df['review_date'] = pd.to_datetime(reviews_df['review_date'], errors='coerce')

# Group by month and year for trend analysis
reviews_df['year_month'] = reviews_df['review_date'].dt.to_period('M').astype(str)
monthly_review_trends = reviews_df.groupby('year_month').size().reset_index(name='review_count')

# Filter data for the period Jan 2023 - Jan 2024
filtered_review_trends = monthly_review_trends[
    (monthly_review_trends['year_month'] >= '2023-01') &
    (monthly_review_trends['year_month'] <= '2024-01')
]

# Visualize Review Trends Over Time
review_trends_time_fig = px.line(
    filtered_review_trends,
    x='year_month',
    y='review_count',
    title='Review Trends Over Time (2023)',
    labels={'year_month': 'Year-Month', 'review_count': 'Review Count'},
    template='plotly_white'
)
review_trends_time_fig.update_layout(xaxis_title='Year-Month', yaxis_title='Review Count')
review_trends_time_fig.show()

"""**Ratings vs. Revenue**:
    - Explores the relationship between product ratings and revenue, identifying high-performing products.

"""

# Merge datasets
merged_df = pd.merge(order_df, reviews_df, on=['product_id', 'customer_userid'], how='inner')
merged_df = pd.merge(merged_df, product_df[['product_id', 'product_name', 'product_category']], on='product_id', how='left')

# Calculate average star ratings and total revenue per product
product_performance = merged_df.groupby('product_id').agg({
    'paid_amt': 'sum',
    'star_ratings': 'mean',
    'product_name': 'first',  # Include product_name
    'product_category': 'first'
}).reset_index()

# Rename columns
product_performance.columns = ['product_id', 'total_revenue', 'avg_star_rating', 'product_name', 'product_category']

# Visualize top-performing products
top_products = product_performance.nlargest(10, 'total_revenue')
fig = px.bar(
    top_products,
    x='product_name',  # Use product_name instead of product_id
    y='total_revenue',
    color='avg_star_rating',
    title='Top 10 Products by Revenue and Average Star Rating',
    labels={'product_name': 'Product Name', 'total_revenue': 'Total Revenue', 'avg_star_rating': 'Avg Star Rating'},
    template='plotly_white'
)
fig.update_layout(xaxis_title='Product Name', yaxis_title='Total Revenue')
fig.show()

# Merge datasets
category_analysis = pd.merge(order_df, reviews_df, on='product_id', how='inner')
category_analysis = pd.merge(category_analysis, product_df, on='product_id', how='left')

# Calculate metrics for each category
category_performance = category_analysis.groupby('product_category').agg({
    'paid_amt': 'sum',
    'star_ratings': 'mean',
    'review_content': 'count'
}).reset_index()
category_performance.columns = ['product_category', 'total_revenue', 'avg_star_rating', 'total_reviews']

# Visualize Category Performance
fig = px.bar(
    category_performance,
    x='product_category',
    y='total_revenue',
    color='avg_star_rating',
    title='Category Performance: Revenue, Ratings, and Reviews',
    labels={'product_category': 'Product Category', 'total_revenue': 'Total Revenue'},
    template='plotly_white'
)
fig.update_layout(xaxis_title='Product Category', yaxis_title='Total Revenue')
fig.show()

# Fill missing values with the mean of the respective columns
columns_to_impute = ['user_age', 'user_weight', 'user_height']
for column in columns_to_impute:
    customer_df[column] = customer_df[column].fillna(customer_df[column].mean())


customer_df

def remove_outliers_iqr(data, column):
    q1 = data[column].quantile(0.15)
    q3 = data[column].quantile(0.80)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    return data[(data[column] >= lower_bound) & (data[column] <= upper_bound)]

customer_df = remove_outliers_iqr(customer_df, 'user_age')

# Visualize Age Distribution using a Histogram
hist_fig = px.histogram(
    customer_df,
    x='user_age',
    title='Age Distribution of Customers',
    labels={'user_age': 'Age'},
    nbins=20,
    template='plotly_white'
)
hist_fig.update_layout(xaxis_title='Age', yaxis_title='Count')
hist_fig.show()

def remove_outliers_iqr(data, column):
    q1 = data[column].quantile(0.15)
    q3 = data[column].quantile(0.80)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    return data[(data[column] >= lower_bound) & (data[column] <= upper_bound)]

customer_df = remove_outliers_iqr(customer_df, 'user_weight')

# Visualize Weight Distribution
weight_hist_fig = px.histogram(
    customer_df,
    x='user_weight',
    title='Weight Distribution of Customers',
    labels={'user_weight': 'Weight (in lbs)'},
    nbins=20,
    template='plotly_white'
)
weight_hist_fig.update_layout(xaxis_title='Weight (in lbs)', yaxis_title='Count')
weight_hist_fig.show()

def remove_outliers_iqr(data, column):
    q1 = data[column].quantile(0.15)
    q3 = data[column].quantile(0.80)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    return data[(data[column] >= lower_bound) & (data[column] <= upper_bound)]

customer_df = remove_outliers_iqr(customer_df, 'user_height')

# Visualize Height Distribution
height_hist_fig = px.histogram(
    customer_df,
    x='user_height',
    title='Height Distribution of Customers',
    labels={'user_height': 'Height (in inches)'},
    nbins=20,
    template='plotly_white'
)
height_hist_fig.update_layout(xaxis_title='Height (in inches)', yaxis_title='Count')
height_hist_fig.show()

import numpy as np
product_df['product_price'] = np.log(product_df['product_price'])

# Visualize Price Distribution
price_hist_fig = px.histogram(
    product_df,
    x='product_price',
    title='Price Distribution of Products',
    labels={'product_price': 'Product Price'},
    nbins=20,
    template='plotly_white'
)
price_hist_fig.update_layout(xaxis_title='Product Price', yaxis_title='Count')
price_hist_fig.show()

order_df = pd.read_csv('./data/processed/order.csv')

order_df['paid_amt'] = np.log10(order_df['paid_amt'])

# Visualize Paid Amount Distribution
paid_amt_hist_fig = px.histogram(
    order_df,
    x='paid_amt',
    title='Paid Amount Distribution',
    labels={'paid_amt': 'Paid Amount'},
    nbins=20,
    template='plotly_white'
)
paid_amt_hist_fig.update_layout(xaxis_title='Paid Amount', yaxis_title='Count')
paid_amt_hist_fig.show()

