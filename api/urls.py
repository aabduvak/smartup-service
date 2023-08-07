from django.urls import path
from api import views
from api.view.region import RegionListView, CityListView, DistrictListView

urlpatterns = [
    path('auth/login/', views.AuthView.as_view()),
    path('regions/', RegionListView.as_view()),
    path('cities/', CityListView.as_view()),
    path('districts/', DistrictListView.as_view()),
    # path('create-regions/', views.CreateRegionsView.as_view()), # never use again
    # path('create-cities/', views.CreateCitiesView.as_view()), # never use again
    # path('create-districts/', views.CreateDistrictsView.as_view())
]
