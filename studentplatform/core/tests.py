from django.test import TestCase, Client
from django.urls import reverse
from .models import Room, Message
from django.contrib.auth.models import User
from .forms import SignupStudent, SignupParent, SignupLecturer, Signupadmin
from django.contrib.auth.forms import UserCreationForm

# Models tests
class RoomModelTests(TestCase):
    def test_room_creation(self):
        room = Room.objects.create(name="Test Room")
        self.assertIs(isinstance(room, Room), True)
        self.assertEqual(room.name, "Test Room")

class MessageModelTests(TestCase):
    def test_message_creation(self):
        room = Room.objects.create(name="Test Room")
        message = Message.objects.create(value="Hello, world!", user="test_user", room="Test Room")
        self.assertIs(isinstance(message, Message), True)
        self.assertEqual(message.value, "Hello, world!")
        self.assertEqual(message.user, "test_user")
        self.assertEqual(message.room, "Test Room")

# Views tests
class SignupViewTests(TestCase):
    def test_signup_student_view(self):
        response = self.client.get(reverse('signupstudent'))
        self.assertEqual(response.status_code, 200)

    def test_signup_parent_view(self):
        response = self.client.get(reverse('signupparent'))
        self.assertEqual(response.status_code, 200)

# Form tests
class UserCreationFormTests(TestCase):
    def test_signup_student_form(self):
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        form = SignupStudent(data=data)
        self.assertTrue(form.is_valid())

    def test_signup_parent_form(self):
        data = {
            'username': 'testparent',
            'email': 'parent@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        form = SignupParent(data=data)
        self.assertTrue(form.is_valid())

# Testing authentication and redirection
class LoginTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_login_student(self):
        response = self.client.post('/loginstudent/', {'username': 'testuser', 'password': '12345'})
        self.assertRedirects(response, expected_url=reverse('modelstudent'), status_code=302, target_status_code=200)


# Additional Views tests
class LoginLogoutTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='user@test.com', password='testpass123')

    def test_login_view(self):
        response = self.client.post(reverse('loginstudent'), {'username': 'testuser', 'password': 'testpass123'})
        self.assertEqual(response.status_code, 302)  # Assuming redirection after login

    def test_logout_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('logout_user'))
        self.assertEqual(response.status_code, 302)  # Assuming redirection after logout

class ChatRoomTests(TestCase):
    def setUp(self):
        Room.objects.create(name="Test Room")

    def test_room_view(self):
        response = self.client.get(reverse('room', kwargs={'room': "Test Room"}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Room")

    def test_send_message(self):
        self.client.post(reverse('send'), {'message': "Hello", 'username': "testuser", 'room_id': "Test Room"})
        message = Message.objects.get(value="Hello")
        self.assertEqual(message.value, "Hello")

    def test_get_messages(self):
        room = Room.objects.create(name="New Test Room")
        Message.objects.create(value="Test Message", user="testuser", room=room.name)
        response = self.client.get(reverse('getMessages', kwargs={'room': room.name}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Message")

# Test class-specific and subject-specific views
class ClassAndSubjectViewsTests(TestCase):
    def test_class_view(self):
        response = self.client.get(reverse('class10'))
        self.assertEqual(response.status_code, 200)
        # Similar tests can be replicated for class11, class12, etc.

    def test_subject_view(self):
        response = self.client.get(reverse('algebrastudent'))
        self.assertEqual(response.status_code, 200)
        # Similar tests for calculusstudent and other subject-specific views

# HomePage and Administrative Views Tests
class HomePageAndViewTests(TestCase):
    def test_homepage_view(self):
        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)

    def test_admin_page_view(self):
        self.user = User.objects.create_superuser('adminuser', 'admin@test.com', 'adminpass123')
        self.client.login(username='adminuser', password='adminpass123')
        response = self.client.get(reverse('adminpage'))
        self.assertEqual(response.status_code, 200)



class ViewTests(TestCase):
    def setUp(self):
        # Setting up for tests that require authenticated user
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.room = Room.objects.create(name="Test Room")
        self.message = Message.objects.create(value="Test Message", user="testuser", room="Test Room")
        self.login = self.client.login(username='testuser', password='12345')

    def test_model_lecturer_view(self):
        response = self.client.get(reverse('modellecturer'))
        self.assertEqual(response.status_code, 200)

    def test_calculus_student_view(self):
        response = self.client.get(reverse('calculusstudent'))
        self.assertEqual(response.status_code, 200)

    def test_algebra_student_view(self):
        response = self.client.get(reverse('algebrastudent'))
        self.assertEqual(response.status_code, 200)

    def test_homepage_view(self):
        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_adminpage_view(self):
        response = self.client.get(reverse('adminpage'))
        self.assertEqual(response.status_code, 200)

    def test_room_view(self):
        response = self.client.get(reverse('room', kwargs={'room': self.room.name}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.room.name)

    def test_checkview_view_post_exists(self):
        response = self.client.post(reverse('checkview'), {'room_name': self.room.name, 'username': 'testuser'})
        self.assertEqual(response.status_code, 302)  # Redirects if room exists

    def test_checkview_view_post_new(self):
        response = self.client.post(reverse('checkview'), {'room_name': 'New Room', 'username': 'testuser'})
        self.assertEqual(response.status_code, 302)  # Redirects if room is created

    def test_send_message_view(self):
        response = self.client.post(reverse('send'), {'message': 'Hello', 'username': 'testuser', 'room_id': self.room.id})
        self.assertEqual(response.status_code, 200)  # Message sent successfully

    def test_get_messages_view(self):
        response = self.client.get(reverse('getMessages', kwargs={'room': self.room.name}))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {"messages": [{"value": "Test Message", "user": "testuser", "room": "Test Room"}]})

    def test_search_view(self):
        response = self.client.get(reverse('search'))
        self.assertEqual(response.status_code, 200)