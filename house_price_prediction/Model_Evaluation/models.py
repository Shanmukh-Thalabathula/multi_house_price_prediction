from django.db import models

class EvaluationMetrics(models.Model):
    city = models.CharField(max_length=50, unique=True)
    mse = models.FloatField()
    rmse = models.FloatField()
    mae = models.FloatField()
    r2 = models.FloatField()
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.city} Metrics"