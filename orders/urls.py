
from django.urls import path,include
from . import views

urlpatterns = [
    
    path('place_order/', views.place_order, name='place_order'),
    
    path('wallet_payments/<slug:order_id>', views.wallet_payments, name='wallet_payments'),
    path('payments/<slug:order_id>', views.payments, name='payments'),
    path('rozer_payments/<slug:order_id>', views.rozer_payments, name='rozer_payments'),
    path("callback/<slug:order_id>", views.callback, name="callback"),
    #path('proceed_to_pay/', views.razorpaycheck ),

    path('order_complete',views.order_complete, name='order_complete'),
    path('payment_cancel',views.payment_cancel, name='payment_cancel'),



    #path('download_invoice_pdf/', views.download_invoice_pdf, name='download_invoice_pdf'),
    #path('download_invoice_xls/', views.download_invoice_xls, name='download_invoice_xls'),
        
]