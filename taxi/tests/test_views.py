from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from taxi.models import Manufacturer
from taxi_service.settings import AUTH_USER_MODEL

CARS_URL = reverse("taxi:car-list")
MANUFACTURER_URL = reverse("taxi:manufacturer-list")
DRIVERS_URL = reverse("taxi:driver-list")


class PublicCarTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_required(self):
        res = self.client.get(CARS_URL)

        self.assertNotEqual(res.status_code, 200)


class PublicManufacturerTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_required(self):
        res = self.client.get(MANUFACTURER_URL)

        self.assertNotEqual(res.status_code, 200)


class PublicDriverTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_required(self):
        res = self.client.get(AUTH_USER_MODEL)

        self.assertNotEqual(res.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='user',
            password='pwd123'
        )
        self.client.force_login(self.user)

    def test_manufacturer_login_required(self):
        Manufacturer.objects.create(
            name="BMW",
            country='Germany'
        )
        Manufacturer.objects.create(
            name="Ferrari",
            country='Italy'
        )
        res = self.client.get(MANUFACTURER_URL)

        manufacturers = Manufacturer.objects.all()

        self.assertEquals(res.status_code, 200)
        self.assertEquals(list(res.context["manufacturer_list"]), list(manufacturers))

    def test_user_login_required(self):
        res = self.client.get(DRIVERS_URL)

        self.assertEquals(res.status_code, 200)
        self.assertEquals(list(res.context["driver_list"]), [self.user])
