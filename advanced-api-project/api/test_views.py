from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from .models import Author, Book

class BookAPITestCase(APITestCase):

    def setUp(self):
        # إنشاء مستخدم للاختبارات التي تحتاج توثيق
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()

        # إنشاء مؤلف واحد
        self.author = Author.objects.create(name="Test Author")

        # إنشاء كتب للاختبارات
        self.book1 = Book.objects.create(title="Book One", publication_year=2020, author=self.author)
        self.book2 = Book.objects.create(title="Book Two", publication_year=2021, author=self.author)

        # روابط الـ API
        self.list_url = reverse('book-list')           # GET list
        self.create_url = reverse('book-create')       # POST create
        self.detail_url = lambda pk: reverse('book-detail', args=[pk])  # GET detail
        self.update_url = lambda pk: reverse('book-update', args=[pk])  # PUT/PATCH update
        self.delete_url = lambda pk: reverse('book-delete', args=[pk])  # DELETE delete

    def test_list_books(self):
        # اختبار جلب قائمة الكتب بدون تسجيل دخول (يجب يسمح)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_filter_books_by_title(self):
        # فلترة كتب بعنوان "Book One"
        response = self.client.get(self.list_url, {'title': 'Book One'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Book One')

    def test_search_books(self):
        # البحث عن كتب تحتوي "Two" في العنوان
        response = self.client.get(self.list_url, {'search': 'Two'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Book Two')

    def test_ordering_books(self):
        # طلب الكتب مرتبة تنازليًا حسب سنة النشر
        response = self.client.get(self.list_url, {'ordering': '-publication_year'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['publication_year'], 2021)

    def test_create_book_unauthenticated(self):
        # محاولة إنشاء كتاب بدون تسجيل دخول (يجب يمنع)
        data = {
            "title": "New Book",
            "publication_year": 2023,
            "author": self.author.id
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_book_authenticated(self):
        # إنشاء كتاب مع تسجيل دخول
        self.client.login(username='testuser', password='testpass')
        data = {
            "title": "New Book",
            "publication_year": 2023,
            "author": self.author.id
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], "New Book")

    def test_update_book(self):
        # تحديث كتاب مع تسجيل دخول
        self.client.login(username='testuser', password='testpass')
        data = {"title": "Updated Title"}
        response = self.client.patch(self.update_url(self.book1.id), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Updated Title")

    def test_delete_book(self):
        # حذف كتاب مع تسجيل دخول
        self.client.login(username='testuser', password='testpass')
        response = self.client.delete(self.delete_url(self.book2.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book2.id).exists())
