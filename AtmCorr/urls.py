from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('getimagelist/',views.getImageList, name='getimagelist'),
    path('getmapid/',views.getMapId, name='getmapid'),
    path('getcorrectedmapid/',views.getCorrectedMapId, name='getcorrectedmapid'),
    path('exportImage/',views.exportImage, name='exportImage'),
    path('auth/',views.auth, name='auth'),
    path('oauth2callback/', views.oauth2callback, name='oauth2callback')
]
