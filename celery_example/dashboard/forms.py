
from .models import Post
from django import forms
import datetime


class DateUpdateForm(forms.DateTimeInput):
    input_type = 'datetime-local'


class ScheduledDateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['scheduled_date']
        widgets = {
            'scheduled_date': DateUpdateForm(attrs={'class': 'datetimepicker'})
        }

    def clean_scheduled_date(self):
        date = self.cleaned_data['scheduled_date']
        if date.date() < datetime.date.today():
            raise forms.ValidationError("Date in past")
        return date
