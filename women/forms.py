from django import forms
from django.core.exceptions import ValidationError
from .models import Women
from .models import Category, Husband
from captcha.fields import CaptchaField


class AddPostForm(forms.ModelForm):
    cat = forms.ModelChoiceField(queryset=Category.objects.all(),
                                 empty_label='Not specified',
                                 label='Category')
    husband = forms.ModelChoiceField(queryset=Husband.objects.filter(woman__husband__isnull=False),
                                     empty_label='Not married',
                                     required=False)

    class Meta:
        model = Women
        fields = ['title', 'content', 'photo', 'cat', 'husband', 'is_published']
        widgets = {'title': forms.TextInput(attrs={'class': 'form-input'}),
                   'content': forms.Textarea(attrs={'cols': 30, 'form-input': 30})}

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise ValidationError('Длина превышает 50 символов')

        return title


class UploadFileForm(forms.Form):
    file = forms.ImageField(label='File')


class ContactForm(forms.Form):
    name = forms.CharField(label='Name', max_length=255)
    email = forms.EmailField(label='E-mail')
    content = forms.CharField(label='Message', widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))
    captcha = CaptchaField()
