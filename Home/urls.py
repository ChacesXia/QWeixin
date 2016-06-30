from django.conf.urls import url,include
from . import views
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^test.php', views.test, name='test'),
    url(r'^Addons/',include("AddonsBase.urls")),
    url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    # ex: /polls/5/results/
    url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
    # ex: /polls/5/vote/
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
]