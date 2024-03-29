from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group',)
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control', 'name': 'text', 'cols': '40',
                'rows': '10', 'required id': 'id_text'}
            ),
            'group': forms.Select(attrs={
                'name': 'group', 'class': 'form-control', 'id': 'id_group'}),
        }
