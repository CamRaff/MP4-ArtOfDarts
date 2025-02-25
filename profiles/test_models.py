from django.test import TestCase
from django.contrib.auth.models import User
from .models import UserProfile


class UserProfileModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.profile = UserProfile.objects.get(user=self.user)

    def test_user_profile_created(self):
        """ Test that a UserProfile is created when a new User is created. """
        self.assertIsInstance(self.profile, UserProfile)
        self.assertEqual(self.profile.user.username, 'testuser')

    def test_user_profile_str(self):
        """ Test the string representation of the UserProfile model. """
        self.assertEqual(str(self.profile), 'testuser')

    def test_user_profile_defaults(self):
        """ Test that default fields are set to None or empty."""
        self.assertIsNone(self.profile.full_name)
        self.assertIsNone(self.profile.default_phone_number)
        self.assertIsNone(self.profile.default_street_address1)
        self.assertIsNone(self.profile.default_street_address2)
        self.assertIsNone(self.profile.default_town_or_city)
        self.assertIsNone(self.profile.default_postcode)

    def test_create_or_update_user_profile_signal(self):
        """ Test that the signal
        does not overwrite existing UserProfile data.
        """
        self.profile.full_name = 'John Doe'
        self.profile.save()

        self.user.save()  # Trigger post_save

        updated_profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(updated_profile.full_name, 'John Doe')
