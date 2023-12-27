from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('snippets', views.SnippetViweSet, basename='snippets')



urlpatterns = [
    # path('', views.index, name='index'),
    path('snippets/', views.snippet_list, name='snippet_list'),
    path('snippets/<int:id>/', views.detail_snippet, name='detail_snippet'),
]


urlpatterns += router.urls
