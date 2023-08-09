from django.urls import path

from api.view import region, pay_details, auth, customer

urlpatterns = [
    path('auth/login/', auth.AuthView.as_view()),
    
    # Retrieve data from SmartUp
    path('create/regions/', region.CreateRegionsView.as_view()), # never use again
    path('create/cities/', region.CreateCitiesView.as_view()), # never use again
    path('create/districts/', region.CreateDistrictsView.as_view()), # never use again
    path('create/currencies/', pay_details.CreateCurrencyView.as_view()),
    path('create/payments/', pay_details.CreatePaymentTypeView.as_view()),
    path('create/customers/', customer.CreateUserView.as_view()), # never use again
    
    path('get/regions/', region.RegionListView.as_view(), name='regions'),
    path('get/cities/', region.CityListView.as_view(), name='cities'),
    path('get/districts/', region.DistrictListView.as_view(), name='districts'),
    path('get/currency/', pay_details.CurrencyListView.as_view(), name='currencies'),
    path('get/payment-types/', pay_details.PaymentTypeListView.as_view(), name='payment-types'),
    path('get/customers/', customer.UserListView.as_view(), name='customers'),
]
