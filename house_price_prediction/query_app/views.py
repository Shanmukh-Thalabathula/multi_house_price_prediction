import pandas as pd
import sqlite3
from django.shortcuts import render
from django.conf import settings
from .forms import QueryForm
import os


def query_interface(request):
    results = []
    columns = []
    error = None
    form = QueryForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        try:
            city = form.cleaned_data['city']
            raw_sql = form.cleaned_data['query']
            sql_query = raw_sql.lower()

            # Security check
            forbidden_keywords = ['insert', 'update', 'delete', 'drop', 'alter', ';--']
            if any(kw in sql_query for kw in forbidden_keywords):
                raise ValueError("Potentially dangerous operation detected")

            # Load and process CSV
            csv_path = os.path.join(settings.BASE_DIR, 'data', f'{city}_house_prices.csv')
            df = pd.read_csv(csv_path).applymap(lambda x: x.strip() if isinstance(x, str) else x)

            # Convert numeric columns
            numeric_cols = ['Price', 'Size_sqft', 'Bedrooms', 'Bathrooms']
            type_mapping = {
                'Price': 'REAL',
                'Size_sqft': 'REAL',
                'Bedrooms': 'INTEGER',
                'Bathrooms': 'REAL'
            }

            for col in numeric_cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')

            # Create SQLite in-memory database with proper typing
            conn = sqlite3.connect(':memory:')

            # Create type mapping dictionary
            dtype_dict = {col: type_mapping.get(col, 'TEXT') for col in df.columns}

            # Write DataFrame to SQL with type mapping
            df.to_sql(
                'properties',
                conn,
                index=False,
                dtype=dtype_dict,
                if_exists='replace'
            )

            # Execute query
            cursor = conn.cursor()
            cursor.execute(raw_sql)

            # Get results with proper types
            if cursor.description:
                columns = [desc[0] for desc in cursor.description]
                results = cursor.fetchall()
                # Convert bytes to strings for display
                results = [
                    tuple(x.decode('utf-8') if isinstance(x, bytes) else x for x in row)
                    for row in results
                ]

            conn.close()

        except Exception as e:
            error = str(e)

    return render(request, 'query_app/interface.html', {
        'form': form,
        'results': results,
        'columns': columns,
        'error': error
    })