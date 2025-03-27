import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np  # Added missing import
import io
import base64
from django.shortcuts import render

def save_plot_to_buffer():  # Added missing function
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    plt.close()
    buffer.seek(0)
    return buffer

def area_prices(request, city):
    try:
        df = pd.read_csv(f"data/{city.lower()}_house_prices.csv")
        buffers = {}

        # 1. Price per Sqft
        plt.figure(figsize=(12, 8))
        df["Price_per_sqft"] = df["Price"] / df["Size_sqft"]
        area_avg_price = df.groupby("Area")["Price_per_sqft"].mean().sort_values(ascending=False).head(20)
        sns.barplot(x=area_avg_price.values, y=area_avg_price.index, palette="viridis")
        plt.title(f"Top 20 Areas by Price/Sqft in {city.title()}")
        plt.xlabel("Price per Sqft (₹)")
        buffers['price_per_sqft'] = save_plot_to_buffer()

        # 2. Property Type Distribution
        plt.figure(figsize=(10, 6))
        prop_type_counts = df['Property_Type'].value_counts()
        plt.pie(prop_type_counts, labels=prop_type_counts.index,
                autopct='%1.1f%%', startangle=90, wedgeprops={'width': 0.4})
        plt.title(f'Property Type Distribution in {city.title()}')
        buffers['property_type'] = save_plot_to_buffer()

        # 3. Price vs Size
        plt.figure(figsize=(12, 8))
        sns.regplot(x='Size_sqft', y='Price', data=df, scatter_kws={'alpha':0.4}, line_kws={'color':'red'})
        plt.title(f'Price vs Property Size in {city.title()}')
        plt.xlabel('Size (sqft)')
        plt.ylabel('Price (₹)')
        plt.xlim(0, df['Size_sqft'].quantile(0.95))
        buffers['price_vs_size'] = save_plot_to_buffer()

        # 4. Bedroom Analysis
        plt.figure(figsize=(12, 8))
        bedroom_prices = df.groupby('Bedrooms')['Price'].median()
        ax = sns.barplot(x=bedroom_prices.index, y=bedroom_prices.values, palette="rocket")
        plt.title(f'Median Price by Bedroom Count in {city.title()}')
        plt.xlabel('Number of Bedrooms')
        plt.ylabel('Median Price (₹)')
        for p in ax.patches:
            ax.annotate(f'₹{p.get_height():,.0f}',
                       (p.get_x() + p.get_width() / 2., p.get_height()),
                       ha='center', va='center', xytext=(0, 10),
                       textcoords='offset points')
        buffers['bedroom_prices'] = save_plot_to_buffer()

        # 5. Correlation Heatmap
        plt.figure(figsize=(14, 10))
        numeric_cols = df.select_dtypes(include=['number']).columns
        corr_matrix = df[numeric_cols].corr()
        mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
        sns.heatmap(corr_matrix[corr_matrix.abs() > 0.3], mask=mask,
                   annot=True, cmap='coolwarm', fmt=".2f", vmin=-1, vmax=1)
        plt.title(f'Feature Correlations in {city.title()}')
        buffers['correlation'] = save_plot_to_buffer()

        graphics = {k: base64.b64encode(v.getvalue()).decode('utf-8') for k, v in buffers.items()}

        descriptions = {
            'price_per_sqft': "Shows the most expensive areas by price per square foot. Higher values indicate premium locations.",
            'property_type': "Displays the distribution of different property types in the market. Helps identify dominant property categories.",
            'price_vs_size': "Illustrates the relationship between property size and price. The red line shows the general trend.",
            'bedroom_prices': "Compares median prices based on bedroom count. Helps understand value progression with room numbers.",
            'correlation': "Shows how different numeric features relate to each other. Strong correlations (close to +1/-1) indicate important relationships."
        }

        return render(request, 'visualization/area_prices.html', {
            "graphics": graphics,
            "city": city.title(),
            "descriptions": descriptions
        })

    except FileNotFoundError:
        return render(request, 'error.html', {'message': f'Data not available for {city.title()}'})
    except Exception as e:
        return render(request, 'error.html', {'message': f'Error processing data: {str(e)}'})