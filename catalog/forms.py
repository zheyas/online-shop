from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label='Имя', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'name'}))
    message = forms.CharField(label='Сообщение', widget=forms.Textarea(attrs={'class': 'form-control', 'autocomplete': 'off'}))