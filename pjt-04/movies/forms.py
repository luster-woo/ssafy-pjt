from django import forms
from .models import Movie

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = '__all__'
        
        labels = {
            'title': 'Title:',
            'content': 'Description:',
            'director': 'Director:',
        }
        
        widgets = {
           
            'title': forms.TextInput(attrs={
                'class': 'form-control d-inline-block',
                'style': 'width: 200px;',  
            }),
            
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'cols': 40, 
                'rows': 10,
                'style': 'width: 300px;',  
            }),
           
            'director': forms.TextInput(attrs={
                'class': 'form-control d-inline-block',
                'style': 'width: 200px;',
            }),
        }