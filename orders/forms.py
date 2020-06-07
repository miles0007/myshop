from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
	first_name = forms.CharField()
	mobile = forms.CharField()
	email = forms.EmailField()
	address = forms.CharField()
	postal_code = forms.CharField(widget=forms.NumberInput())
	city = forms.CharField()

	class Meta:
		model = Order
		fields = ['first_name','mobile','email','address',
				  'postal_code','city']
		