import pandas as pd
import sqlite3
from io import StringIO
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
            raw_sql = form.cleaned_data['query']  # Keep original case
            sql_query = raw_sql.lower()  # Only for security checks

            # Security check (case-insensitive)
            forbidden_keywords = ['insert', 'update', 'delete', 'drop', 'alter', ';--']
            if any(kw in sql_query for kw in forbidden_keywords):
                raise ValueError("Potentially dangerous operation detected")

            # Load CSV with type conversion
            csv_path = os.path.join(settings.BASE_DIR, 'data', f'{city}_house_prices.csv')
            df = pd.read_csv(csv_path).applymap(lambda x: x.strip() if isinstance(x, str) else x)

            # Convert numeric columns
            numeric_cols = ['Price', 'Size_sqft', 'Bedrooms', 'Bathrooms']
            for col in numeric_cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')

            # Create in-memory DB with case-sensitive column names
            conn = sqlite3.connect(':memory:')
            df.to_sql('properties', conn, index=False, dtype={col: 'TEXT' for col in df.columns})

            # Execute original case query
            cursor = conn.cursor()
            cursor.execute(raw_sql)  # Use original case-sensitive query

            # Get results
            if cursor.description:
                columns = [desc[0] for desc in cursor.description]
                results = cursor.fetchall()

            conn.close()

        except Exception as e:
            error = str(e)

    return render(request, 'query_app/interface.html', {
        'form': form,
        'results': results,
        'columns': columns,
        'error': error
    })