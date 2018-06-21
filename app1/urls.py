from django.urls import path
from app1 import views

# TEMPLATE TAGGING
app_name = 'app1'

urlpatterns = [
  path('logout', views.user_logout, name='logout'),
  path('special', views.special, name='special'),
  path('relative', views.relative, name='relative'),
  path('other', views.other, name='other'),
  path('user', views.user, name='user'),
  path('form_page', views.form_page, name='form_page'),
]
