from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from watchlist.api import serializers
from watchlist import models

# Create your tests here.
class StreamPlatformTestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username= "testuser", password = "testpassword")
        self.token = Token.objects.get(user__username = self.user)
        self.client.credentials(HTTP_AUTHORIZATION = "Token "+self.token.key)
        
        self.platform = models.StreamPlatform.objects.create(name="Ullu", about="Ullu originals", website = "http://ullu.com")
        
    def test_stream_platform_create(self):
        url = reverse("stream-platform")
        data = {
            "name": "Ullu",
            "about": "No 1 streaming platform",
            "website": "http://ullu.com"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_stream_platform_list(self):
        url = reverse("stream-platform")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_stream_platform_detail(self):
        url = reverse("stream-detail", kwargs={"id": self.platform.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_stream_platform_update(self):
        url = reverse("stream-detail", kwargs={"id": self.platform.id})
        data = {
            "name": "Ullu (Updated)",
            "about": "Ullu originals (Updated)",
            "website": "http://ullu.com/updated"
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
class WatchlistTestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username = 'testuser', password = 'testpassword')
        self.token = Token.objects.get(user__username = self.user)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token '+ self.token.key)
        self.stream = models.StreamPlatform.objects.create(name="Nova OTT", about="We built the dreams", website="https://www.novaott.in")
        self.watchlist = models.WatchList.objects.create(
            title = "dummy store",
            platform = self.stream,
            storyline = "dummy storyline",
            active = True,
        )
        
    def test_watchlist_create(self):
        url = reverse('movie-list')
        data = {
            "platform": self.stream,
            "title": "A computer science film",
            "storyline": "new movie series",
            "active": True,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_watchlist_list(self):
        url = reverse('movie-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_watchlist_detail(self):
        url = reverse('movie-details', kwargs={'id': self.watchlist.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.WatchList.objects.count(), 1)
        self.assertEqual(models.WatchList.objects.get().title, 'dummy store')
        
        
class ReviewTestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username = 'testuser', password = 'testpassword')
        self.token = Token.objects.get(user__username = self.user)
        self.client.credentials(HTTP_AUTHORIZATION = 'Token '+ self.token.key)
        self.stream = models.StreamPlatform.objects.create(name="Nova OTT", about="We built the dreams", website="https://www.novaott.in")
        self.watchlist = models.WatchList.objects.create(
            title = "dummy store",
            platform = self.stream,
            storyline = "dummy storyline",
            active = True,
        )
        self.watchlist2 = models.WatchList.objects.create(
            title = "dummy store2",
            platform = self.stream,
            storyline = "dummy storyline",
            active = True,
        )
        self.review = models.Review.objects.create(
            review_user = self.user,
            watchlist = self.watchlist2,
            rating = 5,
            description = "dummy review description",
            active = True,)
        
    def test_review_create(self):
        url = reverse('review-create', kwargs={'pk': self.watchlist.pk})
        data = {
            "review_user": self.user,
            "watchlist": self.watchlist,
            "rating": 5,
            "description": "dummy review description",
            "active": True,
        }
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_review_create_unauthorized(self):
        url = reverse('review-create', kwargs={'pk': self.watchlist.pk})
        data = {
            "review_user": self.user,
            "watchlist": self.watchlist,
            "rating": 5,
            "description": "dummy review description",
            "active": True,
        }
        self.client.force_authenticate(user=None)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_review_update(self):
        url = reverse('review-detail', kwargs={'pk': self.review.id})
        data = {
            "review_user": self.user,
            "watchlist": self.watchlist,
            "rating": 4,
            "description": "dummy review description updated",
            "active": True,
        }
        
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_review_get_all_reviews(self):
        url = reverse('review-list', kwargs={'pk': self.watchlist.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_review_filter(self):
        url = "/movie/reviews/?username"+ self.user.username
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)