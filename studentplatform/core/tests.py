from django.test import TestCase
from django.contrib.auth.models import User
# Create your tests here.
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
class SignupViewTests(TestCase):

    def test_signup_view(self):
        url = reverse('signup')
        data = {
            'username': 'testuser',
            'password1': 'abcd123456',
            'password2': 'abcd123456',
            'email': 'test@example.com'
        }
        response = self.client.post(url, data)

        self.assertTrue(get_user_model().objects.filter(username='testuser').exists())

        self.assertRedirects(response, reverse('profile'))

        def test_successful_signup(self):
            """Test that a user can sign up successfully with valid data."""
            url = reverse('signup')
            data = {
                'username': 'newuser',
                'email': 'newuser@example.com',
                'password1': 'testpassword123',
                'password2': 'testpassword123',
            }
            response = self.client.post(url, data)
            self.assertEqual(User.objects.count(), 1)
            self.assertEqual(User.objects.first().username, 'newuser')

        def test_signup_with_invalid_data(self):

            url = reverse('signup')
            data = {
                'username': 'user',
                'email': 'user@example.com',
                'password1': 'testpassword',
                'password2': 'testpassword',
            }
            response = self.client.post(url, data)
            self.assertEqual(User.objects.count(), 0)

        def test_redirect_after_successful_signup(self):

            url = reverse('signup')
            data = {
                'username': 'newuser',
                'email': 'newuser@example.com',
                'password1': 'testpassword123',
                'password2': 'testpassword123',
            }
            response = self.client.post(url, data)
            self.assertRedirects(response, reverse('profile'))
