from django import forms
from django.core.validators import RegexValidator

class HyderabadHouseForm(forms.Form):
    PROPERTY_TYPES = [
        ('Apartment', 'Apartment'),
        ('Villa', 'Villa'),
        ('Independent House', 'Independent House')
    ]

    AMENITY_CHOICES = [
        ('Swimming Pool', 'Swimming Pool'),
        ('Gym', 'Gym'),
        ('Parking', 'Parking'),
        ('Security', 'Security'),
        ('Park', 'Park'),
        ('Clubhouse', 'Clubhouse'),
    ]

    area = forms.CharField(
        label='Locality',
        widget=forms.TextInput(attrs={
            'autocomplete': 'off',
            'pattern': '[A-Za-z ]+',
            'title': 'Only letters and spaces allowed'
        }),
        validators=[
            RegexValidator(
                regex='^[A-Za-z ]+$',
                message='Locality name must contain only letters and spaces'
            )
        ],
        required=True
    )

    size_sqft = forms.IntegerField(
        label='Size (Square Feet)',
        min_value=100,
        max_value=10000,
        widget=forms.NumberInput(attrs={'step': '100'})
    )

    bedrooms = forms.IntegerField(
        label='Bedrooms',
        min_value=1,
        max_value=10
    )

    bathrooms = forms.IntegerField(
        label='Bathrooms',
        min_value=1,
        max_value=10
    )

    property_type = forms.ChoiceField(
        choices=PROPERTY_TYPES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    age = forms.IntegerField(
        label='Property Age (Years)',
        min_value=0,
        max_value=100
    )

    floor = forms.IntegerField(
        label='Floor Number',
        min_value=0
    )

    furnished = forms.ChoiceField(
        label='Furnished',
        choices=[('1', 'Yes'), ('0', 'No')],
        widget=forms.RadioSelect
    )

    amenities = forms.MultipleChoiceField(
        label='Amenities',
        choices=AMENITY_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    # New distance fields
    metro_distance = forms.FloatField(
        label='Distance to Nearest Metro (km)',
        min_value=0.1,
        max_value=20.0,
        widget=forms.NumberInput(attrs={'step': '0.1'}),
        required=True
    )

    mall_distance = forms.FloatField(
        label='Distance to Nearest Mall (km)',
        min_value=0.1,
        max_value=20.0,
        widget=forms.NumberInput(attrs={'step': '0.1'}),
        required=True
    )

    hospital_distance = forms.FloatField(
        label='Distance to Nearest Hospital (km)',
        min_value=0.1,
        max_value=20.0,
        widget=forms.NumberInput(attrs={'step': '0.1'}),
        required=True
    )

    school_distance = forms.FloatField(
        label='Distance to Nearest School (km)',
        min_value=0.1,
        max_value=20.0,
        widget=forms.NumberInput(attrs={'step': '0.1'}),
        required=True
    )