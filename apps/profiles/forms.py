from django import forms
from .models import Profile


class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile

        fields = [
            "avatar",
            "cover_image",
            "bio",
            "headline",
            "country",
            "city",
            "skills",
            "programming_languages",
            "frameworks",
            "experience_level",
            "availability",
            "github_url",
            "linkedin_url",
            "portfolio_url",
            "website_url",
            "twitter_url",
            "cv",
            "resume",
            "is_public",
        ]

        labels = {
            "avatar": "Profile Picture",
            "cover_image": "Cover Image",
            "bio": "About You",
            "headline": "Professional Headline",
            "skills": "Skills",
            "programming_languages": "Programming Languages",
            "frameworks": "Frameworks",
            "is_public": "Make profile public",
        }


    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)


        # Tailwind styling
        for name, field in self.fields.items():

            if isinstance(
                field.widget,
                (
                    forms.FileInput,
                    forms.CheckboxInput
                )
            ):
                continue


            field.widget.attrs.update({

                "class":
                "w-full px-4 py-3 rounded-lg "
                "border border-gray-300 "
                "dark:border-gray-600 "
                "dark:bg-gray-700 "
                "dark:text-white "
                "focus:ring-2 "
                "focus:ring-blue-500",

            })


        # File inputs
        self.fields["avatar"].widget.attrs.update({

            "class":
            "block w-full text-sm text-gray-500 "

        })


        self.fields["cover_image"].widget.attrs.update({

            "class":
            "block w-full text-sm text-gray-500"

        })


        self.fields["cv"].widget.attrs.update({

            "class":
            "block w-full text-sm text-gray-500"

        })


        self.fields["resume"].widget.attrs.update({

            "class":
            "block w-full text-sm text-gray-500"

        })


        # Convert JSON arrays back to text

        for field in [
            "skills",
            "programming_languages",
            "frameworks"
        ]:

            value = self.initial.get(field)


            if isinstance(value, list):

                self.initial[field] = ", ".join(value)



    def clean_skills(self):

        return self.clean_list_field("skills")


    def clean_programming_languages(self):

        return self.clean_list_field(
            "programming_languages"
        )


    def clean_frameworks(self):

        return self.clean_list_field(
            "frameworks"
        )


    def clean_list_field(self, field):

        data = self.cleaned_data.get(field)


        if isinstance(data, list):

            return data


        if not data:

            return []


        return [
            item.strip()
            for item in data.split(",")
            if item.strip()
        ]



    def clean_avatar(self):

        avatar = self.cleaned_data.get("avatar")


        if avatar:

            if avatar.size > 2 * 1024 * 1024:

                raise forms.ValidationError(
                    "Avatar size cannot exceed 2MB."
                )


        return avatar



    def clean_cover_image(self):

        cover = self.cleaned_data.get(
            "cover_image"
        )


        if cover:

            if cover.size > 5 * 1024 * 1024:

                raise forms.ValidationError(
                    "Cover image cannot exceed 5MB."
                )


        return cover