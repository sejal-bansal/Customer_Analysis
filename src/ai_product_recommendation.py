# -*- coding: utf-8 -*-
"""AI_Product_Recommendation.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1NdSgHCipfplzhmrAI_DkyflpgHOZV2lL

## AI-Powered Product Recommendation System

This notebook implements an AI-powered product recommendation system for the given dataset. The system leverages customer purchase history and product details to recommend relevant products.

Key steps in this notebook include:
- Loading and preprocessing datasets (`order.csv`, `reviews.csv`, `product.csv`).
- Calculating similarities using cosine similarity.
- Generating product recommendations for customers based on their past purchases.

This is the final step in the project, consolidating insights from previous analyses to create a functional recommendation system.

## Dataset and Libraries
The datasets used in this notebook include:
- `order.csv`: Contains customer purchase history, including purchase amounts and dates.
- `reviews.csv`: Includes customer reviews and ratings for products.
- `product.csv`: Provides details about products, such as categories and descriptions.

Libraries:
- **pandas**: For data manipulation and analysis, including loading and merging datasets.
- **numpy**: For numerical computations and matrix operations.
- **scikit-learn**:
   - `cosine_similarity`: To compute similarity scores between products or customers.
   - `StandardScaler`: To normalize data for improved similarity calculations.

The datasets are merged and preprocessed to ensure consistency and prepare for the recommendation system.
"""

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
import numpy as np

# Load datasets
order_data = pd.read_csv('./data/processed/order.csv')
reviews_data = pd.read_csv('./data/processed/reviews.csv')
product_data = pd.read_csv('./data/processed/product.csv')

"""The recommendation system uses cosine similarity to:
- Measure the similarity between products based on purchase and review data.
- Suggest relevant products to customers based on their previous purchases.

Standard scaling is applied to normalize data and improve similarity calculations.
"""

# Merge datasets on product_id and customer_userid
merged_data = pd.merge(order_data, reviews_data, on=['product_id', 'customer_userid'], how='inner')

# Create a user-item interaction matrix
user_item_matrix = merged_data.pivot_table(
    index='customer_userid', columns='product_id', values='star_ratings', fill_value=0
)

# Normalize the user-item matrix for cosine similarity
scaler = StandardScaler()
user_item_normalized = scaler.fit_transform(user_item_matrix)

# Calculate cosine similarity between users
user_similarity = cosine_similarity(user_item_normalized)
user_similarity_df = pd.DataFrame(user_similarity, index=user_item_matrix.index, columns=user_item_matrix.index)

# Function to recommend products for a specific user with confidence scores
def recommend_products(customer_userid, top_n=5):
    if customer_userid not in user_similarity_df.index:
        return f"Customer ID {customer_userid} not found in the dataset."

    # similarity scores for user
    similar_users = user_similarity_df[customer_userid].sort_values(ascending=False)
    similar_users = similar_users[similar_users.index != customer_userid]

    # Weighted average for similar users
    weighted_ratings = np.dot(similar_users.values, user_item_matrix.loc[similar_users.index])
    similarity_sum = np.abs(similar_users.values).sum()
    if similarity_sum == 0:
        return "No similar users found to base recommendations on."
    recommendations = weighted_ratings / similarity_sum

    # Create a Series with product IDs and their corresponding recommendation scores
    recommendations_series = pd.Series(recommendations, index=user_item_matrix.columns)

    # Filter out products already rated by the user
    rated_products = user_item_matrix.loc[customer_userid]
    unrated_products = recommendations_series[~rated_products.index.isin(rated_products[rated_products > 0].index)]

    # Get the top N product IDs and their scores
    top_products = unrated_products.nlargest(top_n)

    # Map product IDs to product names using product_data
    top_product_names = product_data[product_data['product_id'].isin(top_products.index)][['product_id', 'product_name']]

    # Merge to include scores
    top_recommendations = top_product_names.merge(top_products.rename('score'), left_on='product_id', right_index=True)

    # Normalize scores
    min_score = top_recommendations['score'].min()
    max_score = top_recommendations['score'].max()
    if max_score == min_score:
        top_recommendations['confidence'] = 100
    else:
        top_recommendations['confidence'] = 100 * (top_recommendations['score'] - min_score) / (max_score - min_score)

    # Sort by confidence
    top_recommendations = top_recommendations.sort_values(by='confidence', ascending=False)

    return top_recommendations[['product_id', 'product_name', 'confidence']]

"""## Generating Recommendations

Recommendations are generated by identifying products that are most similar to those previously purchased by each customer. The system considers:
- Purchase frequency and amounts.
- Customer reviews and product ratings.

Example recommendations for selected customer is displayed in the results below.

"""

# Example
customer_id = 'user_3454'
recommended_products = recommend_products(customer_id, top_n=5)
print(f"Recommended products for customer {customer_id}:")
print(recommended_products)

