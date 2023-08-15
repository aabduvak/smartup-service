from django.urls import path

from api.view import region, pay_details, auth, customer, payment, product

urlpatterns = [
    path('auth/login/', auth.AuthView.as_view(), name='login'),
    
    # Retrieve data from SmartUp
    path('create/regions/', region.CreateRegionsView.as_view()), # never use again
    path('create/cities/', region.CreateCitiesView.as_view()), # never use again
    path('create/districts/', region.CreateDistrictsView.as_view()), # never use again
    path('create/currencies/', pay_details.CreateCurrencyView.as_view()),
    path('create/payment-types/', pay_details.CreatePaymentTypeView.as_view()),
    path('create/customers/', customer.CreateUserView.as_view()), # never use again
    path('create/payments/', payment.CreatePaymentView.as_view()),
    path('create/products/', product.CreateProductView.as_view()),
    
    path('get/regions/', region.RegionListView.as_view(), name='regions'),
    path('get/cities/', region.CityListView.as_view(), name='cities'),
    path('get/districts/', region.DistrictListView.as_view(), name='districts'),
    path('get/currency/', pay_details.CurrencyListView.as_view(), name='currencies'),
    path('get/payment-types/', pay_details.PaymentTypeListView.as_view(), name='payment-types'),
    path('get/customers/', customer.UserListView.as_view(), name='customers'),
    path('get/customers/<str:smartup_id>/', customer.UserDetailView.as_view(), name='customer-detail'),
    path('get/payments/', payment.PaymentListView.as_view(), name='payment-list'),
    path('get/payments/<str:smartup_id>/', payment.PaymentDetailView.as_view(), name='payment-detail'),
]
