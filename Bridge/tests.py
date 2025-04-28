from django.test import TestCase, Client
from django.urls import reverse
from .models import User, Course, Module

class ModelTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testteacher',
            email='teacher@test.com',
            password='testpassword'
        )
        
        # Create a test module
        self.module = Module.objects.create(
            title='Test Module',
            description='Test Description',
            content='Test Content',
            order=1
        )
        
        # Create a test course
        self.course = Course.objects.create(
            class_name='Test Class',
            teacher=self.user,
            location='Test Location',
            home_content='Test Home Content'
        )
        
        # Add the module to the course
        self.course.modules.add(self.module)
    
    def test_user_creation(self):
        """Test user creation"""
        self.assertEqual(self.user.username, 'testteacher')
        self.assertEqual(self.user.email, 'teacher@test.com')
        
    def test_module_creation(self):
        """Test module creation"""
        self.assertEqual(self.module.title, 'Test Module')
        self.assertEqual(self.module.description, 'Test Description')
        self.assertEqual(self.module.content, 'Test Content')
        self.assertEqual(self.module.order, 1)
        
    def test_course_creation(self):
        """Test course creation"""
        self.assertEqual(self.course.class_name, 'Test Class')
        self.assertEqual(self.course.teacher, self.user)
        self.assertEqual(self.course.location, 'Test Location')
        self.assertEqual(self.course.modules.count(), 1)
        self.assertEqual(self.course.modules.first(), self.module)

class ViewTests(TestCase):
    def setUp(self):
        # Create client
        self.client = Client()
        
        # Create a test user
        self.user = User.objects.create_user(
            username='testteacher',
            email='teacher@test.com',
            password='testpassword'
        )
        
        # Create a test course
        self.course = Course.objects.create(
            class_name='Test Class',
            teacher=self.user,
            location='Test Location'
        )
    
    def test_index_view(self):
        """Test the index view"""
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        
    def test_classes_view(self):
        """Test the classes view"""
        # Log in the user
        self.client.login(username='testteacher', password='testpassword')
        
        response = self.client.get(reverse('classes'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Class')
