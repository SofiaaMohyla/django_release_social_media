from django import forms

from posts.models import Post, Like, Comment, Repost


class PostCreationForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "description", "media"]

    def __init__(self, *args, **kwargs):
        super(PostCreationForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': "form-control mb-2"})

        self.fields["media"].widget.attrs.update({'class': "form-control mb-2", "type": "file"})


class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "description"]

    def __init__(self, *args, **kwargs):
        super(PostUpdateForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': "form-control mb-2"})


class LikeCreationForm(forms.ModelForm):
    class Meta:
        model = Like
        fields = []


class CommentCreationForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(attrs={'class': 'form-control mb-2'}),
        }


class RepostCreationForm(forms.ModelForm):
    class Meta:
        model = Repost
        fields = ["text"]
        widgets = {
            "text": forms.Textarea(attrs={'class': 'form-control mb-2'}),
        }

