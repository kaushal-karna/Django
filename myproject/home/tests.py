from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from courses.models import Course
from students.models import Student

User = get_user_model()


class DashboardTests(TestCase):
	def setUp(self):
		self.user = User.objects.create_user('member', password='test-password-123')
		self.staff = User.objects.create_user(
			'staff',
			password='test-password-123',
			is_staff=True,
		)

	def test_dashboard_requires_staff(self):
		response = self.client.get(reverse('home:admin_dashboard'))
		self.assertEqual(response.status_code, 302)

		self.client.force_login(self.user)
		response = self.client.get(reverse('home:admin_dashboard'))
		self.assertEqual(response.status_code, 302)

	def test_staff_can_view_dashboard(self):
		self.client.force_login(self.staff)
		response = self.client.get(reverse('home:admin_dashboard'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Admin Dashboard')

	def test_login_rejects_external_next_url(self):
		response = self.client.post(
			reverse('accounts:login') + '?next=https://example.com',
			{'username': 'member', 'password': 'test-password-123'},
		)
		self.assertRedirects(response, reverse('home:home_page'))


class ManagementSafetyTests(TestCase):
	def setUp(self):
		self.user = User.objects.create_user('manager', password='test-password-123')
		self.student = Student.objects.create(
			student_id='ST-001',
			first_name='Test',
			last_name='Student',
			email='student@example.com',
			date_of_birth='2000-01-01',
			department='Science',
			program='BSc',
			semester='Fall 2026',
		)

	def test_delete_student_requires_post(self):
		self.client.force_login(self.user)
		url = reverse('students:delete_student', args=[self.student.pk])
		response = self.client.get(url)
		self.assertEqual(response.status_code, 405)
		self.assertTrue(Student.objects.filter(pk=self.student.pk).exists())

	def test_course_form_rejects_missing_required_values(self):
		from courses.forms import CourseForm

		form = CourseForm({'code': 'CS-001'})
		self.assertFalse(form.is_valid())
		self.assertIn('name', form.errors)
