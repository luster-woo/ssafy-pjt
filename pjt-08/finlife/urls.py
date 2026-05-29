from django.urls import path
from . import views

urlpatterns = [

    # F801
    path(
        'save-deposit-products/',
        views.save_deposit_products,
        name='save_deposit_products'
    ),

    # F802 + F803
    path(
        'deposit-products/',
        views.deposit_products,
        name='deposit_products'
    ),
    
    path(
        'top-rate/',
        views.top_rate,
        name='top_rate'
    ),
    # F804
    path(
        'deposit-product-options/<str:fin_prdt_cd>/',
        views.deposit_product_options,
        name='deposit_product_options'
    ),

    # F806

]