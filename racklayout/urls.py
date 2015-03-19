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
                          regex=r'^dc/(?P<dcid>\d+)$',
                          view=views.RowView.as_view(),
                          name='dc'
                      ),
                      url(
                          regex=r'^rack/(?P<pk>\d+)$',
                          view=views.RackView.as_view(),
                          name='rack'
                      ),
                      url(
                          regex=r'^create/dc$',
                          view=views.CreateDc.as_view(),
                          name='createdc'
                      ),
                      url(
                          regex=r'^create/row/(?P<pk>\d+)$',
                          view=views.CreateRow.as_view(),
                          name='createrow'
                      ),
                      url(
                          regex=r'^create/rack/(?P<pk>\d+)$',
                          view=views.CreateRack.as_view(),
                          name='createrack'
                      ),
                      url(
                          regex=r'^create/asset/(?P<pk>\d+)/(?P<location>\d+)$',
                          view=views.CreateAsset.as_view(),
                          name='createasset'
                      ),
)
