from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    # MOBILE VERSION
    path('map_mobile/', views.map_mobile, name='map_mobile'),
    path('save_location_mobile/', views.save_location_mobile, name='save_location_mobile'),
    path('locations_mobile/', views.locations_list_mobile, name='locations_list_mobile'),
    path('location_detail_mobile/<int:location_id>/', views.location_detail_mobile, name='location_detail_mobile'),
    path('item_mobile/<int:location_id>/add-item/', views.add_item_mobile, name='add_item_mobile'),
    path('item_mobile/<int:item_id>/update/', views.update_item_mobile, name='update_item_mobile'),

    path('media_mobile/<int:media_id>/delete/', views.delete_media, name='delete_media_mobile'),
    path('media_mobile/<int:media_id>/update/', views.update_media, name='update_media_mobile'),



    # WEB VERSION
    path('dashboard/', views.dashboard, name='dashboard'),
    path('map/', views.map, name='map'),
    path('save-location/', views.save_location, name='save_location'),
 
    path('locations/', views.locations_list, name='locations-list'),
    path('location/<int:location_id>/', views.location_detail, name='location-detail'),
    path('location/<int:location_id>/add-item/', views.add_item, name='add-item'),
    path('location/<int:location_id>/update/', views.update_location, name='update-location'),
    path('location/<int:location_id>/delete/', views.delete_location, name='delete-location'),

    path('toggle-archive-location/<int:location_id>/', views.toggle_archive_location, name='toggle-archive-location'),


    path('item/<int:item_id>/update/', views.update_item, name='update-item'),
    path('item/<int:item_id>/delete/', views.delete_item, name='delete-item'),

    path('manage-media/', views.manage_media, name='manage-media'),
    path('management-media/<int:item_id>/add/', views.management_add_media, name='management-add-media'),
    path('management-media/<int:media_id>/update/', views.management_update_media, name='management-update-media'),
    path('management-media/<int:media_id>/delete/', views.management_delete_media, name='management-delete-media'),

    path('manage-items/', views.manage_items, name='manage-items'),
    path('management-item/<int:item_id>/update/', views.management_update_item, name='management-update-item'),
    path('management-item/<int:item_id>/delete/', views.management_delete_item, name='management-delete-item'),


    path('media/<int:media_id>/delete/', views.delete_media, name='delete-media'),
    path('media/<int:media_id>/update/', views.update_media, name='update-media'),

    path('rapport/project/', views.project_report, name='project_report'),
    path('rapport/elements/', views.elements_rapport, name='elements-rapport'),

    path('generate-location-word/<int:location_id>/', views.generate_location_word, name='generate-location-word'),

    path('upload/<int:location_id>/', views.upload_kml_kmz, name='upload_kml_kmz'),
    path('import/kml-kmz/', views.import_kml_kmz, name='import_kml_kmz'),
    path('exporter/kml-kmz/', views.export_kml_kmz, name='export_kml_kmz'),


    path('location/<int:location_id>/generate-kml/', views.generate_location_kml, name='generate-location-kml'),
    path('location/<int:location_id>/generate-kmz/', views.generate_location_kmz, name='generate-location-kmz'),

    path('users/', views.user_list, name='user-list'),  # Liste des utilisateurs

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

