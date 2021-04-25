from django.urls import path

from . import views

urlpatterns = [
    path('getTextEmotionScore/', views.getTextEmotionScore, name='getTextEmotionScore'),
    path('getKeyWord/',views.getKeyWord, name='getKeyWord'),
    path('test/', views.test, name="test"),
]