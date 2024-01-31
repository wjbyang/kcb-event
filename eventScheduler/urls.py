from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("v1/user/post", views.UserView.as_view(), name="userPost"),
    path("v1/user/get/<str:user_id>", views.ViewUser.as_view(), name="userGet"),
    path("v1/user/getall", views.ViewUsers.as_view(), name="userGetAll"),
    path("v1/organization/post", views.OrganizationView.as_view(), name="organizationPost"),
    path("v1/organization/get/<str:organization_id>", views.OrganizationView.as_view(), name="organizationGet"),
    path("v1/organization/getall", views.GetOrganization.as_view(), name="organizationGetAll"),
    path("v1/group/post", views.GroupView.as_view(), name="groupPost"),
    path("v1/group/get", views.GetGroups.as_view(), name="groupGet"),
]