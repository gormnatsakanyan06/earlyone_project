from django.urls import path
from . import views

urlpatterns = [
    path('', views.category_detail_view, {'category_slug': 'finance'}, name='home'),
   
    # Sector Detail (e.g., /category/finance/)
    path('category/<slug:category_slug>/', views.category_detail_view, name='category_detail'),
    
    # Provider Branches (e.g., /provider/ameria/)
    path('provider/<slug:provider_slug>/', views.branch_list_view, name='branch_list'),
    
    # Branch Services/Actions (e.g., /provider/ameria/sayat-nova/actions/)
    path('provider/<slug:provider_slug>/<slug:branch_slug>/actions/', views.action_list_view, name='action_list'),
]