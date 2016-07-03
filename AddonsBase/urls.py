from django.conf.urls import url,include
from .views import index
urlpatterns = [
url(r'^index/(?P<id>\d+)/',index,name='windex'),
url(r'^oucjw/',include('AddonOucJw.urls')) #/addon/oucjw/ - > oucjw
]