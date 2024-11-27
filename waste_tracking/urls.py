from django.urls import path
from . import views

app_name = "wastes"
urlpatterns = [
    # path("", views.waste_list, name='waste_list'),
    path("add/", views.add_waste, name='add_waste'),
    path("edit/<int:id>/", views.edit_waste, name='edit_waste'),
    path("delete/<int:id>/", views.delete_waste, name='delete_waste'),
    path("c/", views.collector_dashboard, name='collector_dashboard'),
    path("c/all_wastes/", views.waste_list, name='c_waste_list'),
    path("c/collected/", views.collected_wastes, name='collected_wastes'),
    path("c/not_collected/", views.not_collected_wastes, name='not_collected_wastes'),
    path("c/not_collected/<int:waste_id>/mark_collected/", views.mark_as_collected, name='mark_as_collected'),
    path("u/", views.normaluser_dashboard, name='normaluser_dashboard'),
    path("u/all_wastes/", views.waste_list, name='u_waste_list'),
    path("u/biodegradable/", views.biodegradable_wastes, name = "biodegradable_wastes"),
    path("u/non_biodegradable/", views.non_biodegradable_wastes, name = "non_biodegradable_wastes"),
]
