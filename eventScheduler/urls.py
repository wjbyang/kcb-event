from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('v1/user/post/', views.UserView.as_view(), name='user_post'),
    path('v1/user/get/<str:user_id>/', views.ViewUser.as_view(), name='user_get'),
    path('v1/user/getall/', views.ViewUsers.as_view(), name='user_get_all'),
    path('v1/organization/post/', views.OrganizationView.as_view(), name='organization_post'),
    path('v1/organization/get/<str:organization_id>/', views.OrganizationView.as_view(), name='organization_get'),
    path('v1/organization/getall/', views.GetOrganization.as_view(), name='organization_get_all'),
    path('v1/group/post/', views.GroupView.as_view(), name='group_post'),
    path('v1/group/getall/', views.GetGroups.as_view(), name='group_get_all'),
]