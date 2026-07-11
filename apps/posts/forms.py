from django import forms
from .models import Post, PostImage, PollOption


class PostForm(forms.ModelForm):

    # Hashtags field
    tags = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Add hashtags e.g python django coding",
                "class": "w-full rounded-xl border px-4 py-3"
            }
        ),
        help_text="Separate hashtags with spaces"
    )


    class Meta:

        model = Post

        fields = [
            "title",
            "content",
            "tags",
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
                    "placeholder": "Share something with the community... Use @username to mention someone",
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
                    "class": "w-full rounded-xl border px-4 py-3",
                    "accept": "video/*"
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



    def clean_tags(self):

        tags = self.cleaned_data.get("tags")

        if not tags:
            return []


        # Convert:
        # python django coding
        #
        # into:
        # ["python", "django", "coding"]

        tags = tags.replace("#", "")

        return [
            tag.strip()
            for tag in tags.split()
            if tag.strip()
        ]



    def clean(self):

        cleaned_data = super().clean()

        post_type = cleaned_data.get("post_type")


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


        if post_type == Post.PostType.VIDEO:

            if not cleaned_data.get("video"):
                self.add_error(
                    "video",
                    "Please upload a video."
                )


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
                    "multiple": True
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