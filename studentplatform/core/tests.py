from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class SignupParentTestCase(TestCase):

    def test_view_exists(self):
        response = self.client.get(reverse('signupparent'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('signupparent'))
        self.assertTemplateUsed(response, 'signupparent.html')

    def test_view_uses_correct_form_class(self):
        response = self.client.get(reverse('signupparent'))
        self.assertIsInstance(response.context['form'], SignupParentForm)

    def test_model_used(self):
        self.assertEqual(SignupParent.model, User)
