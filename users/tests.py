from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from users.models import Profile

User = get_user_model()


class SellerProfileViewTests(TestCase):
    def setUp(self):
        self.seller = User.objects.create_user(username="seller1", password="pass")
        self.seller_profile = Profile.objects.get(user=self.seller)
        self.seller_profile.role = Profile.Role.SELLER
        self.seller_profile.bio = "I sell great stuff."
        self.seller_profile.save()

        self.buyer = User.objects.create_user(username="buyer1", password="pass")
        # buyer profile is auto-created with role=buyer via signal

    def test_returns_seller_info(self):
        url = reverse("seller_profile", kwargs={"username": "seller1"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["username"], "seller1")
        self.assertEqual(response.context["bio"], "I sell great stuff.")
        self.assertIn("product_count", response.context)

    def test_product_count_is_integer(self):
        url = reverse("seller_profile", kwargs={"username": "seller1"})
        response = self.client.get(url)
        self.assertIsInstance(response.context["product_count"], int)

    def test_404_for_non_seller_user(self):
        url = reverse("seller_profile", kwargs={"username": "buyer1"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_404_for_nonexistent_user(self):
        url = reverse("seller_profile", kwargs={"username": "nobody"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
