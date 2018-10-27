from django.conf import settings
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.homepage),
    url(r'^(\d{4})/([a-z]{3})/$', views.archive_month),

]

if settings.DEBUG:
    urlpatterns += [url(r'^debuginfo/$', views.debug) ,]

# the url /debuginfo/ will only be available if debug is set to true.


# in python regular expressions, syntax for named regular expression groups is (?P<name>pattern) where name 
# is the name of the group and patterns is some pattern to match

urlpatterns = [
    url(r'^reviews/2003/$', views.special_case_2003),
    url(r'^reviews/[0-9]{4})/$', views.year_archive),
    url(r'^reviews/[0-9]{4})/([0-9]{2})/$', views.month_archive),
    url(r'^reviews/([0-9]{4})/([0-9]{2})/([0-9]+)/$', views.review_detail),
    
    # /reviews/2003 would not match any of these patterns, because each pattern requires that the url end with a slash
    # to capture a value from url, just put parenthesis around it. No need for a leading slash. Every url already has that.

    # the 'r' in each reg expression string is optional but recommended. It tells python that a string is raw - that nothing
    # in the string should be escaped

    # the patterns are tested in order, btw!


]


# the above urlpattern list, written to use NAMED GROUPS
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^reviews/2003/$', views.special_case_2003),
    url(r'^reviews/(?P<year>[0-9]{4})/$', views.year_archive),
    url(r'^reviews/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?<<day>[0-9]{2})/$', views.review_detail),
    url(r'^alex/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/$', views.alex_detail),

]

# -----------------specifying default parameters for your view's arguments-----------
from django.conf.urls import url
from . import views

urlpatterns = [
    # both of these patterns point to same views, views.page
    url(r'^reviews/$', views.page),
    url(r'^reviews/page(?P<num>[0-9]+)/$', views.page),

]

#----------in views.py----------
def page(request, num="1"):
    # output the appropriate page of reviews entries according to num
    pass


# ----------------including other urlconfs----------------------
from django.conf.urls import include, url

urlpatterns = [
    url(r'^community/', include('django_website.aggregator_urls')),
    url(r'^contact/', include('django_website.contact.urls')),

]

# ---------including a list of extra url instances---------------
from django.conf.urls import include, url
from apps.main import views as main_views
from credit import views as credit_views

extra_patterns = [
    url(r'^reports/(?P<id>[0-9]+)/$', credit_views.report),
    url(r'^charge/$', credit_views.charge),

]

urlpatterns = [
    url(r'^$', main_views.homepage),
    url(r'^help/', include('apps.help.urls')),
    url(r'^credit/', include(extra_patterns)),

]

# another example showing how to write condensed url patterns
urlpatterns = [ 
    url(r'^(?P<page_slug>\w+)-(?P<page_id>\w+)/history/$', views.history), 
    url(r'^(?P<page_slug>\w+)-(?P<page_id>\w+)/edit/$', views.edit), 
    url(r'^(?P<page_slug>\w+)-(?P<page_id>\w+)/discuss/$', views.discuss), 
    url(r'^(?P<page_slug>\w+)-(?P<page_id>\w+)/permissions/$', views.permissions),
]

# instead of all this redundancy, we can write the above as:
urlpatterns = [
    url(r'^(?P<page_slug>\w+)-(?P<page_id>\w+)/', include([
        url(r'^history/$', views.history),
        url(r'^edit/$', views.edit),
        url(r'^discuss/$', views.discuss),
        url(r'^permissions/$', views.permissions),
            ]))


]

# in settings/urls/main.py
from django.conf.urls import include, url


urlpatterns = [
    url(r'^(?P<username>\w+)/reviews/', include('foo.urls.reviews')),

]

# in foo/urls/reviews.py
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.reviews.index),
    url(r'^archive/$', views.reviews.archive),

]

# -----------passing extra options to view functions ---------------------
from django.conf.urls import url    # url function contained in django.conf.urls.url()
from . import views

urlpatterns = [
    url(r'^reviews/(?P<year>[0-9]{4})/$', views.year_archive), {'foo': 'bar'}),

    # for a request to /reviews/2005/, django calls views.year_archive(request, year='2005', foo=bar)
    # this technique used in syndication framework to pass metadata and options to views




]

# ----------passing extra options to include-------------
from django.conf.urls import url, include

urlpatterns = [
    url(r'^reviews/', include('inner'), {'reviewid': 3}),


]

# inner.py
from django.conf.urls import url
from mysite import views


urlpatterns = [
     url(r'^archive/$', views.archive),
     url(r'^about/$', views.about),
]

# -----------the above is equivalent to-------------
# main.py
from django.conf.urls import include, url
from mysite import views


urlpatterns = [
    url(r'^reviews/', include('inner')),

]

# inner.py
from django.conf.urls import url

urlpatterns = [
    url(r'^archive/$', views.archive, {'reviewid': 3}),
    url(r'^about/$', views.about, {'reviewid': 3}),

]

#------------------------REVERSE RESOLUTION OF URLS IN DJANGO-----------------
# urls can be reversed :
# in templates using 'url' template tag
# in python code using django.core.urlresolvers.reverse() function
# in high level code for handling model instances using 'get_absolute_url' method

# example 1
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^reviews/([0-9]{4})/$', views.year_archive, name='reviews-year-archive'), # /reviews/yyyy/

]

# in the template
<a href="{% url 'reviews-year-archive' 2012 %}">2012 archive</a>

<ul>
    {% for yearvar in year_list %}
        <li><a href="{% url 'reviews-year-archive' yearvar %}">{{yearvar}} Archive </a></li>
    {% endfor %}
</ul>

# in python code
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect


def redirect_to_year(request):
    year = 2012
    return HttpResponseRedirect(reverse('reviews-year-archive', args=(year,)))  # just noticed this type of execution

#----------naming urlpatterns----------------
 # when you name your url patterns, make sure you use names that are unlikely to clash with another app's choice of names

    # eg. 'myapp-comment' instead of just 'comment'....this eliminates confusion if another app has 'comment' url too.

#---------------URL Namespaces------------------
# allow you to uniquely reverse named url patterns even if dif apps use the same URL names
# also allows you to reverse urls if multiple instances of an app are deployed

# django apps that make use of URL namespacing can be deployed more than once for a particular site

# eg django.contrib.admin has an 'AdminSite' class which allows you to easily deploy more than one instance of the admin

# a URL namespace comes with 2 different parts, both of which are strings

# application namespace --the name of the app that is being deployed
# instance namespace --identifies a specific instance of an application. Should be unique across your entire app

# eg the main index page of the admin app is referenced using "admin:index"
    # the namespace here is admin and named url is "index"

# nested namespaces like "members:reviews:index" ----look for a pattern named index inside namespace called reviews that is itself defined in top-level namespace members


#--------------reversing namespaced urls------------------
when given a namespaced url like "reviews: index" to resolve, django splits the name into parts and tries the following:

>>first, django looks for a matching app namespace ("reviews"), which yields a list of instances of the app
>>if current app is defined, django finds and returns the URLresolver for that instance
>>current app can be specified as an attribute on the request
>>apps that expect to have multiple deployments should set the "current_app" attribute on the request being processed
>>current app can also be found manually as an argument to reverse() function
>> if current_app = False, django looks for default app instance
>>default app instance is the instance that has am instance namespace matching app namespace eg. an instance of reviews called "reviews"
>>if there is no default app instance django picks the last deployed instance of the app
>> if provided namespace doesnt match app namespace in step 1, django attempts a direct lookup of the namespace
    as an instance namespace

# -----------URL namespaces of included URLconfs-----------------
1. you can provide the app and instance namespaces as arguments to include()
    eg. 
        url(r'^reviews/$', include('reviews.urls', namespace='author-reviews', app='reviews')),
        # this will include the URLS defined in reviews.urls into the app namespace "reviews" with 
        # instance namespace 'author-reviews

2. if you include a list of url() instances, the URLS contained in that object will be added to the global namespace.
    ie. (<list of url() instances>, <app namespace>, <instance namespace>)  # 3-tuple

    eg.
    from django.conf.urls import include, url
    from . import views

    reviews_patterns = [
        url(r'^$', views.IndexView.as_view(), name='index'),
        url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name="detail"),
    ]

    url(r'^reviews/', include((reviews_patterns, 'reviews', 'author-reviews'))),


eg. django admin is deployed as instances of AdminSite.
AdminSite objects have a urls attribute --a 3-tuple containing all patterns in the corresponding admin site,
    plus the app namespace "admin" and name of the admin instance. It is this urls attribute that you 
    include() in your project urlpatterns when you deploy an instance of django admin

# be sure to pass a tuple to include()

































































