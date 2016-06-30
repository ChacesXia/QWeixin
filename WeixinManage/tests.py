from django.test import TestCase
from django.core.urlresolvers import resolve
from WeixinManage.views import home_page
# Create your tests here.
class HomePageTest(TestCase):
    
    def test_root_url_to_home_page_view(self):
        found = resolve(r'/')
        self.assertEqual(found.func,home_page)
