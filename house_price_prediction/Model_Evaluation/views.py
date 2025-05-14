from django.shortcuts import render
from .models import EvaluationMetrics

def model_metrics(request):
    metrics = EvaluationMetrics.objects.all().order_by('city')
    context = {
        'metrics': metrics,
        'cities': ['hyderabad', 'delhi', 'mumbai', 'kolkata']  # Add all your cities
    }
    return render(request, 'Model_Evaluation/metrics.html', context)