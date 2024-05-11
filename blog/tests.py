from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post
from django.contrib.auth.models import User

# Create your tests here.
class TestView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_trump = User.objects.create_user(username='trump', password='somepassword')
        self.user_obama = User.objects.create_user(username='obama', password='somepassword')

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

    def test_post_list(self):
        # 1.1 포스트 목록 페이지를 가져온다.
        response = self.client.get('/blog/')

        # 1.2 정상적으로 페이지가 로드된다.
        self.assertEquals(response.status_code, 200)

        # 1.3 페이지 타이틀은 'blog'이다.
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEquals(soup.title.text, 'Blog')

        self.navbar_test(soup)


        # 2.1 메인 영역에 게시물이 하나도 없다면
        self.assertEquals(Post.objects.count(), 0)

        # 2.2 '아직 게시물이 없습니다'라는 문구가 보인다.
        main_area = soup.find('div', id='main-area')
        self.assertIn('아직 게시물이 없습니다', main_area.text)

        # 3.1 게시물이 2개 있다면
        post_001 = Post.objects.create(
            title='첫 번째 포스트입니다.',
            content='Hello World. We are the world.',
            author=self.user_trump,
        )
        post_002 = Post.objects.create(
            title='첫 번째 포스트입니다.',
            content='1등이 전부는 아니잖아요?',
            author=self.user_obama,
        )
        self.assertEquals(Post.objects.count(), 2)

        # 3.2 포스트 목록 페이지를 새로고침 했을 때
        response = self.client.get('/blog/')
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEquals(response.status_code, 200)

        # 3.3 main area에 포스트 2개의 타이틀이 존재한다.
        main_area = soup.find('div', id='main-area')
        self.assertIn(post_001.title, main_area.text)
        self.assertIn(post_002.title, main_area.text)

        self.assertIn(self.user_trump.username.upper(), main_area.text)
        self.assertIn(self.user_obama.username.upper(), main_area.text)

        # 3.4 '아직 게시물이 없습니다'라는 문구는 더 이상 보이지 않는다.
        self.assertNotIn('아직 게시물이 없습니다', main_area.text)

    def test_post_detail(self):
        # 1.1 포스트가 하나 있다.
        post_001 = Post.objects.create(
            title='첫 번째 포스트입니다.',
            content='Hello World. We are the world.',
            author=self.user_trump,
        )

        # 1.2 그 포스트의 url은 '/blog/1'이다.
        self.assertEquals(post_001.get_absolute_url(), '/blog/1/')

        # 2. 첫 번째 포스트의 상세 페이지 테스트
        # 2.1 첫 번쨰 포스트의 url로 접근하면 정상적으로 동작한다.(status code: 200)
        response = self.client.get(post_001.get_absolute_url())
        self.assertEquals(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.navbar_test(soup)

        # 2.3 첫 번째 포스트의 제목이 웹 브라우저 탭 타이틀에 들어 있다.
        self.assertIn(post_001.title, soup.title.text)

        # 2.4 첫 번째 포스트의 제목이 포스트 영역에 있다.
        main_area = soup.find('div', id='main-area')
        post_area = main_area.find('div', id='post-area')
        self.assertIn(post_001.title, post_area.text)

        # 2.5 첫 번째 포스트의 작성자(autor)가 포스트 영역에 있다.(아직 구현할 수 없음)
        # 아직 작성 불가

        # 2.6 첫 번째 포스트의 내용(content)이 포스트 영역에 있다.
        self.assertIn(post_001.content, post_area.text)

        self.assertIn(self.user_trump.username.upper(), main_area.text)