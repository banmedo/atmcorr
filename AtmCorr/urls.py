from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('getsrtm/',views.getSrtmMap, name='getsrtm'),
    path('getsomething/',views.getSomething, name='getsomething')
]
