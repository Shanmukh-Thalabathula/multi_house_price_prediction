import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
import joblib

# Load data
data = pd.read_csv('data/hyderabad_house_prices.csv')

# Drop the 'Amenities' column (text data requiring special handling)
data = data.drop('Amenities', axis=1)

# Define features and target
X = data.drop('Price', axis=1)
y = data['Price']

# Identify column types
numerical_cols = [
    'Size_sqft', 'Bedrooms', 'Bathrooms', 'Age',
    'Floor', 'Furnished', 'Metro_Distance',
    'Mall_Distance', 'Hospital_Distance', 'School_Distance'
]
categorical_cols = ['Area', 'Property_Type']  # Categorical features

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
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Preprocess data
X_train_preprocessed = preprocessor.fit_transform(X_train)
X_test_preprocessed = preprocessor.transform(X_test)

# Train model
model = RandomForestRegressor(n_estimators=200, random_state=42, max_depth=10)
model.fit(X_train_preprocessed, y_train)

# Save artifacts
joblib.dump(model, 'hyderabad_house_price_model.pkl')
joblib.dump(preprocessor, 'hyderabad_preprocessor.pkl')

print("Model training complete! Saved:")
print("- hyderabad_house_price_model.pkl (trained model)")
print("- hyderabad_preprocessor.pkl (data preprocessing pipeline)")