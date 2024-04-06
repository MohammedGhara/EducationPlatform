
from .models import Room, Message, Lecturer
from .forms import SignupStudent, SignupParent, SignupLecturer, Signupadmin
from django.test import TestCase, Client
from django.urls import reverse
from .models import Lecturer
from .forms import LecturerForm
import tempfile
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User, Group
import tempfile
import shutil
import os
from django.core.files import File
class UserModelTest(TestCase):
    def test_user_creation(self):
        user = User.objects.create_user(username='testuser', password='12345')
        self.assertEqual(User.objects.filter(username='testuser').exists(), True)

class RoomModelTest(TestCase):
    def test_room_creation(self):
        room = Room.objects.create(name="Test Room")
        self.assertEqual(Room.objects.filter(name="Test Room").exists(), True)

class MessageModelTest(TestCase):
    def setUp(self):
        Room.objects.create(name="Test Room")

    def test_message_creation(self):
        room = Room.objects.get(name="Test Room")
        message = Message.objects.create(value="Hello, World!", user="test_user", room=room.name)
        self.assertEqual(Message.objects.filter(value="Hello, World!").exists(), True)

class SignupViewTest(TestCase):
    def test_signup_student_view_status_code(self):
        response = self.client.get(reverse('signupstudent'))
        self.assertEqual(response.status_code, 200)

    def test_signup_lecturer_view_template_used(self):
        response = self.client.get(reverse('signuplecturer'))
        self.assertTemplateUsed(response, 'signuplecturer.html')


class LoginLogoutTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client = Client()

    def test_login_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('modelstudent'))
        self.assertEqual(response.status_code, 200)

    def test_logout_view(self):
        self.client.logout()
        response = self.client.get(reverse('loginstudent'))
        self.assertEqual(response.status_code, 200)

class AccessRestrictionTest(TestCase):
    def setUp(self):
        self.user_student = User.objects.create_user(username='studentuser', password='12345')
        student_group, _ = Group.objects.get_or_create(name='student')
        self.user_student.groups.add(student_group)

        self.client = Client()
        self.client.login(username='studentuser', password='12345')

    def test_student_access_restricted_view(self):
        response = self.client.get(reverse('modelstudent'))
        self.assertEqual(response.status_code, 200)


class SearchFunctionalityTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_search_redirect(self):
        # Assuming 'search' functionality redirects based on query to specific views
        response = self.client.get(reverse('search') + '?query=student')
        self.assertRedirects(response, reverse('modelstudent'), status_code=302, fetch_redirect_response=False)

        response = self.client.get(reverse('search') + '?query=parent')
        self.assertRedirects(response, reverse('modelparent'), status_code=302, fetch_redirect_response=False)

        response = self.client.get(reverse('search') + '?query=lecturer')
        self.assertRedirects(response, reverse('modellecturer'), status_code=302, fetch_redirect_response=False)

    def test_search_no_results(self):
        response = self.client.get(reverse('search') + '?query=unknown')
        self.assertIn("No results found for 'unknown'.", response.content.decode())



class LoginViewTest(TestCase):
    def setUp(self):

        self.test_user = User.objects.create_user(username='testuser', password='testpassword')
        self.test_user.save()

    def test_login_student_get(self):
        response = self.client.get(reverse('loginstudent'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'loginstudent.html')

    def test_login_student_post_success(self):
        response = self.client.post(reverse('loginstudent'), {'username': 'testuser', 'password': 'testpassword'})

        self.assertRedirects(response, reverse('modelstudent'))

    def test_login_student_post_failure(self):

        response = self.client.post(reverse('loginstudent'), {'username': 'testuser', 'password': 'wrongpassword'})
        self.assertRedirects(response, reverse('loginstudent'))

    def test_login_admin_get(self):

        response = self.client.get(reverse('loginadmin'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'loginadmin.html')

    def test_login_admin_post_success(self):

        response = self.client.post(reverse('loginadmin'), {'username': 'testuser', 'password': 'testpassword'})

        self.assertRedirects(response, 'http://127.0.0.1:8000/adminpage/', fetch_redirect_response=False)

    def test_login_admin_post_failure(self):
        response = self.client.post(reverse('loginadmin'), {'username': 'testuser', 'password': 'wrongpassword'})

        self.assertRedirects(response, reverse('loginadmin'))

    def tearDown(self):
        self.test_user.delete()


class IndexViewTest(TestCase):

    def setUp(self):

        self.client = Client()

    def test_index_get_request(self):

        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_index_post_request(self):

        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=True) as tmp:
            tmp.write(b'Some file content')
            tmp.seek(0)
            response = self.client.post(reverse('index'), {
                'name': 'Test Lecturer',
                'file': tmp
            }, follow=True)
        self.assertRedirects(response, reverse('index'))
        self.assertTrue(Lecturer.objects.exists())

    def test_index_file_url_in_context(self):

        lecturer = Lecturer.objects.create(name='Test Lecturer')
        response = self.client.get(reverse('index'))
        self.assertIsNone(response.context['file_url'])



class DownloadFileTest(TestCase):

    def setUp(self):

        self.client = Client()
        self.test_dir = tempfile.mkdtemp()


