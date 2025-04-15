from django import forms


class QueryForm(forms.Form):
    CITY_CHOICES = [
        ('hyderabad', 'Hyderabad'),
        ('delhi', 'Delhi'),
        ('kolkata', 'Kolkata'),
        ('mumbai', 'Mumbai')
    ]

    city = forms.ChoiceField(choices=CITY_CHOICES)
    query = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'query-input',
        'placeholder': 'Enter your SQL query here...'
    }))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user and self.user.is_authenticated:
            self.fields['load_history'] = forms.ModelChoiceField(
                queryset=QueryHistory.objects.filter(user=self.user),
                required=False,
                label='Load from history'
            )