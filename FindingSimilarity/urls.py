from django.urls import path, include
import FindingSimilarity.views as views

urlpatterns = [
    path('', views.index, name="index")
]
