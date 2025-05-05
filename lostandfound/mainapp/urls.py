from django.urls import path, include
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),

    path('', views.index, name='home'),
    path('items/', views.UnclaimedItems.as_view(), name='items'),
    path('items/<int:pk>', views.ItemDetailView.as_view(), name='item-detail'),
    path('report/', views.report, name='report'),
    path('search/', views.search, name='search'),
    path('item/<int:pk>/claim/', views.claim_item, name='claim-item'),
    path('profile/', views.profile, name='profile'),
    path('approve_claim/<int:claim_id>/', views.approve_claim, name='approve_claim'),
    path('reject_claim/<int:claim_id>/', views.reject_claim, name='reject_claim'),
]
