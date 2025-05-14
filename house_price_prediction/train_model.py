import os
import django
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# Django setup to access models
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'house_price_prediction.settings')
django.setup()

from Model_Evaluation.models import EvaluationMetrics

# Configuration
CITIES = ['hyderabad', 'delhi', 'mumbai', 'kolkata']  # Add all your cities


def train_and_evaluate_models():
    for city in CITIES:
        print(f"\n{'=' * 40}")
        print(f"Processing {city.capitalize()} dataset")
        print(f"{'=' * 40}")

        try:
            # Load data
            data = pd.read_csv(f'data/{city}_house_prices.csv')

            # Data preprocessing
            data = data.drop('Amenities', axis=1)
            X = data.drop('Price', axis=1)
            y = data['Price']

            # Define column types
            numerical_cols = [
                'Size_sqft', 'Bedrooms', 'Bathrooms', 'Age',
                'Floor', 'Furnished', 'Metro_Distance',
                'Mall_Distance', 'Hospital_Distance', 'School_Distance'
            ]
            categorical_cols = ['Area', 'Property_Type']

            # Create preprocessing pipeline
            numerical_transformer = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='median')),
                ('scaler', StandardScaler())
            ])

            categorical_transformer = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='most_frequent')),
                ('encoder', OneHotEncoder(handle_unknown='ignore'))
            ])

            preprocessor = ColumnTransformer(transformers=[
                ('num', numerical_transformer, numerical_cols),
                ('cat', categorical_transformer, categorical_cols)
            ])

            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )

            # Preprocess data
            X_train_preprocessed = preprocessor.fit_transform(X_train)
            X_test_preprocessed = preprocessor.transform(X_test)

            # Train model
            model = RandomForestRegressor(
                n_estimators=200,
                random_state=42,
                max_depth=10
            )
            model.fit(X_train_preprocessed, y_train)

            # Save artifacts
            joblib.dump(model, f'{city}_house_price_model.pkl')
            joblib.dump(preprocessor, f'{city}_preprocessor.pkl')

            # Generate predictions
            y_pred = model.predict(X_test_preprocessed)

            # Calculate metrics
            metrics = {
                'mse': mean_squared_error(y_test, y_pred),
                'rmse': mean_squared_error(y_test, y_pred) ** 0.5,
                'mae': mean_absolute_error(y_test, y_pred),
                'r2': r2_score(y_test, y_pred)
            }

            # Save to database
            EvaluationMetrics.objects.update_or_create(
                city=city,
                defaults=metrics
            )

            print(f"\n{city.capitalize()} metrics:")
            print(f"MSE: {metrics['mse']:.2f}")
            print(f"RMSE: {metrics['rmse']:.2f}")
            print(f"MAE: {metrics['mae']:.2f}")
            print(f"R²: {metrics['r2']:.2f}")
            print(f"Saved {city} model and metrics!")

        except Exception as e:
            print(f"\nError processing {city}: {str(e)}")
            continue


if __name__ == "__main__":
    train_and_evaluate_models()
    print("\nTraining complete for all cities!")