from django import forms
from .models import Feedback

# class AvailabilityForm(forms.Form):
#     Room_Categories = ( 
#                        ('WAC','AC'),
#                        ('NAC','NON_AC'),
#                        ('DEL','DELUXE'),
#                        ('KIN','KING'),
#                        ('QUE','QUEEN'))
#     room_category = forms.ChoiceField(choices=Room_Categories, required=True)
#     #price = forms.IntegerField(required=True)
#     check_in = forms.DateTimeField(required=True, input_formats="%y-%m-%dT%H:%M",)
#     check_out = forms.DateTimeField(required=True, input_formats="%y-%m-%dT%H:%M",)




class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ('rating', 'comment')
