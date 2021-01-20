from django.forms.fields import DateTimeField
from django.forms.widgets import DateTimeInput
from .models import Post
from django import forms

class DateUpdateForm(forms.DateTimeInput):
    input_type = 'datetime-local'
    
class ScheduledDateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['scheduled_date']
        widgets = {
            'scheduled_date':DateUpdateForm()
        }

