from django import forms

PRODUCT_QUANTITY_CHOICES = [(i,str(i)) for i in range(1,11)]

class CartAddProductForm(forms.Form):
	quantity = forms.TypedChoiceField(widget=forms.Select(attrs={'class':'form-group custom-select'}),
				choices = PRODUCT_QUANTITY_CHOICES,
				coerce = int) #corec to convert input into integer
	override = forms.BooleanField(
				required=False,initial=False,
				widget=forms.HiddenInput)
