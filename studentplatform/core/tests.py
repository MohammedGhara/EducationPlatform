
from .models import Room, Message, Lecturer
from .forms import SignupStudent, SignupParent, SignupLecturer, Signupadmin
from django.test import TestCase, Client
from django.urls import reverse
from .models import Lecturer
from .forms import LecturerForm
import tempfile

from django.contrib.auth.models import User, Group

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

class LoginFormTest(TestCase):
    def test_login_student_form_valid_data(self):
        form_data = {'username': 'testuser', 'password': '12345'}
        form = SignupStudent(data=form_data)
        self.assertTrue(form.is_valid())

class UserGroupTest(TestCase):
    def setUp(self):
        User.objects.create_user('testuser', password='12345')
        Group.objects.create(name='student')

    def test_add_user_to_group(self):
        user = User.objects.get(username='testuser')
        group = Group.objects.get(name='student')
        user.groups.add(group)
        self.assertIn(group, user.groups.all())

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




class AccessControlTest(TestCase):
    def setUp(self):
        self.student_user = User.objects.create_user(username='student', password='password')
        self.parent_user = User.objects.create_user(username='parent', password='password')
        self.lecturer_user = User.objects.create_user(username='lecturer', password='password')

        student_group, _ = Group.objects.get_or_create(name='student')
        parent_group, _ = Group.objects.get_or_create(name='parent')
        lecturer_group, _ = Group.objects.get_or_create(name='lecturer')

        self.student_user.groups.add(student_group)
        self.parent_user.groups.add(parent_group)
        self.lecturer_user.groups.add(lecturer_group)

        self.client = Client()

    def test_modelstudent_access(self):
        self.client.login(username='student', password='password')
        response = self.client.get(reverse('modelstudent'))
        self.assertEqual(response.status_code, 200)
        self.client.login(username='parent', password='password')
        response = self.client.get(reverse('modelstudent'))
        self.assertNotEqual(response.status_code, 200)

    def test_modelparent_access(self):
        self.client.login(username='parent', password='password')
        response = self.client.get(reverse('modelparent'))
        self.assertEqual(response.status_code, 200)
        self.client.login(username='student', password='password')
        response = self.client.get(reverse('modelparent'))
        self.assertNotEqual(response.status_code, 200)

    def test_modellecturer_access(self):
        self.client.login(username='lecturer', password='password')
        response = self.client.get(reverse('modellecturer'))
        self.assertEqual(response.status_code, 200)

        self.client.login(username='parent', password='password')
        response = self.client.get(reverse('modellecturer'))
        self.assertNotEqual(response.status_code, 200)


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





class IndexViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index_view_get(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertIsInstance(response.context['form'], LecturerForm)

    def test_index_view_post_success(self):
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp_file:
            post_data = {
                'name': 'Test Lecturer',
                'file': tmp_file
            }
            response = self.client.post(reverse('index'), post_data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Lecturer.objects.count(), 1)
        lecturer = Lecturer.objects.first()
        self.assertEqual(lecturer.name, 'Test Lecturer')

    def test_index_view_post_failure(self):
        response = self.client.post(reverse('index'), {'name': '', 'file': None})
        self.assertEqual(Lecturer.objects.count(), 0)
        self.assertFormError(response, 'form', 'name',
                             'This field is required.')




