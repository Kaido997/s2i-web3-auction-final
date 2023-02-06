from django.test import TestCase, Client
from django.contrib.auth.models import User






class Authtentication_TestCase(TestCase):

    def setUp(self) -> None:
        self.c: Client= Client()

    def test_user_can_register(self) -> None:
        response = self.c.post(
            '/register/', {'username': 'test', 'psw': 'testpsw'}, follow=True)
        self.assertEqual(response.status_code, 200, f"Status code is {response.status_code} should be 200")
    

    def test_user_can_login(self) -> None:
        User.objects.create_user(username="test", password="testpsw")
        response = self.c.post(
            '', {'username': 'test', 'psw': 'testpsw'}, follow=True)
        self.assertEqual(response.status_code, 200, f"Status code is {response.status_code} should be 200")



# Create your tests here.
