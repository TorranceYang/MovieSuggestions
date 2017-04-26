import hello.views
from django.conf.urls import include, url
from django.contrib import admin

admin.autodiscover()


# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^search/$', hello.views.search_movies, name='search'),
    url(r'^recommend/$', hello.views.generate_recommendation, name='recommend'),
    url(r'^$', hello.views.db, name='index'),
    url(r'^db', hello.views.db, name='db'),
    url(r'^admin/', include(admin.site.urls)),
]
