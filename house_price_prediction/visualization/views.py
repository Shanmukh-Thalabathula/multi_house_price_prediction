import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import io
import base64
from django.shortcuts import render
from django.utils.text import slugify


def save_plot_to_buffer():
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    plt.close()
    buffer.seek(0)
    return buffer


def area_prices(request, city):
    try:
        # Get user selection
        selected_area = request.GET.get('area', 'overall').strip()
        safe_city = slugify(city.lower())

        # Load data
        df = pd.read_csv(f"data/{safe_city}_house_prices.csv")

        # Get unique areas for dropdown
        areas = ['overall'] + sorted(df['Area'].dropna().astype(str).unique().tolist())

        # Apply area filter
        if selected_area != 'overall' and selected_area in df['Area'].astype(str).values:
            df = df[df['Area'].astype(str) == selected_area]

        buffers = {}

        # 1. Price per Sqft
        plt.figure(figsize=(12, 8))
        df["Price_per_sqft"] = df["Price"] / df["Size_sqft"]

        if selected_area == 'overall':
            area_avg_price = df.groupby("Area")["Price_per_sqft"].mean().sort_values(ascending=False).head(20)
            sns.barplot(x=area_avg_price.values, y=area_avg_price.index, palette="viridis")
            plt.title(f"Top 20 Areas by Price/Sqft in {city.title()}")
            price_per_sqft_desc = "Shows the most expensive areas by price per square foot. Higher values indicate premium locations."
        else:
            sns.histplot(df['Price_per_sqft'], kde=True, color='skyblue')
            plt.title(f'Price Distribution in {selected_area}')
            price_per_sqft_desc = f"Price distribution for properties in {selected_area}. The curve shows typical price ranges."

        buffers['price_per_sqft'] = save_plot_to_buffer()

        # 2. Property Type Distribution
        plt.figure(figsize=(10, 6))
        prop_type_counts = df['Property_Type'].value_counts()
        if len(prop_type_counts) > 0:
            plt.pie(prop_type_counts, labels=prop_type_counts.index,
                    autopct='%1.1f%%', startangle=90, wedgeprops={'width': 0.4})
            plt.title(f'Property Type Distribution in {selected_area if selected_area != "overall" else city.title()}')
        else:
            plt.text(0.5, 0.5, 'No Data Available', ha='center', va='center')
        buffers['property_type'] = save_plot_to_buffer()

        # 3. Price vs Size
        plt.figure(figsize=(12, 8))
        if not df.empty:
            sns.regplot(x='Size_sqft', y='Price', data=df, scatter_kws={'alpha': 0.4}, line_kws={'color': 'red'})
            plt.title(f'Price vs Size in {selected_area if selected_area != "overall" else city.title()}')
            plt.xlabel('Size (sqft)')
            plt.ylabel('Price (₹)')
            plt.xlim(0, df['Size_sqft'].quantile(0.95))
        else:
            plt.text(0.5, 0.5, 'No Data Available', ha='center', va='center')
        buffers['price_vs_size'] = save_plot_to_buffer()

        # 4. Bedroom Analysis
        plt.figure(figsize=(12, 8))
        if 'Bedrooms' in df.columns and not df.empty:
            bedroom_prices = df.groupby('Bedrooms')['Price'].median()
            ax = sns.barplot(x=bedroom_prices.index, y=bedroom_prices.values, palette="rocket")
            plt.title(f'Median Price by Bedrooms in {selected_area if selected_area != "overall" else city.title()}')
            plt.xlabel('Number of Bedrooms')
            plt.ylabel('Median Price (₹)')
            for p in ax.patches:
                ax.annotate(f'₹{p.get_height():,.0f}',
                            (p.get_x() + p.get_width() / 2., p.get_height()),
                            ha='center', va='center', xytext=(0, 10),
                            textcoords='offset points')
        else:
            plt.text(0.5, 0.5, 'No Data Available', ha='center', va='center')
        buffers['bedroom_prices'] = save_plot_to_buffer()

        # 5. Correlation Heatmap
        plt.figure(figsize=(14, 10))
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 1:
            corr_matrix = df[numeric_cols].corr()
            mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
            sns.heatmap(corr_matrix[corr_matrix.abs() > 0.3], mask=mask,
                        annot=True, cmap='coolwarm', fmt=".2f", vmin=-1, vmax=1)
            plt.title(f'Feature Correlations in {selected_area if selected_area != "overall" else city.title()}')
        else:
            plt.text(0.5, 0.5, 'Insufficient Data', ha='center', va='center')
        buffers['correlation'] = save_plot_to_buffer()

        graphics = {k: base64.b64encode(v.getvalue()).decode('utf-8') for k, v in buffers.items()}

        area_suffix = f" in {selected_area}" if selected_area != 'overall' else ""
        descriptions = {
            'price_per_sqft': price_per_sqft_desc,
            'property_type': f"Distribution of property types{area_suffix}. Helps identify popular property categories.",
            'price_vs_size': f"Relationship between property size and price{area_suffix}. Red line shows trend.",
            'bedroom_prices': f"Median prices based on bedroom count{area_suffix}. Shows value progression.",
            'correlation': f"Feature correlations{area_suffix}. Strong correlations (>0.3) shown."
        }

        return render(request, 'visualization/area_prices.html', {
            "graphics": graphics,
            "city": city.title(),
            "descriptions": descriptions,
            "areas": areas,
            "selected_area": selected_area
        })

    except FileNotFoundError:
        return render(request, 'error.html', {'message': f'Data not available for {city.title()}'})
    except Exception as e:
        return render(request, 'error.html', {'message': f'Error processing data: {str(e)}'})