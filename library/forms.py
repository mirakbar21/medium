from django import forms
from .models import ReadingList
from django.contrib.auth import get_user_model

User = get_user_model()

class ReadingListForm(forms.ModelForm):
    class Meta:
        model = ReadingList
        fields = ['name']


class ReadingListSelectionForm(forms.Form):
    def __init__(self, *args, user=None, **kwargs):
        super(ReadingListSelectionForm, self).__init__(*args, **kwargs)
        if user is not None:
            choices = [(rl.id, rl.name) for rl in ReadingList.objects.filter(owner=user)]
            self.fields['reading_lists'] = forms.MultipleChoiceField(
                choices=choices,
                widget=forms.CheckboxSelectMultiple,
                required=True
            )