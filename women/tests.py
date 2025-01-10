from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from women.models import Women


# Create your tests here.

class GetPagesTestCase(TestCase):
    fixtures = ['women_women.json', 'women_category.json',
                'women_husband.json', 'women_tagpost.json',
                'user_user.json']

    def setUp(self):
        pass

    def test_mainpage(self):
        path = reverse('index')
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'women/index.html')
        self.assertEqual(response.context_data['title'], 'Main page')

    def test_redirect_addpage(self):
        path = reverse('add_page')
        redirect_uri = reverse('users:login') + '?next=' + path
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, redirect_uri)

    def test_data_mainpage(self):
        w = Women.published.all().select_related('cat')
        path = reverse('index')
        response = self.client.get(path)
        self.assertQuerySetEqual(response.context_data['posts'], w[:5])
        print(w)

    def test_paginate_mainpage(self):
        path = reverse('index')
        page = 2
        paginate_by = 5
        response = self.client.get(path + f'?page={page}')
        w = Women.published.all().select_related('cat')
        self.assertQuerySetEqual(response.context_data['posts'], w[(page-1) * paginate_by:page * paginate_by])

    def test_content_post(self):
        w = Women.published.first()
        path = reverse('post', args=[w.slug])
        response = self.client.get(path)
        self.assertEqual(w.content, response.context_data['post'].content)

    def tearDown(self):
        pass
