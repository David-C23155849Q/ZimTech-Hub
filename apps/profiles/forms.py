from django import forms
from .models import Profile

class ProfileUpdateForm(forms.ModelForm):
    # Overriding widgets to maintain a consistent Tailwind look across all fields
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply Tailwind classes to all fields automatically
        for field in self.fields.values():
            if not isinstance(field.widget, (forms.CheckboxInput, forms.FileInput)):
                field.widget.attrs.update({'class': 'w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white'})
        
        # Convert list data from database back to comma-separated strings for the UI
        for field in ['skills', 'programming_languages', 'frameworks']:
            val = self.initial.get(field)
            if isinstance(val, list):
                self.initial[field] = ', '.join(val)

    class Meta:
        model = Profile
        fields = [
            'avatar', 'cover_image', 'bio', 'headline', 'country', 'city', 
            'skills', 'programming_languages', 'frameworks', 'experience_level', 
            'availability', 'github_url', 'linkedin_url', 'portfolio_url', 
            'website_url', 'twitter_url', 'cv', 'resume', 'is_public'
        ]
        # Hide the default labels if you want to use custom labels in the template
        labels = {
            'is_public': 'Make profile public',
        }

    def _clean_list_field(self, field_name):
        data = self.cleaned_data.get(field_name, '')
        if isinstance(data, list): return data
        return [s.strip() for s in data.split(',') if s.strip()] if data else []

    def clean_skills(self): return self._clean_list_field('skills')
    def clean_programming_languages(self): return self._clean_list_field('programming_languages')
    def clean_frameworks(self): return self._clean_list_field('frameworks')
    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            # Check file size (e.g., limit to 2MB)
            if avatar.size > 2 * 1024 * 1024:
                raise forms.ValidationError("Image file too large ( > 2mb )")
        return avatar