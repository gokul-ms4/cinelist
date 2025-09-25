from django import forms

from movies.models import *

class ReviewForm(forms.ModelForm):

    class Meta:

        model = ReviewItems

        exclude = ["title","review_id","poster_path","movie_id"]

        widgets = {
            'rating': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 10,
                'name' : 'rating'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'name' : 'content',
                'placeholder': 'Write your thoughts...'
            })
        }