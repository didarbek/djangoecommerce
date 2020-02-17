from django import forms
from django.contrib.auth.models import User
from .models import Profile,Comment
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

PAYMENT_CHOICES = {
    ('S','Stripe'),
    ('P','PayPal'),
}

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'birth_date', 'website','city','country','organization','phone','avatar',)

class CheckoutForm(forms.Form):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    shipping_address = forms.CharField(required=False)
    shipping_address2 = forms.CharField(required=False)
    shipping_country = CountryField(blank_label='(select country)').formfield(required=False,widget=CountrySelectWidget(attrs={'class': 'custom-select d-block w-100'}))
    shipping_zip = forms.CharField(required=False)
    set_default_shipping = forms.BooleanField(required=False)
    use_default_shipping = forms.BooleanField(required=False)
    payment_option = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT_CHOICES)
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name','body',)
