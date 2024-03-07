from django.test import TestCase

# Create your tests here.



# test for the parent
def test_template_used(self):
    response = self.client.get(reverse('signupparent'))
    self.assertTemplateUsed(response, 'signupparent.html')

def test_form_class(self):
    response = self.client.get(reverse('signupparent'))
    self.assertIsInstance(response.context['form'], SignupParentForm)ignupParentForm)


def test_model_used(self):
    self.assertEqual(SignupParent.model, User)


def test_view_success_status_code(self):
    response = self.client.get(reverse('signupparent'))
    self.assertEqual(response.status_code, 200)