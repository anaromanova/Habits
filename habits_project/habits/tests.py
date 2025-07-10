from django.test import SimpleTestCase

class SmokeTest(SimpleTestCase):
    def test_dummy(self):
        """Просто проверка, что тестовый раннер работает."""
        self.assertTrue(True)