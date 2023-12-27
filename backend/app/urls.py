from django.urls import path
from . import views

urlpatterns = [
    path('puresnippets/', views.snippets_page, name='snippets-page'),
    # Include other URL patterns if needed
]
