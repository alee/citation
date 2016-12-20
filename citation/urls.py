from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import url
from django.views.generic import RedirectView, TemplateView

from . import views

app_name = 'citation'

# django rest framework endpoints that can generate JSON / HTML
urlpatterns = format_suffix_patterns([
    url(r'^publications/$', views.PublicationList.as_view(), name='publications'),
    url(r'^publication/(?P<pk>\d+)(?:/(?P<slug>[-\w\d]+))?/$', views.CuratorPublicationDetail.as_view(), name='publication_detail'),
    url(r'^notes/$', views.NoteList.as_view(), name='notes'),
    url(r'^note/(?P<pk>\d+)/$', views.NoteDetail.as_view(), name='note_detail'),
])

# non django rest framework endpoints for authentication, user dashboard, workflow, and search URLs
urlpatterns += [
    url(r'^publication/workflow/$', views.CuratorWorkflowView.as_view(), name='curator_workflow'),
    url(r'^search/$', views.CatalogSearchView.as_view(), name='haystack_search'),
    url(r'^search/platform/$', views.PlatformSearchView.as_view(), name="platform_search"),
    url(r'^search/sponsor/$', views.SponsorSearchView.as_view(), name="sponsor_search"),
    url(r'^search/tag/$', views.TagSearchView.as_view(), name="tag_search"),
    url(r'^search/journal/$', views.JournalSearchView.as_view(), name="journal_search"),
    url(r'^search/model-documentation/$', views.ModelDocumentationSearchView.as_view(), name="model_documentation_search"),
]