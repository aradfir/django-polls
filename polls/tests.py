from django.test import TestCase
from django.urls import reverse
# Create your tests here.
from .models import *


class QuestionModelTests(TestCase):
    def test_was_published_recently_old_q(self):
        time = (timezone.now() - timezone.timedelta(days=2)).date()
        old_q = Question(pub_date=time)
        self.assertFalse(old_q.was_published_recently())

    def test_was_published_recently_recent_q(self):
        time = (timezone.now()).date()
        old_q = Question(pub_date=time)
        self.assertTrue(old_q.was_published_recently())

    def test_was_published_recently_future_q(self):
        time = (timezone.now() + timezone.timedelta(days=2)).date()
        old_q = Question(pub_date=time)
        self.assertFalse(old_q.was_published_recently())


class DetailViewTest(TestCase):

    def test_details_non_existing_question(self):
        res = self.client.get(reverse('detail', args=(1,)))
        self.assertEqual(res.status_code, 404)

    def test_details_real_question(self):
        q = Question(text='AAA', pub_date=timezone.now().date())
        q.save()
        res = self.client.get(reverse('detail', args=(q.id,)))
        self.assertEqual(res.status_code, 200)
