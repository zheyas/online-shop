
from django import forms
from .models import Product

FORBIDDEN_WORDS = {"казино", "криптовалюта", "крипта", "биржа", "дешево", "бесплатно", "обман", "полиция", "радар"}

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "image", "category", "purchase_price"]

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control',  # Стилизация с использованием класса CSS
                'placeholder': f'Введите {field.label.lower()}'  # Добавление плейсхолдера
            })

    def clean_name(self):
        name = self.cleaned_data["name"].lower()
        if any(word in name for word in FORBIDDEN_WORDS):
            raise forms.ValidationError("Название содержит запрещенные слова.")
        return self.cleaned_data["name"]

    def clean_description(self):
        description = self.cleaned_data["description"].lower()
        if any(word in description for word in FORBIDDEN_WORDS):
            raise forms.ValidationError("Описание содержит запрещенные слова.")
        return self.cleaned_data["description"]

    def clean_purchase_price(self):
        purchase_price = self.cleaned_data.get("purchase_price")
        if purchase_price is not None and purchase_price < 0:
            raise forms.ValidationError("Цена не может быть отрицательной.")
        return purchase_price

class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100, label='Имя',
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'autocomplete': 'name'}))
    message = forms.CharField(
        label='Сообщение', widget=forms.Textarea(
            attrs={'class': 'form-control', 'autocomplete': 'off'}))
