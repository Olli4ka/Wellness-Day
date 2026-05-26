from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

ACTIVITY_CHOICES = [
    ('beginner', 'Beginner'),
    ('moderate', 'Moderate'),
    ('active', 'Active'),
    ('athlete', 'Athlete'),
]

DIET_CHOICES = [
    ('none', 'No Preference'),
    ('vegetarian', 'Vegetarian'),
    ('vegan', 'Vegan'),
    ('gluten_free', 'Gluten-Free'),
]

WORKSHOPS = [
    ('yoga', 'Morning Yoga'),
    ('nutrition', 'Healthy Nutrition'),
    ('stress', 'Stress Management'),
]


class RegistrationForm(forms.Form):
    full_name = forms.CharField(
        max_length=100,
        min_length=2,
        label='Full Name',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter your full name'
            }
        ),
        error_messages={
            'required': 'Please enter your full name',
            'min_length': 'Name must be at least 2 characters long',
            'max_length': 'Name must be at most 100 characters long'
        }
    )

    email = forms.EmailField(
        label='Email Address',
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email'
            }
        ),
        error_messages={
            'required': 'Please enter your email',
            'invalid': 'Please enter a valid email address. Example: example@domain.com'
        }
    )

    age = forms.IntegerField(
        min_value=18,
        max_value=100,
        label='Age',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter your age'
            }
        ),
        error_messages={
            'required': 'Please enter your age',
            'min_value': 'Age must be at least 18',
            'max_value': 'Age must be at most 100'
        }
    )

    phone_number = forms.CharField(
        label='Phone Number',
        validators=[
            RegexValidator(
                regex=r'^\+\d{10,15}$',
                message='Phone number must be in international format. Example: +49123456789'
            )
        ],
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '+49123456789'
            }
        ),
        error_messages={
            'required': 'Please enter your phone number'
        }
    )

    activity_level = forms.ChoiceField(
        label='Activity Level',
        choices=ACTIVITY_CHOICES,
        widget=forms.Select(
            attrs={
                'class': 'form-select'
            }
        ),
        error_messages={
            'required': 'Please select your activity level'
        }
    )

    dietary_preference = forms.ChoiceField(
        label='Dietary Preference',
        choices=DIET_CHOICES,
        required=False,
        widget=forms.Select(
            attrs={
                'class': 'form-select'
            }
        )
    )

    workshops = forms.MultipleChoiceField(
        choices=WORKSHOPS,
        widget=forms.CheckboxSelectMultiple,
        error_messages={
            'required': 'Please select at least one workshop.'
        }
    )

    motivation = forms.CharField(
        label='Motivation',
        min_length=20,
        help_text='Tell us why you want to attend the conference',
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Tell us why you want to attend the conference'
            }
        ),
        error_messages={
            'required': 'Please enter your motivation',
            'min_length': 'Motivation must be at least 20 characters long'
        }
    )

    agree_terms = forms.BooleanField(
        error_messages={
            'required': 'You must agree to the terms and conditions to submit the form'
        },
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input'
            }
        )
    )

    # ---------- CUSTOM VALIDATION ----------

    def clean_full_name(self):
        full_name = self.cleaned_data['full_name']

        words = full_name.strip().split()

        if len(words) < 2:
            raise ValidationError(
                'Please enter your first and last name.'
            )

        for word in words:
            if not word.isalpha():
                raise ValidationError(
                    'Name must contain letters only.'
                )

        return full_name

    def clean_motivation(self):
        motivation = self.cleaned_data['motivation']

        if motivation.strip() == '':
            raise ValidationError(
                'This field cannot contain only spaces.'
            )
        return motivation

    def clean(self):
        cleaned_data = super().clean()

        age = cleaned_data.get('age')
        activity_level = cleaned_data.get('activity_level')
        dietary_preference = cleaned_data.get('dietary_preference')
        workshops = cleaned_data.get('workshops')

        if age and activity_level:
            if age < 25 and activity_level == 'athlete':
                self.add_error(
                    'activity_level',
                    'Athlete level is available only for participants aged 25 or older.'
                )

        if activity_level == 'athlete' and dietary_preference == 'none':
            self.add_error(
                'dietary_preference',
                'Athlete participants must select a dietary preference for nutrition planning.'
            )

        if workshops and len(workshops) > 2:
            self.add_error(
                'workshops',
                "You can select a maximum of 2 workshops only."
            )

        return cleaned_data
