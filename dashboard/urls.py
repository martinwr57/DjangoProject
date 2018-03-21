from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from django.views.generic import list_detail
from dashboarding.models import Dellinqdata
import haystack
from haystack import urls
from haystack.forms import FacetedSearchForm
from haystack.query import SearchQuerySet
from haystack.views import FacetedSearchView
sqs = SearchQuerySet().facet('serialnumber_exact')

admin.autodiscover()


urlpatterns = patterns('dashboarding.views',
    (r'^dashboarding/$', 'index'),
    #(r'^dashboarding/(?P<modelnumber_id>\d+)/$', 'detail'),
    #(r'^dashboarding/(?P<modelnumber_id>\d+)/results/$', 'results'),
    #(r'^dashboarding/(?P<modelnumber_id>\d+)/vote/$', 'vote'),    
    #(r'^dashboarding/product_list/', 'product_list'),


    # Example:
    # (r'^dashboard/', include('dashboard.foo.urls')),
    #(r'^.*$', 'dashboarding.index'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
)

urlpatterns  += patterns('',                                              
    # Uncomment the next line to enable the admin:    
    (r'^admin/dashboarding/dellinqdata/report/$','dashboarding.admin_views.report' ),
    (r'^admin/dashboarding/systems/report/$','dashboarding.admin_views.sys_report' ),
    (r'^admin/dashboarding/device/report/(\w+),(\w+)/$','dashboarding.admin_views.device_report' ),
    (r'^admin/', include(admin.site.urls)),
    (r'^search/', include(haystack.urls)),


)
