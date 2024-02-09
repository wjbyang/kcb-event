from django.urls import path
from . import views

urlpatterns = [
    path('v1/user/', views.UserView.as_view(), name='user_post'),
    path('v1/user/<str:user_id>/', views.ViewUser.as_view(), name='user_get_one'),
    path('v1/users/', views.ViewUsers.as_view(), name='user_get_all'),
    path('v1/user/update/<str:user_id>/', views.UpdateUser.as_view(), name='user_update'),
    path('v1/user/delete/<str:user_id>/', views.ViewUser.as_view(), name='user_delete'),
    path('v1/organization/', views.OrganizationView.as_view(), name='organization_post'),
    path('v1/organization/<str:organization_id>/', views.ViewOrganization.as_view(), name='organization_get_one'),
    path('v1/organizations/', views.ViewOrganizations.as_view(), name='organization_get_all'),
    path('v1/group/', views.GroupView.as_view(), name='group_post'),
    path('v1/groups/', views.ViewGroups.as_view(), name='group_get_all'),
    path('v1/event/', views.EventView.as_view(), name='event_post'),
    path('v1/event/<str:event_id>/', views.ViewEvent.as_view(), name='event_get_one'),
    path('v1/events/', views.ViewEvents.as_view(), name='event_get_all'),
]