# from django.urls import path
# from .views import *
#
# app_name = "library"
# urlpatterns = [
#     path("", index, name="library"),
#     path("store/", store, name = "library"),
#     path("detail/", detail, name = "library"),
#     path("list_view", list_view, name = "library"),
#     path("add/<int:id>/", add_to_saved, name = "add"),
# ]
#
# # href="{% url 'library:add' id=story.id %}"

# urls.py

from django.urls import path
from .views import ReadingListIndexView, ReadingListDetailView, CreateReadingList, EditReadingList, add_to_saved, DeleteReadingList, remove_from_reading_list

urlpatterns = [
    path('', ReadingListIndexView.as_view(), name='reading_list'),
    path('<int:pk>/', ReadingListDetailView.as_view(), name='reading_list_details'),
    path('create/', CreateReadingList.as_view(), name='create_reading_list'),
    path('<int:pk>/edit/', EditReadingList.as_view(), name='edit_reading_list'),
    path('add_to_saved/<int:article_id>/', add_to_saved, name = 'add_to_saved'),
    path('<int:pk>/delete', DeleteReadingList.as_view(), name = 'confirm_reading_list_delete'),
    path('<int:reading_list_id>/remove/<int:article_id>', remove_from_reading_list, name = 'remove_from_reading_list'),
]
