from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
import pandas as pd
import joblib
from users.models import RecentActivity

# Helper function to load localities
def get_localities(city):
    try:
        df = pd.read_csv(f'data/{city}_house_prices.csv')
        return sorted(df['Area'].unique().tolist())
    except Exception as e:
        print(f"Error loading localities: {str(e)}")
        return []



@login_required(login_url='login')
def predict_price(request,city):

    # load model and preprocess
    model = joblib.load(f'{city}_house_price_model.pkl')
    preprocessor = joblib.load(f'{city}_preprocessor.pkl')

    localities = get_localities(city)

    if request.method == 'POST':
        try:
            input_data = {
                'Area': request.POST.get('area', '').strip(),
                'Size_sqft': int(request.POST.get('size_sqft', 0)),
                'Bedrooms': int(request.POST.get('bedrooms', 1)),
                'Bathrooms': int(request.POST.get('bathrooms', 1)),
                'Property_Type': request.POST.get('property_type'),
                'Age': int(request.POST.get('age', 0)),
                'Floor': int(request.POST.get('floor', 0)),
                'Furnished': int(request.POST.get('furnished', 0)),
                'Amenities': request.POST.getlist('amenities', []),
                'Metro_Distance': float(request.POST.get('metro_distance', 0.0)),
                'Mall_Distance': float(request.POST.get('mall_distance', 0.0)),
                'Hospital_Distance': float(request.POST.get('hospital_distance', 0.0)),
                'School_Distance': float(request.POST.get('school_distance', 0.0))
            }

            if input_data['Area'] not in localities:
                messages.error(request, 'Invalid locality selected')
                return render(request, 'form.html', {
                    'localities': localities,
                    'form_data': input_data
                })

            # Prepare and predict
            input_df = pd.DataFrame([input_data])
            processed_data = preprocessor.transform(input_df)
            prediction = model.predict(processed_data)[0]

            # Save activity
            RecentActivity.save_activity(request.user, input_data, prediction)

            return render(request, 'result.html', {
                'prediction': f'₹{int(prediction):,}',
                'input_data': input_data
            })

        except Exception as e:
            messages.error(request, f'Error processing request: {str(e)}')
            return render(request, 'form.html', {
                'localities': localities,
                'form_data': request.POST
            })


    return render(request, 'form.html', {
        'city': city.capitalize(),
        'localities': localities,
        'form_data': request.POST if request.method == 'POST' else None,
        'amenities_list': ['Swimming Pool', 'Gym', 'Parking', 'Security', 'Park', 'Clubhouse']
    })


