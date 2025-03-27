# descriptive_statistics/views.py

import pandas as pd
from django.shortcuts import render
from django.utils.text import slugify


def descriptive_stats(request, city):
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

        # Define numerical features
        numerical_cols = [
            'Size_sqft', 'Bedrooms', 'Bathrooms', 'Age', 'Floor',
            'Metro_Distance', 'Mall_Distance', 'Hospital_Distance',
            'School_Distance', 'Price'
        ]

        # Convert to numeric and clean data
        df[numerical_cols] = df[numerical_cols].apply(pd.to_numeric, errors='coerce')
        df = df.dropna(subset=numerical_cols)

        # Generate full statistics
        full_stats = df[numerical_cols].describe(percentiles=[.25, .5, .75]).round(2)

        # Prepare statistics dictionary
        stats_dict = {
            'count': 'Count',
            'mean': 'Mean',
            'std': 'Std Dev',
            'min': 'Minimum',
            '25%': '25th Percentile',
            '50%': 'Median',
            '75%': '75th Percentile',
            'max': 'Maximum'
        }

        # Organize statistics for template
        numerical_stats = {}
        for stat, stat_name in stats_dict.items():
            numerical_stats[stat_name] = {
                col: full_stats.at[stat, col] for col in numerical_cols
            }

        # Prepare price statistics
        price_stats = {
            'Average': df['Price'].mean(),
            'Median': df['Price'].median(),
            'Minimum': df['Price'].min(),
            'Maximum': df['Price'].max(),
            'Std Deviation': df['Price'].std(),
            'Range': df['Price'].max() - df['Price'].min()
        }

        # Prepare categorical stats
        categorical_stats = {}
        for cat_col in ['Property_Type', 'Furnished', 'Amenities']:
            if cat_col in df.columns:
                counts = df[cat_col].value_counts().head(10)
                categorical_stats[cat_col] = {
                    'top_values': counts.to_dict(),
                    'unique_count': df[cat_col].nunique(),
                    'mode': counts.index[0] if not counts.empty else 'N/A'
                }

        context = {
            'city': city.title(),
            'selected_area': selected_area,
            'areas': areas,
            'numerical_stats': numerical_stats,
            'price_stats': price_stats,
            'categorical_stats': categorical_stats,
            'numerical_columns': numerical_cols,
            'statistics_order': [
                'Count', 'Mean', 'Std Dev', 'Minimum',
                '25th Percentile', 'Median', '75th Percentile', 'Maximum'
            ]
        }

        return render(request, 'descriptive_statistics/stats.html', context)

    except Exception as e:
        return render(request, 'error.html', {'message': f"Error: {str(e)}"})