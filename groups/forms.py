from django.forms import ModelForm
from groups.models import Group, Member, Channel, Viewer


class GroupCreationForm(ModelForm):
    class Meta:
        model = Group
        fields = ["title", "description", "group_picture"]

    def __init__(self, *args, **kwargs):
        super(GroupCreationForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control mb-2'}

        self.fields['group_picture'].widget.attrs = {'class': 'form-control mb-2', 'type': 'file'}


class MemberCreationForm(ModelForm):
    class Meta:
        model = Member
        fields = []


class ViewerCreationForm(ModelForm):
    class Meta:
        model = Viewer
        fields = []


class ChannelCreationForm(ModelForm):
    class Meta:
        model = Channel
        fields = ['title', 'description', "channel_picture"]

    def __init__(self, *args, **kwargs):
        super(ChannelCreationForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control mb-2'}

        self.fields['channel_picture'].widget.attrs = {'class': 'form-control mb-2', 'type': 'file'}
