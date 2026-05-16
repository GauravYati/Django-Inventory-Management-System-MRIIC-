from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import BorrowRequest, Item, Category

# Create your forms here.

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user


class ItemForm(forms.ModelForm):
    category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-select category-select', 'size': 6}),
        required=True,
    )

    class Meta:
        model = Item
        fields = ['name', 'category', 'item_img', 'item_qty', 'featured', 'item_desc', 'tags']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Resource name'}),
            'item_qty': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'featured': forms.CheckboxInput(attrs={'class': 'feature-input'}),
            'item_desc': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Short description, usage notes, location, or constraints'}),
            'tags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'arduino, sensor, printer'}),
        }


class BorrowRequestForm(forms.ModelForm):
    class Meta:
        model = BorrowRequest
        fields = ['requester_name', 'requester_email', 'quantity', 'purpose']
        widgets = {
            'quantity': forms.NumberInput(attrs={'min': 1}),
            'purpose': forms.Textarea(attrs={'rows': 3}),
        }
