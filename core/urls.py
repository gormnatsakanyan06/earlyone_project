from django.urls import path
from .views import *

urlpatterns = [
    path("appointment/", appointment, name="appointment"),

    path('finance/', finance, name='finance'),

    path('government/', government, name='government'),

    path('telecom/', telecom, name='telecom'),

    path('utilitie/', utilitie, name='utilitie'),

    # --- Finance ---

    path('finance/<str:service_slug>/', bank_branches, name='branch_list'),
    path('finance/<str:service_slug>/<str:branch_name>/', bank_actions, name='bank_actions'),
    path('finance/<str:service_slug>/<str:branch_name>/<str:action_slug>/time/', 
         datetime_selection, name='datetime_selection'),
    path('finance/<str:service_slug>/<str:branch_name>/<str:action_slug>/<str:date>/<str:time>/ticket/', 
         generate_ticket, name='generate_ticket'),


    # --- Government  ---
    path('government/<str:service_slug>/', government_branches, name='government_branches'),
    path('government/<str:service_slug>/<str:branch_name>/actions/', 
         government_actions, name='government_actions'),
    path('government/<str:service_slug>/<str:branch_name>/<str:action_slug>/time/', 
         datetime_selection, name='gov_datetime_selection'),
    path('government/<str:service_slug>/<str:branch_name>/<str:action_slug>/<str:date>/<str:time>/ticket/', 
         generate_ticket, name='gov_generate_ticket'),

     # --- Telecom---
    path('telecom/<str:service_slug>/', telecom_branches, name='telecom_branches'),
    path('telecom/<str:service_slug>/<str:branch_name>/actions/', 
         telecom_actions, name='telecom_actions'),
    path('telecom/<str:service_slug>/<str:branch_name>/<str:action_slug>/time/', 
         datetime_selection, name='telecom_datetime_selection'),
    path('telecom/<str:service_slug>/<str:branch_name>/<str:action_slug>/<str:date>/<str:time>/ticket/', 
         generate_ticket, name='telecom_generate_ticket'),  

     # --- Utilities ---
    path('utility/<str:service_slug>/', 
         utility_branches, name='utility_branches'),
    
    path('utility/<str:service_slug>/<str:branch_name>/actions/', 
         utility_actions, name='utility_actions'),
    
    path('utility/<str:service_slug>/<str:branch_name>/<str:action_slug>/time/', 
         datetime_selection, name='utility_datetime_selection'),
    
    path('utility/<str:service_slug>/<str:branch_name>/<str:action_slug>/<str:date>/<str:time>/ticket/', 
         generate_ticket, name='utility_generate_ticket'),
       
  ]