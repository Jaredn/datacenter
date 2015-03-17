__author__ = 'jeff_dambly'

from django.conf.urls import patterns, url
from racklayout import views

urlpatterns = patterns('',
                      url(
                          regex=r'^$',
                          view=views.IndexView.as_view(),
                          name='index'
                      ),

                      url(
                          regex=r'dc/(?P<dcid>\d+)$',
                          view=views.RowView.as_view(),
                          name='dc'
                      ),
                      url(
                          regex=r'rack/(?P<racjid>\d+)$',
                          view=views.RackView.as_view(),
                          name='rack'
                      ),
)
