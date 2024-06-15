from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Contact

# Create your tests here.
class TestView(TestCase):
    def setUp(self):
        self.client = Client()

    def navbar_test(self, soup):
        navbar = soup.nav

        self.assertIn('Blog', navbar.text)
        self.assertIn('About Me', navbar.text)

        logo_btn = navbar.find('a', text='Do It Django')
        self.assertEqual(logo_btn.attrs['href'], '/')

        home_btn = navbar.find('a', text='Home')
        self.assertEqual(home_btn.attrs['href'], '/')

        blog_btn = navbar.find('a', text='Blog')
        self.assertEqual(blog_btn.attrs['href'], '/blog/')

        about_me_btn = navbar.find('a', text='About Me')
        self.assertEqual(about_me_btn.attrs['href'], '/about_me/')

    def test_create_contact(self):
        self.assertEqual(Contact.objects.count(), 0)
        contact_001 = Contact.objects.create(
            name='obama',
            email='1234@abc.abc',
            phone='01012341234',
            service='후원',
            message='가나다라',
            from_value='10000',
            to_value='60000'
        )

        contact_002 = Contact.objects.create(
            name='trump',
            email='5678@abc.abc',
            phone='01012345678',
            service='후원2',
            message='가나다라2',
            from_value='100000',
            to_value='600000'
        )

        contact_003 = Contact.objects.create(
            name='홍길동',
            email='1234555@abc.abc',
            phone='01044444444',
            service='고용 제안',
            message='test',
            from_value='150000',
            to_value='650000'
        )

        self.assertEqual(Contact.objects.count(), 3)
        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.navbar_test(soup)

