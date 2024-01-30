from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("v1/create_user/", views.CreateUser.as_view(), name="userPost"),
    path("v1/users/", views.ViewUsers.as_view(), name="usersPost"),
    path("v1/user/<str:user_id>/", views.ViewUser.as_view(), name="userGet"),
    path("v1/organization/", views.OrganizationView.as_view(), name="organizationPost"),
    path("v1/organizations/", views.GetOrganization.as_view(), name="organizationsGet"),
    path("v1/group", views.GroupView.as_view(), name="groupPost"),
    path("v1/groups", views.GetGroups.as_view(), name="groupGet"),

]