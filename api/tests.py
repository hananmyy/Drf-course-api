from django.test import TestCase
from api.models import Order, User
from django.urls import reverse
from rest_framework import status

# Create your tests here.

class UserOrderTestCast(TestCase):
    def setUp(self):
        user1 = User.objects.create_user(username='user1', password='testpass123')
        user2 = User.objects.create_user(username='user2', password='testpass123')
        Order.objects.create(user=user1)
        Order.objects.create(user=user1)
        Order.objects.create(user=user2) 
        Order.objects.create(user=user2)

    def test_user_order_endpoint_retrieves_only_authenticated_user_orders(self):
        user = User.objects.get(username='user2')
        self.client.force_login(user) # login user
        response = self.client.get(reverse('user-orders')) #send request to user-orders endpoint

        assert response.status_code == status.HTTP_200_OK  # Check that the response is OK
        orders = response.json()
        self.assertTrue(all(order['user'] == user.id for order in orders)) # check that all orders belong to the authenticated user


    def test_user_order_list_unauthenticated(self):
        response = self.client.get(reverse('user-orders'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Check that unauthenticated access is forbidden