from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import CreateEmployeeView, DetailsEmployeeView, CreateRoleView, \
    CreateSupervisorsView, DetailsRoleView, DetailsSupervisorsView, PromoteEmployeeView, HierarchyView

urlpatterns = {
    url(r'^hierarchy/$', HierarchyView.as_view(), name="view_hierarchy"),
    url(r'^employee/$', CreateEmployeeView.as_view(), name="create_employee"),
    url(r'^employee/(?P<pk>[0-9]+)/$',DetailsEmployeeView.as_view(), name="details_employee"),
    url(r'^supervisors/$',CreateSupervisorsView.as_view(), name="employee_supervisors"),
    url(r'^supervisors/(?P<pk>[0-9]+)/$',DetailsSupervisorsView.as_view(), name="details_supervisors"),
    url(r'^role/$', CreateRoleView.as_view(), name="create_role"),
    url(r'^role/(?P<pk>[0-9]+)/$',DetailsRoleView.as_view(), name="details_role"),
    url(r'^promote/(?P<pk>[0-9]+)/$', PromoteEmployeeView.as_view(), name='promote_employee')
}

urlpatterns = format_suffix_patterns(urlpatterns)