from django.contrib.auth.models import User
from django.db import models

class RecentActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    locality = models.CharField(max_length=100)
    size_sqft = models.IntegerField()
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    property_type = models.CharField(max_length=50)
    age = models.IntegerField()
    floor = models.IntegerField()
    furnished = models.BooleanField()
    metro_distance = models.FloatField()
    mall_distance = models.FloatField()
    hospital_distance = models.FloatField()
    school_distance = models.FloatField()
    amenities = models.TextField()
    predicted_price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.locality} - ₹{int(self.predicted_price):,}"

    @classmethod
    def save_activity(cls, user, input_data, predicted_price):
        cls.objects.create(
            user=user,
            locality=input_data['Area'],
            size_sqft=input_data['Size_sqft'],
            bedrooms=input_data['Bedrooms'],
            bathrooms=input_data['Bathrooms'],
            property_type=input_data['Property_Type'],
            age=input_data['Age'],
            floor=input_data['Floor'],
            furnished=bool(input_data['Furnished']),
            metro_distance=input_data['Metro_Distance'],
            mall_distance=input_data['Mall_Distance'],
            hospital_distance=input_data['Hospital_Distance'],
            school_distance=input_data['School_Distance'],
            amenities=', '.join(input_data['Amenities']) if 'Amenities' in input_data else '',
            predicted_price=predicted_price
        )
