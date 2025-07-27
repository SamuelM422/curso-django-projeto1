from unittest import TestCase
from django.test import TestCase as DjangoTestCase
from django.urls import reverse
from django.contrib.messages import get_messages
from authors.forms.register_form import RegisterForm

class AuthorRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self):
        self.form_data = {
            'username': 'user',
            'first_name': 'first',
            'last_name': 'last',
            'email': 'email@anyemail.com',
            'password': 'Str0ngP@ssword1',
            'password2': 'Str0ngP@ssword1'
        }

        return super().setUp()

    def test_form_must_be_valid(self):
        url = reverse('authors:register_create')
        response = self.client.post(url, self.form_data, follow=True)
        messages = [m.message for m in list(get_messages(response.wsgi_request))]
        self.assertIn('Account created successfully', messages)

    def test_fields_cannot_be_empty(self):
        fields = (
            ('username', 'This field is required.'),
            ('first_name', 'Please enter your first name.'),
            ('last_name', 'Please enter your last name.'),
            ('password', 'Please enter your password.'),
            ('password2', 'Please enter your password again.'),
            ('email', 'Please enter your email address.'),
        )

        url = reverse('authors:register_create')

        for field, error_msg in fields:
            with self.subTest(field=field, error_msg=error_msg):
                self.form_data[field] = ''
                response = self.client.post(url, self.form_data, follow=True)
                self.assertIn(error_msg, response.context['form'].errors.get(field, ''))

    def test_username_field_min_length_should_be_4(self):
        self.form_data['username'] = 'us'
        url = reverse('authors:register_create')
        response = self.client.post(url, self.form_data, follow=True)
        self.assertIn('Ensure this value has at least 4 characters.',
                      response.context['form'].errors.get('username', ''))

    def test_username_field_max_length_should_be_65(self):
        self.form_data['username'] = 'A' * 66
        url = reverse('authors:register_create')
        response = self.client.post(url, self.form_data, follow=True)
        self.assertIn('Ensure this value has at most 65 characters.',
                      response.context['form'].errors.get('username', ''))

    def test_password_field_have_lower_upper_case_letters_and_numbers(self):
        url = reverse('authors:register_create')
        self.form_data['password'] = 'weakpassword'
        response = self.client.post(url, self.form_data, follow=True)
        self.assertIn('Password must have at least one uppercase letter, one lowercase letter and one number. '
                      'The length should be at least 8 characters.',
                      response.context['form'].errors.get('password', ''))

    def test_password_and_confirmation_must_be_equal(self):
        url = reverse('authors:register_create')
        self.form_data['password2'] = 'Str0ngP@ssword2'
        response = self.client.post(url, self.form_data, follow=True)
        self.assertIn('Passwords do not match',
                      response.context['form'].errors.get('password2', ''))

    def test_send_get_request_to_registration_create_view_returns_404(self):
        url = reverse('authors:register_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_create_user_with_email_that_already_exists(self):
        url = reverse('authors:register_create')
        self.client.post(url, self.form_data, follow=True)
        response = self.client.post(url, self.form_data, follow=True)
        self.assertIn('This email address is already in use.',
                      response.context['form'].errors.get('email', ''))

    def test_user_created_can_login(self):
        url = reverse('authors:register_create')
        self.client.post(url, self.form_data, follow=True)
        response = self.client.login(username=self.form_data['username'], password=self.form_data['password'])
        self.assertTrue(response)

class AuthorRegisterFormUnitTest(TestCase):
    def test_fields_placeholder_are_correct(self):
        form = RegisterForm()

        fields = (
            ('first_name', 'Ex.: John'),
            ('email', 'Your e-mail address'),
            ('username', 'Type your username here'),
            ('last_name', 'Ex.: Doe'),
            ('password', 'Your password here'),
            ('password2', 'Please enter your password again.'),
        )

        for field, placeholder_str in fields:
            with self.subTest(field=field, placeholder_str=placeholder_str): # type: ignore
                placeholder = form[field].field.widget.attrs['placeholder']
                self.assertEqual(placeholder, placeholder_str)

    def test_password_help_text_is_correct(self):
        form = RegisterForm()
        password_help_text = form['password'].field.help_text
        self.assertEqual(password_help_text, 'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.')

    def test_labels_are_correct(self):
        form = RegisterForm()
        fields = (
            ('first_name', 'First Name'),
            ('last_name', 'Last Name'),
            ('username', 'Username'),
            ('email', 'Email'),
            ('password', 'Password'),
        )

        for field, label in fields:
            with self.subTest(field=field, label=label):
                self.assertEqual(form[field].field.label, label)