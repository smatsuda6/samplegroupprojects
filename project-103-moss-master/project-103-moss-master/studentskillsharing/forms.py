from django import forms

from .models import Post, Comment, Profile


class UploadProfilePictureForm(forms.Form):
    profile_picture = forms.FileField()


class ProfilePrivacyForm(forms.Form):
    class Meta:
        model = Profile

        fields = ('profile_privacy',)

        widgets = {
            'profile_privacy': forms.ChoiceField(choices=['all', 'some', 'none'], widget=forms.RadioSelect),
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('post_title', 'post_text',)

        widgets = {
            'post_title': forms.TextInput(attrs={'placeholder': 'Enter title'}),
            'post_text': forms.Textarea(attrs={'placeholder': 'Enter post text', 'rows': 12, 'cols': 100,
                                               }),
        }


# Don't allow users to edit the title of a post
class EditPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('post_text',)
        widgets = {
            'post_text': forms.Textarea(attrs={'placeholder': 'Enter post text', 'rows': 12, 'cols': 100,
                                               }),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment_text',)
        widgets = {
            'comment_text': forms.Textarea(attrs={'rows': 1, 'cols': 87, 'placeholder': 'Reply to the post here'}),
        }


class ReplyCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment_text',)
        widgets = {
            'comment_text': forms.Textarea(attrs={'rows': 1, 'cols': 84, 'placeholder': 'Reply to the comment here'}),
        }