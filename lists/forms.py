from django import forms

from .models import MediaListRow, List
from accounts.models import CustomUser


class MediaListRowForm(forms.ModelForm):
    class Meta:
        model = MediaListRow
        fields = ('title', 'media_type')
        widgets = {
            'title': forms.TextInput(attrs={'id': 'media-title'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['media_type'].empty_label = None
        self.fields['media_type'].initial = 'movie'


class ListForm(forms.ModelForm):
    class Meta:
        model = List
        fields = ('name', 'contributors')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['contributors'].queryset = \
                    CustomUser.objects.exclude(id=user.id)
