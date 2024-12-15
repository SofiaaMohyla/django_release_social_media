from django import forms
from profiles.models import Profile, Subscriber, Friendship
from requests.models import FriendRequest


class ProfileCreationForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['pfp', 'username', 'bio', 'status', 'banner']

    def __init__(self, *args, **kwargs):
        super(ProfileCreationForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': "form-control mb-2"})

        self.fields["pfp"].widget.attrs.update({'class': "form-control mb-2", 'type': "file"})
        self.fields["banner"].widget.attrs.update({'class': "form-control mb-2", 'type': "file"})


class SubscriptionCreationForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = []


class FriendRequestCreationForm(forms.ModelForm):
    class Meta:
        model = FriendRequest
        fields = []


class FriendshipCreationForm(forms.ModelForm):
    class Meta:
        model = Friendship
        fields = []


class SearchForm(forms.Form):
    search = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control mb-2'}), required=False,
                             label="Search by username")
