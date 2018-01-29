from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('getimagelist/',views.getImageList, name='getimagelist'),
    path('getmapid/',views.getMapId, name='getmapid'),
    path('getcorrectedmapid/',views.getCorrectedMapId, name='getcorrectedmapid')
]
