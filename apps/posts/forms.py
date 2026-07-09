from django import forms
from .models import Post, PostImage, PollOption


class PostForm(forms.ModelForm):

    class Meta:
        model = Post

        fields = [
            "title",
            "content",
            "post_type",
            "video",
            "code_snippet",
            "language",
            "link_url",
            "link_title",
            "link_description",
            "link_image",
        ]

        widgets = {

            "title": forms.TextInput(
                attrs={
                    "placeholder": "Post title (optional)",
                    "class": "w-full rounded-xl border px-4 py-3"
                }
            ),


            "content": forms.Textarea(
                attrs={
                    "placeholder": "Share something with the community...",
                    "rows": 6,
                    "class": "w-full rounded-xl border px-4 py-3"
                }
            ),


            "post_type": forms.Select(
                attrs={
                    "class": "w-full rounded-xl border px-4 py-3"
                }
            ),


            "video": forms.FileInput(
                attrs={
                    "class": "w-full rounded-xl border px-4 py-3"
                }
            ),


            "code_snippet": forms.Textarea(
                attrs={
                    "placeholder": "Paste your code here...",
                    "rows": 10,
                    "class": "w-full rounded-xl border px-4 py-3 font-mono"
                }
            ),


            "language": forms.TextInput(
                attrs={
                    "placeholder": "Example: Python, Dart, JavaScript",
                    "class": "w-full rounded-xl border px-4 py-3"
                }
            ),


            "link_url": forms.URLInput(
                attrs={
                    "placeholder": "https://example.com",
                    "class": "w-full rounded-xl border px-4 py-3"
                }
            ),


            "link_title": forms.TextInput(
                attrs={
                    "placeholder": "Link title",
                    "class": "w-full rounded-xl border px-4 py-3"
                }
            ),


            "link_description": forms.Textarea(
                attrs={
                    "placeholder": "Describe the link...",
                    "rows": 3,
                    "class": "w-full rounded-xl border px-4 py-3"
                }
            ),


            "link_image": forms.URLInput(
                attrs={
                    "placeholder": "Preview image URL",
                    "class": "w-full rounded-xl border px-4 py-3"
                }
            ),

        }


    def clean(self):

        cleaned_data = super().clean()

        post_type = cleaned_data.get("post_type")


        # Require code fields
        if post_type == Post.PostType.CODE:

            if not cleaned_data.get("code_snippet"):
                self.add_error(
                    "code_snippet",
                    "Please provide your code."
                )


            if not cleaned_data.get("language"):
                self.add_error(
                    "language",
                    "Please specify the programming language."
                )


        # Require video

        if post_type == Post.PostType.VIDEO:

            if not cleaned_data.get("video"):
                self.add_error(
                    "video",
                    "Please upload a video."
                )


        # Require link

        if post_type == Post.PostType.LINK:

            if not cleaned_data.get("link_url"):
                self.add_error(
                    "link_url",
                    "Please provide the link URL."
                )


        return cleaned_data



class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class PostImageForm(forms.ModelForm):

    class Meta:

        model = PostImage

        fields = [
            "image"
        ]

        widgets = {

            "image": MultipleFileInput(
                attrs={
                    "class": "w-full rounded-xl border px-4 py-3",
                    "accept": "image/*",
                }
            )

        }


class PollOptionForm(forms.ModelForm):

    class Meta:

        model = PollOption

        fields = [
            "text"
        ]

        widgets = {

            "text": forms.TextInput(
                attrs={
                    "placeholder": "Poll option",
                    "class": "w-full rounded-xl border px-4 py-3"
                }
            )

        }