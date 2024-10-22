from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.core.files import File
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from django.conf import settings
from django.urls import reverse
from django.db.models import Count
from django.db.models.functions import TruncMonth
from .models import Location, Item, MediaModel, upload_to, upload_plot_to
import os
import psutil
import json
import zipfile
from datetime import datetime
import cv2
import numpy as np
import matplotlib.pyplot as plt
from docx import Document
from docx.shared import Inches
from io import BytesIO
from datetime import datetime
from fastkml import kml
from shapely.geometry import Point, LineString, Polygon
from pyproj import Transformer
import xml.etree.ElementTree as ET

#MOBILE VERSION

def map_mobile(request):
    return render(request, 'dashboard_app/mobile/index.html')

def save_location_mobile(request):
    if request.method == 'POST':
        geojson = request.POST.get('geojson')
        name = request.POST.get('name')
        description = request.POST.get('description')

        # Vérifier les données reçues
        if not geojson or not name or not description:
            messages.warning(request, 'Assurez-vous de saisir correctement tous les champs.')
            return redirect(reverse('map_mobile'))

        # Vérifier si un projet avec le même nom existe déjà
        if Location.objects.filter(name=name).exists():
            messages.warning(request, 'Un projet avec ce nom existe déjà. Veuillez choisir un autre nom.')
            return redirect(reverse('map_mobile'))

        # Créer Le projet s'il n'existe pas encore
        location = Location.objects.create(
            name=name,
            description=description,
            geojson=geojson,
        )
        messages.success(request, 'Le projet a été enregistré avec succès!')
        return redirect(reverse('location_detail_mobile', args=[location.id]))
    else:
        return redirect(reverse('map_mobile'))


def location_detail_mobile(request, location_id):
    location = get_object_or_404(Location, pk=location_id)

    # Vérifier que les données GeoJSON sont analysées correctement
    try:
        location_geojson = json.loads(location.geojson)
    except json.JSONDecodeError as e:
        # Gérer les erreurs dans les données JSON
        location_geojson = None
        print(f"Erreur lors du décodage du geojson : {e}")

    # Convertir les éléments associés à Location en GeoJSON
    items = location.items.all()
    items_geojson = []
    for item in items:
        try:
            geojson = json.loads(item.geojson)  # Lire les données GeoJSON pour chaque élément
            properties = {
                "name": item.name,
                "description": item.description,
                "id": item.id,
                "media": []  # Liste des fichiers média associés
            }

            # Obtenir les fichiers média associés à l'élément actuel
            media_files = item.media_files.all()
            for media in media_files:
                media_data = {
                    "id": media.id,  # ID du fichier
                    "file_url": media.file.url,  # URL du fichier
                    "file_type": "image" if media.file.url.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp')) else "video",  # Type du fichier
                    "capture_angle": media.capture_angle,  # Angle de capture
                    "icon_url": media.icon_url,  # Icône si disponible
                    "plot_image_url": media.plot_image.url if media.plot_image else None  # Graphique si disponible
                }
                properties["media"].append(media_data)  # Ajouter les données du média aux propriétés

            geojson['properties'] = properties
            items_geojson.append(geojson)
        except json.JSONDecodeError:
            print(f"Erreur lors du décodage du geojson pour l'élément {item.id}")
        except Exception as e:
            print(f"Erreur lors du traitement de l'élément {item.id} : {e}")

    # Regrouper toutes les données géographiques
    items_geojson = json.dumps({"type": "FeatureCollection", "features": items_geojson})

    return render(request, 'dashboard_app/mobile/location_detail.html', {
        'location': location,
        'location_geojson': json.dumps(location_geojson),  # Ajouter le GeoJSON du lieu
        'items_geojson': items_geojson,  # Ajouter le GeoJSON des éléments associés
    })


def add_item_mobile(request, location_id):
    location = get_object_or_404(Location, pk=location_id)

    if request.method == 'POST':
        geojson = request.POST.get('geojson')
        name = request.POST.get('name')
        description = request.POST.get('description')
        
        if not geojson or not name or not description:
            messages.warning(request, 'Veuillez vérifier que tous les champs sont correctement remplis.')
            return redirect(reverse('location_detail_mobile', args=[location.id]))

        # Créer le nouvel élément
        item = Item.objects.create(
            name=name,
            description=description,
            location=location,
            geojson=geojson
        )

        # Traiter les fichiers multimédias (images ou vidéos) téléchargés
        media_files = request.FILES.getlist('media')
        
        for media in media_files:
            temp_file_path = default_storage.save(media.name, media)
            temp_file_url = default_storage.path(temp_file_path)
            
            capture_angle = None
            plot_path = None

            # Analyser les angles si le fichier est une image
            if media.content_type.startswith('image/'):
                angle_info = analyze_image_angle(temp_file_url)
                if "error" in angle_info:
                    messages.warning(request, angle_info["error"])
                else:
                    capture_angle = angle_info.get("mean_angle")

                    # Générer le graphique d'angle
                    plot_filename = f'plot_angle_{capture_angle:.2f}.png'
                    plot_path = upload_plot_to(MediaModel(item=item), plot_filename)
                    create_angle_plot(capture_angle, default_storage.path(plot_path))

            # Enregistrer les données dans la base de données
            MediaModel.objects.create(item=item, file=media, capture_angle=capture_angle, plot_image=plot_path)
            
            # Supprimer le fichier temporaire
            if os.path.exists(temp_file_url):
                os.remove(temp_file_url)

        messages.success(request, "L'élément et les médias ont été enregistrés avec succès!")
        return redirect(reverse('location_detail_mobile', args=[location.id]))

    messages.warning(request, "Une erreur s'est produite lors de l'ajout de l'élément.")
    return redirect('location_detail_mobile', item.location.id)

def update_location_mobile(request, item_id):
    item = get_object_or_404(Item, id=item_id)

    if request.method == 'POST':
        if request.content_type == 'application/json':
            try:
                data = json.loads(request.body)
                geojson = data.get('geojson')

                if geojson:
                    item.geojson = json.dumps(geojson)
                    item.save()
                    return JsonResponse({'success': True, 'message': 'L\'élément a été mis à jour géographiquement avec succès!'})
                else:
                    return JsonResponse({'success': False, 'message': 'Veuillez vérifier que les données GeoJSON sont correctement entrées.'})
            except json.JSONDecodeError:
                return JsonResponse({'success': False, 'message': 'Erreur dans les données JSON.'})
            except Exception as e:
                return JsonResponse({'success': False, 'message': 'Une erreur inattendue s\'est produite: ' + str(e)})
        else:
            # Traiter les données si la méthode est POST à partir d'un formulaire HTML (si vous utilisez un formulaire classique)
            name = request.POST.get('name')
            description = request.POST.get('description')
            media_files = request.FILES.getlist('media')
    
            if not name or not description:
                messages.warning(request, 'Veuillez vérifier que tous les champs sont correctement remplis.')
                return redirect(reverse('location_detail_mobile', args=[item.location.id]))

            # Mettre à jour les champs de base
            item.name = name
            item.description = description
            item.save()

            # Traiter chaque fichier média (image/vidéo)
            for media in media_files:
                # Enregistrer temporairement le fichier média
                temp_file_path = default_storage.save(media.name, media)
                temp_file_url = default_storage.path(temp_file_path)

                # Initialiser les variables pour l'angle et le graphique
                capture_angle = None
                plot_path = None

                # Traiter les fichiers image (pour l'analyse de l'angle et la génération du graphique)
                if media.content_type.startswith('image/'):
                    angle_info = analyze_image_angle(temp_file_url)
                    if "error" in angle_info:
                        messages.warning(request, angle_info["error"])
                    else:
                        capture_angle = angle_info.get("mean_angle")

                        # Générer et enregistrer le graphique de l'angle
                        plot_filename = f'plot_angle_{capture_angle:.2f}.png'
                        plot_path = upload_plot_to(MediaModel(item=item), plot_filename)
                        create_angle_plot(capture_angle, default_storage.path(plot_path))

                # Enregistrer les détails du média dans la base de données
                MediaModel.objects.create(
                    item=item, 
                    file=media, 
                    capture_angle=capture_angle, 
                    plot_image=plot_path
                )

                # Supprimer le fichier temporaire après traitement
                if os.path.exists(temp_file_url):
                    os.remove(temp_file_url)

            # Notification de succès après le traitement
            messages.success(request, "L'élément et les médias ont été mis à jour avec succès!")

            return redirect(reverse('location_detail_mobile', args=[item.location.id]))

    return JsonResponse({'success': False, 'message': 'Requête non valide.'})




# WEB VERSION 
def dashboard(request):        
    # Calcul des statistiques clés
    total_locations = Location.objects.count()
    total_items = Item.objects.count()
    total_media = MediaModel.objects.count()

    # Statistiques mensuelles des projets et éléments
    monthly_projects = (
        Location.objects.filter(archived=False)
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(total=Count('id'))
        .order_by('month')
    )

    monthly_items = (
        Item.objects.annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(total=Count('id'))
        .order_by('month')
    )

    # Préparation des données GeoJSON pour la carte
    locations = [
        {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': ''
            },
            'properties': {
                'name': location.name,
                'description': location.description
            }
        }
        for location in Location.objects.all()
    ]

    # Extraire les données dans des listes pour le graphique
    months = [entry['month'].strftime('%b') for entry in monthly_projects]
    project_data = [entry['total'] for entry in monthly_projects]
    item_data = [entry['total'] for entry in monthly_items]
    
    all_messages = messages.get_messages(request)

    context = {
        'total_locations': total_locations,
        'total_items': total_items,
        'total_media': total_media,
        'locations': locations,
        'months': months,
        'project_data': project_data,
        'item_data': item_data,
        'messages': all_messages,
    }

    return render(request, 'dashboard_app/web/dashboard.html', context)

def map(request):
    return render(request, 'dashboard_app/web/project_map.html')

def locations_list(request):
    month = request.GET.get('month')
    year = request.GET.get('year')
    archived = request.GET.get('archived')

    locations = Location.objects.all().order_by('-created_at')

    # Apply month and year filtering
    if month and not year:
        current_year = datetime.now().year
        locations = locations.filter(created_at__year=current_year, created_at__month=month)
    elif year:
        locations = locations.filter(created_at__year=year)
        if month:
            locations = locations.filter(created_at__month=month)

    # Apply archived filtering
    if archived == 'archived':
        locations = locations.filter(archived=True)
    elif archived == 'non_archived':
        locations = locations.filter(archived=False)

    paginator = Paginator(locations, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    months = [{'name': datetime(2000, i, 1).strftime('%B'), 'value': i} for i in range(1, 13)]
    years = range(2020, datetime.now().year + 1)

    context = {
        'locations': page_obj,
        'page_obj': page_obj,
        'months': months,
        'years': years,
    }
    return render(request, 'dashboard_app/web/locations_list.html', context)

def location_detail(request, location_id):
    location = get_object_or_404(Location, pk=location_id)

    # Vérifier que les données GeoJSON sont analysées correctement
    try:
        location_geojson = json.loads(location.geojson)
    except json.JSONDecodeError as e:
        # Gérer les erreurs dans les données JSON
        location_geojson = None
        print(f"Erreur lors du décodage du geojson : {e}")

    # Convertir les éléments associés à Location en GeoJSON
    items = location.items.all()
    items_geojson = []
    for item in items:
        try:
            geojson = json.loads(item.geojson)  # Lire les données GeoJSON pour chaque élément
            properties = {
                "name": item.name,
                "description": item.description,
                "id": item.id,
                "media": []  # Liste des fichiers média associés
            }

            # Obtenir les fichiers média associés à l'élément actuel
            media_files = item.media_files.all()
            for media in media_files:
                media_data = {
                    "id": media.id,  # ID du fichier
                    "file_url": media.file.url,  # URL du fichier
                    "file_type": "image" if media.file.url.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp')) else "video",  # Type du fichier
                    "capture_angle": media.capture_angle,  # Angle de capture
                    "icon_url": media.icon_url,  # Icône si disponible
                    "plot_image_url": media.plot_image.url if media.plot_image else None  # Graphique si disponible
                }
                properties["media"].append(media_data)  # Ajouter les données du média aux propriétés

            geojson['properties'] = properties
            items_geojson.append(geojson)
        except json.JSONDecodeError:
            print(f"Erreur lors du décodage du geojson pour l'élément {item.id}")
        except Exception as e:
            print(f"Erreur lors du traitement de l'élément {item.id} : {e}")

    # Regrouper toutes les données géographiques
    items_geojson = json.dumps({"type": "FeatureCollection", "features": items_geojson})

    return render(request, 'dashboard_app/web/location_detail.html', {
        'location': location,
        'location_geojson': json.dumps(location_geojson),  # Ajouter le GeoJSON du lieu
        'items_geojson': items_geojson,  # Ajouter le GeoJSON des éléments associés
    })

def save_location(request):
    if request.method == 'POST':
        geojson = request.POST.get('geojson')
        name = request.POST.get('name')
        description = request.POST.get('description')

        # Vérifier les données reçues
        if not geojson or not name or not description:
            messages.warning(request, 'Assurez-vous de saisir correctement tous les champs.')
            return redirect(reverse('map'))

        # Vérifier si un projet avec le même nom existe déjà
        if Location.objects.filter(name=name).exists():
            messages.warning(request, 'Un projet avec ce nom existe déjà. Veuillez choisir un autre nom.')
            return redirect(reverse('map'))

        # Créer Le projet s'il n'existe pas encore
        location = Location.objects.create(
            name=name,
            description=description,
            geojson=geojson,
        )
        messages.success(request, 'Le projet a été enregistré avec succès!')
        return redirect(reverse('location-detail', args=[location.id]))
    else:
        return redirect(reverse('map'))

def update_location(request, location_id):
    location = get_object_or_404(Location, id=location_id)
    if request.method == 'POST':
        try:
            # Utilisation de request.POST pour obtenir les données du formulaire HTML
            geojson = request.POST.get('geojson')
            name = request.POST.get('name')
            description = request.POST.get('description')

            # Vérification de la validité des entrées
            if not geojson or not name or not description:
                messages.warning(request, "Veuillez vérifier que tous les champs sont correctement remplis.")
                return redirect(reverse('locations-list'))

            # Vérifier si un projet avec le même nom existe déjà
            if Location.objects.filter(name=name).exclude(id=location_id).exists():
                messages.warning(request, 'Un projet avec ce nom existe déjà. Veuillez choisir un autre nom.')
                return redirect(reverse('locations-list'))

            # Vérifier si un projet avec la même description existe déjà
            if Location.objects.filter(description=description).exclude(id=location_id).exists():
                messages.warning(request, 'Un projet avec cette description existe déjà. Veuillez choisir une autre description.')
                return redirect(reverse('locations-list'))

            # Mise à jour des données du lieu
            location.name = name
            location.description = description
            location.geojson = geojson
            location.save()
            
            messages.success(request, "Le projet a été mis à jour avec succès !")
            return redirect(reverse('locations-list'))
        except json.JSONDecodeError:
            # Gestion de l'erreur JSON au cas où les données du formulaire ne sont pas valides
            messages.warning(request, "Échec de la lecture des données JSON. Veuillez vérifier que les données sont correctement envoyées.")
            return redirect(reverse('locations-list'))
    return redirect(reverse('locations-list'))

def delete_location(request, location_id):
    location = get_object_or_404(Location, id=location_id)
    location.delete()
    messages.success(request, "Le projet a été supprimé avec succès.")
    return redirect('locations-list')

def toggle_archive_location(request, location_id):
    location = get_object_or_404(Location, pk=location_id)
    location.archived = not location.archived
    location.save()

    if location.archived:
        messages.success(request, "Le lieu a été archivé avec succès.")
    else:
        messages.success(request, "Le lieu a été désarchivé avec succès.")
    return redirect(reverse('locations-list'))

def analyze_image_angle(image_path):
    # Charger l'image
    image = cv2.imread(image_path)
    if image is None:
        return {"error": "Erreur : Image introuvable."}

    # Convertir l'image en niveaux de gris
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Appliquer la détection des contours de Canny avec des seuils ajustables
    edges = cv2.Canny(gray, 30, 200)  # Seuil inférieur pour une détection des contours plus sensible

    # Détecter les lignes en utilisant HoughLinesP avec des paramètres ajustés pour de meilleurs résultats
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 50, minLineLength=50, maxLineGap=30)  # Réduction de minLineLength et maxLineGap

    # Si aucune ligne n'est trouvée, renvoyer un angle par défaut (en face)
    if lines is None:
        # Retourner un résultat par défaut pour une capture directe
        return {
            "mean_angle": 0.0,
            "capture_direction": "Capture effectuée de face",
            "object_location": "L'objet est situé directement devant la caméra",
            "icon": "https://e7.pngegg.com/pngimages/792/964/png-clipart-computer-icons-up-arrow-angle-black.png"
        }

    # Extraire les angles des lignes détectées
    angles = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        angle = np.degrees(np.arctan2(y2 - y1, x2 - x1))

        # Ignorer les lignes horizontales et quasi-horizontales avec un filtre plus strict
        if abs(angle) > 5 and abs(angle) < 175:  # Éviter les lignes presque horizontales et verticales
            angles.append(angle)

    # Si aucun angle n'a été trouvé, renvoyer un résultat par défaut (en face)
    if not angles:
        return {
            "mean_angle": 0.0,
            "capture_direction": "Capture effectuée de face",
            "object_location": "L'objet est situé directement devant la caméra",
            "icon": "https://e7.pngegg.com/pngimages/792/964/png-clipart-computer-icons-up-arrow-angle-black.png"
        }

    # Calculer l'angle moyen ou la médiane en fonction du nombre de lignes
    if len(angles) > 5:  # Utiliser la médiane pour plus de lignes, afin d'éviter les valeurs aberrantes
        mean_angle = np.median(angles)
    else:
        mean_angle = np.mean(angles)

    # Déterminer l'angle de capture et la position de l'objet
    angle_info = {"mean_angle": mean_angle}
    
    if -10 <= mean_angle <= 10:
        angle_info['capture_direction'] = "Capture effectuée de face"
        angle_info['object_location'] = "L'objet est situé directement devant la caméra"
        angle_info['icon'] = "https://e7.pngegg.com/pngimages/792/964/png-clipart-computer-icons-up-arrow-angle-black.png"
    elif mean_angle > 10:
        angle_info['capture_direction'] = "Capture effectuée du côté droit"
        angle_info['object_location'] = "L'objet est situé sur le côté droit de la caméra"
        angle_info['icon'] = "https://icons.iconarchive.com/icons/fa-team/fontawesome/256/FontAwesome-Angle-Right-icon.png"
    elif mean_angle < -10:
        angle_info['capture_direction'] = "Capture effectuée du côté gauche"
        angle_info['object_location'] = "L'objet est situé sur le côté gauche de la caméra"
        angle_info['icon'] = "https://cdn-icons-png.flaticon.com/512/8591/8591387.png"

    return angle_info

def create_angle_plot(angle, save_path):
    # Ensure the directory exists
    directory = os.path.dirname(save_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    fig, ax = plt.subplots(figsize=(6, 6))

    # Dessinez un demi-cercle représentant 180 degrés
    theta = np.linspace(0, np.pi, 180)
    x = np.cos(theta)
    y = np.sin(theta)
    ax.plot(x, y, label="180° semi-circle")

    radians = np.radians(angle)
    x_angle = [0, np.cos(radians)]
    y_angle = [0, np.sin(radians)]
    ax.plot(x_angle, y_angle, color='r', label=f"Capture Angle: {angle}°")

    ax.set_aspect('equal')
    ax.set_title(f"Camera Capture: {angle:.2f}°")
    ax.set_xlim([-1.1, 1.1])
    ax.set_ylim([0, 1.1])
    ax.legend()

    plt.savefig(save_path)
    plt.close(fig)

def add_item(request, location_id):
    location = get_object_or_404(Location, pk=location_id)

    if request.method == 'POST':
        geojson = request.POST.get('geojson')
        name = request.POST.get('name')
        description = request.POST.get('description')
        
        if not geojson or not name or not description:
            messages.warning(request, 'Veuillez vérifier que tous les champs sont correctement remplis.')
            return redirect(reverse('location-detail', args=[location.id]))

        # Créer le nouvel élément
        item = Item.objects.create(
            name=name,
            description=description,
            location=location,
            geojson=geojson
        )

        # Traiter les fichiers multimédias (images ou vidéos) téléchargés
        media_files = request.FILES.getlist('media')
        
        for media in media_files:
            temp_file_path = default_storage.save(media.name, media)
            temp_file_url = default_storage.path(temp_file_path)
            
            capture_angle = None
            plot_path = None

            # Analyser les angles si le fichier est une image
            if media.content_type.startswith('image/'):
                angle_info = analyze_image_angle(temp_file_url)
                if "error" in angle_info:
                    messages.warning(request, angle_info["error"])
                else:
                    capture_angle = angle_info.get("mean_angle")

                    # Générer le graphique d'angle
                    plot_filename = f'plot_angle_{capture_angle:.2f}.png'
                    plot_path = upload_plot_to(MediaModel(item=item), plot_filename)
                    create_angle_plot(capture_angle, default_storage.path(plot_path))

            # Enregistrer les données dans la base de données
            MediaModel.objects.create(item=item, file=media, capture_angle=capture_angle, plot_image=plot_path)
            
            # Supprimer le fichier temporaire
            if os.path.exists(temp_file_url):
                os.remove(temp_file_url)

        messages.success(request, "L'élément et les médias ont été enregistrés avec succès!")
        return redirect(reverse('location-detail', args=[location.id]))

    messages.warning(request, "Une erreur s'est produite lors de l'ajout de l'élément.")
    return redirect('location-detail', item.location.id)

def update_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)

    if request.method == 'POST':
        if request.content_type == 'application/json':
            try:
                data = json.loads(request.body)
                geojson = data.get('geojson')

                if geojson:
                    item.geojson = json.dumps(geojson)
                    item.save()
                    return JsonResponse({'success': True, 'message': 'L\'élément a été mis à jour géographiquement avec succès!'})
                else:
                    return JsonResponse({'success': False, 'message': 'Veuillez vérifier que les données GeoJSON sont correctement entrées.'})
            except json.JSONDecodeError:
                return JsonResponse({'success': False, 'message': 'Erreur dans les données JSON.'})
            except Exception as e:
                return JsonResponse({'success': False, 'message': 'Une erreur inattendue s\'est produite: ' + str(e)})
        else:
            # Traiter les données si la méthode est POST à partir d'un formulaire HTML (si vous utilisez un formulaire classique)
            name = request.POST.get('name')
            description = request.POST.get('description')
            media_files = request.FILES.getlist('media')
    
            if not name or not description:
                messages.warning(request, 'Veuillez vérifier que tous les champs sont correctement remplis.')
                return redirect(reverse('location-detail', args=[item.location.id]))

            # Mettre à jour les champs de base
            item.name = name
            item.description = description
            item.save()

            # Traiter chaque fichier média (image/vidéo)
            for media in media_files:
                # Enregistrer temporairement le fichier média
                temp_file_path = default_storage.save(media.name, media)
                temp_file_url = default_storage.path(temp_file_path)

                # Initialiser les variables pour l'angle et le graphique
                capture_angle = None
                plot_path = None

                # Traiter les fichiers image (pour l'analyse de l'angle et la génération du graphique)
                if media.content_type.startswith('image/'):
                    angle_info = analyze_image_angle(temp_file_url)
                    if "error" in angle_info:
                        messages.warning(request, angle_info["error"])
                    else:
                        capture_angle = angle_info.get("mean_angle")

                        # Générer et enregistrer le graphique de l'angle
                        plot_filename = f'plot_angle_{capture_angle:.2f}.png'
                        plot_path = upload_plot_to(MediaModel(item=item), plot_filename)
                        create_angle_plot(capture_angle, default_storage.path(plot_path))

                # Enregistrer les détails du média dans la base de données
                MediaModel.objects.create(
                    item=item, 
                    file=media, 
                    capture_angle=capture_angle, 
                    plot_image=plot_path
                )

                # Supprimer le fichier temporaire après traitement
                if os.path.exists(temp_file_url):
                    os.remove(temp_file_url)

            # Notification de succès après le traitement
            messages.success(request, "L'élément et les médias ont été mis à jour avec succès!")

            return redirect(reverse('location-detail', args=[item.location.id]))

    return JsonResponse({'success': False, 'message': 'Requête non valide.'})

def delete_item(request, item_id):
    """Supprimer un élément spécifique."""
    if request.method == 'POST':
        item = get_object_or_404(Item, id=item_id)
        item.delete()
        return JsonResponse({'success': True, 'message': "L'élément a été supprimé avec succès!"})
    return JsonResponse({'error': 'Méthode de requête non valide.'}, status=400)

def update_media(request, media_id):
    media = get_object_or_404(MediaModel, id=media_id)
    new_file = request.FILES.get('media_file')

    if new_file:
        # Enregistrer temporairement le nouveau fichier pour l'analyser
        temp_file_path = default_storage.save(new_file.name, new_file)
        temp_file_url = default_storage.path(temp_file_path)
        capture_angle = None
        plot_path = None

        # Analyser le fichier s'il s'agit d'une image
        if new_file.content_type.startswith('image/'):
            angle_info = analyze_image_angle(temp_file_url)
            if "error" in angle_info:
                messages.warning(request, angle_info["error"])
            else:
                capture_angle = angle_info.get("mean_angle")

                if capture_angle is not None:
                    # Générer et enregistrer le graphique d'angle dans un chemin spécifique
                    plot_directory = f'plots/item_{media.item.id}/'
                    
                    # Vérifier si capture_angle est valide pour le formatage
                    try:
                        plot_filename = f'plot_angle_{capture_angle:.2f}.png'
                        plot_path = os.path.join(plot_directory, plot_filename)
                        full_plot_path = default_storage.path(plot_path)
                        
                        # Créer le graphique d'angle
                        create_angle_plot(capture_angle, full_plot_path)
                    except TypeError:
                        messages.warning(request, 'Erreur lors de la création du graphique d\'angle.')
                        plot_path = None  # Définir plot_path à None en cas d'erreur

        # Mettre à jour le modèle de média
        media.file = new_file
        media.capture_angle = capture_angle
        media.plot_image = plot_path
        media.save()

        # Supprimer le fichier temporaire après le traitement
        if os.path.exists(temp_file_url):
            os.remove(temp_file_url)

        messages.success(request, "Les médias et l'analyse d'angle ont été mis à jour avec succès!")
        return redirect(reverse('location-detail', args=[media.item.location.id]))

    messages.warning(request, 'Aucun nouveau fichier sélectionné.')
    return redirect(reverse('location-detail', args=[media.item.location.id]))

def delete_media(request, media_id):
    if request.method == 'POST':
        media = get_object_or_404(MediaModel, pk=media_id)
        location_id = media.item.location.id
        media.delete()
        messages.success(request, 'Le fichier a été supprimé avec succès!')
        return redirect(reverse('location-detail', args=[location_id]))

    messages.warning(request, 'La méthode de commande est incorrecte.')
    return redirect('locations-list')

def manage_media(request):
    locations = Location.objects.all().order_by('-created_at')
    items = MediaModel.objects.select_related('item').all()

    media_data = {}
    total_media_size = 0  # Variable pour la taille totale des médias

    for item in items:
        file_path = item.file.path
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            total_media_size += file_size  # Ajouter la taille du fichier à la somme totale
        
        media_data.setdefault(item.item.id, []).append({
            'id': item.id,
            'name': item.file.name,
            'file_type': 'image' if item.file.url.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp')) else 'video' if item.file.url.lower().endswith(('.mp4', '.avi', '.mov')) else 'document',
            'size': file_size if os.path.exists(file_path) else 'Inconnu',  # Utiliser 'Inconnu' si le fichier n'existe pas
            'thumbnail_url': item.file.url if os.path.exists(file_path) else '',  # Utiliser une URL vide si le fichier n'existe pas
        })

    # Utiliser psutil pour obtenir les informations sur l'espace disque
    disk_usage = psutil.disk_usage('/')
    total_disk_size = disk_usage.total  # Taille totale du disque en octets
    available_disk_size = disk_usage.free  # Espace libre en octets

    # Conversion de la taille en octets en Go
    total_media_size_gb = total_media_size / (1024 * 1024 * 1024)
    total_disk_size_gb = total_disk_size / (1024 * 1024 * 1024)
    available_disk_size_gb = available_disk_size / (1024 * 1024 * 1024)

    # Calcul du pourcentage d'utilisation de l'espace disque
    used_percentage = (total_media_size / total_disk_size) * 100
    context = {
        'locations': locations,
        'media_data': media_data,
        'total_media_size_gb': total_media_size_gb,
        'total_disk_size_gb': total_disk_size_gb,
        'available_disk_size_gb': available_disk_size_gb,
        'used_percentage': used_percentage,
        'selected_item_id': request.GET.get('item_id')
    }
    return render(request, 'dashboard_app/web/manage_media.html', context)
    
def management_add_media(request, item_id):
    if request.method == 'POST' and request.FILES:
        item = get_object_or_404(Item, pk=item_id)
        files = request.FILES.getlist('mediaFiles')
        
        if not files:
            messages.warning(request, 'Aucun fichier sélectionné.')
            return redirect(reverse('manage-media') + f'?item_id={item_id}')

        for media in files:
            temp_file_path = default_storage.save(media.name, media)
            temp_file_url = default_storage.path(temp_file_path)
            
            capture_angle = None
            plot_path = None

            # Analyser les angles si le fichier est une image
            if media.content_type.startswith('image/'):
                angle_info = analyze_image_angle(temp_file_url)
                if "error" in angle_info:
                    messages.warning(request, angle_info["error"])
                else:
                    capture_angle = angle_info.get("mean_angle")

                    # Générer le graphique d'angle
                    plot_filename = f'plot_angle_{capture_angle:.2f}.png'
                    plot_path = upload_plot_to(MediaModel(item=item), plot_filename)
                    create_angle_plot(capture_angle, default_storage.path(plot_path))

            # Enregistrer les données dans la base de données
            MediaModel.objects.create(item=item, file=media, capture_angle=capture_angle, plot_image=plot_path)
            
            # Supprimer le fichier temporaire
            if os.path.exists(temp_file_url):
                os.remove(temp_file_url)


        messages.success(request, f'{len(files)} fichier(s) ont été téléchargé(s) avec succès!')
        return redirect(reverse('manage-media') + f'?item_id={item_id}')

    messages.warning(request, 'La méthode de requête est incorrecte ou aucun fichier n\'a été fourni.')
    return redirect(reverse('manage-media') + f'?item_id={item_id}')

def management_update_media(request, media_id):
    media = get_object_or_404(MediaModel, id=media_id)
    item_id = media.item.id
    new_file = request.FILES.get('media_file')

    if new_file:
        temp_file_path = default_storage.save(new_file.name, new_file)
        temp_file_url = default_storage.path(temp_file_path)
        capture_angle = None
        plot_path = None

        if new_file.content_type.startswith('image/'):
            angle_info = analyze_image_angle(temp_file_url)
            if "error" in angle_info:
                messages.warning(request, angle_info["error"])
            else:
                capture_angle = angle_info.get("mean_angle")
                plot_filename = f'plot_angle_{capture_angle:.2f}.png'
                plot_path = upload_plot_to(MediaModel(item=media.item), plot_filename)
                create_angle_plot(capture_angle, default_storage.path(plot_path))

        media.file = new_file
        media.capture_angle = capture_angle
        media.plot_image = plot_path
        media.save()

        if os.path.exists(temp_file_url):
            os.remove(temp_file_url)

        messages.success(request, "Les médias et l'analyse d'angle ont été mis à jour avec succès!")
        return redirect(reverse('manage-media') + f'?item_id={item_id}')

    messages.warning(request, 'Aucun nouveau fichier sélectionné.')
    return redirect(reverse('manage-media') + f'?item_id={item_id}')

def management_delete_media(request, media_id):
    if request.method == 'POST':
        media = get_object_or_404(MediaModel, pk=media_id)
        item_id = media.item.id
        media.delete()
        messages.success(request, 'Le fichier a été supprimé avec succès!')
        return redirect(reverse('manage-media') + f'?item_id={item_id}')

    messages.warning(request, 'La méthode de commande est incorrecte.')
    return redirect(reverse('manage-media') + f'?item_id={item_id}')


def manage_items(request):
    locations = Location.objects.all().order_by('-created_at')

    item_data = {}
    for location in locations:
        for item in location.items.all():
            item_data.setdefault(location.id, []).append({
                'id': item.id,
                'name': item.name,
                'description': item.description,
                'created_at': item.created_at.strftime('%Y-%m-%d'),
            })

    context = {
        'locations': locations,
        'item_data': item_data,
        'selected_item_id': request.GET.get('item_id')
    }
    return render(request, 'dashboard_app/web/manage_items.html', context)

def management_update_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    location_id = item.location.id

    if request.method == 'POST':
        name = request.POST.get('item_name')
        description = request.POST.get('item_description')

        if not name or not description:
            messages.warning(request, 'Veuillez vérifier que tous les champs sont correctement remplis.')
            return redirect(reverse('manage-items') + f'?location_id={location_id}')

        item.name = name
        item.description = description
        item.save()

        messages.success(request, "L'élément a été mis à jour avec succès!")
        return redirect(reverse('manage-items') + f'?location_id={location_id}')

    return JsonResponse({'success': False, 'message': 'Requête non valide.'})

def management_delete_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    location_id = item.location.id

    if request.method == 'POST':
        item.delete()
        messages.success(request, "L'élément a été supprimé avec succès!")
        return redirect(reverse('manage-items') + f'?location_id={location_id}')

    messages.error(request, "Requête non valide.")
    return redirect(reverse('manage-items') + f'?location_id={location_id}')


def project_report(request):
    month = request.GET.get('month')
    year = request.GET.get('year')
    archived = request.GET.get('archived')

    locations = Location.objects.all().order_by('-created_at')

    # Apply month and year filtering
    if month and not year:
        current_year = datetime.now().year
        locations = locations.filter(created_at__year=current_year, created_at__month=month)
    elif year:
        locations = locations.filter(created_at__year=year)
        if month:
            locations = locations.filter(created_at__month=month)

    # Apply archived filtering
    if archived == 'archived':
        locations = locations.filter(archived=True)
    elif archived == 'non_archived':
        locations = locations.filter(archived=False)

    paginator = Paginator(locations, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    months = [{'name': datetime(2000, i, 1).strftime('%B'), 'value': i} for i in range(1, 13)]
    years = range(2020, datetime.now().year + 1)

    context = {
        'page_obj': page_obj,
        'months': months,
        'years': years,
    }
    return render(request, 'dashboard_app/web/project_report.html', context)

def elements_rapport(request):
    if request.method == "GET":
        # Initial GET request to render the form for selecting items
        month = request.GET.get('month')
        year = request.GET.get('year')
        archived = request.GET.get('archived')
        location_id = request.GET.get('location_id')

        # Get all locations and filter by archived status if provided
        locations = Location.objects.all().order_by('-created_at')
        if archived == 'archived':
            locations = locations.filter(archived=True)
        elif archived == 'non_archived':
            locations = locations.filter(archived=False)

        # Get items related to a specific location
        items = Item.objects.filter(location_id=location_id).prefetch_related('media_files')

        # Apply month and year filtering for items
        if month and not year:
            current_year = datetime.now().year
            items = items.filter(created_at__year=current_year, created_at__month=month)
        elif year:
            items = items.filter(created_at__year=year)
            if month:
                items = items.filter(created_at__month=month)

        paginator = Paginator(locations, 9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        months = [{'name': datetime(2000, i, 1).strftime('%B'), 'value': i} for i in range(1, 13)]
        years = range(2020, datetime.now().year + 1)

        context = {
            'locations': locations,
            'page_obj': page_obj,
            'months': months,
            'years': years,
        }

        return render(request, 'dashboard_app/web/elements_report.html', context)

    elif request.method == "POST":
        # Get selected item IDs from the POST request
        selected_item_ids = request.POST.getlist('selected_items')
        if not selected_item_ids:
            messages.warning(request, 'Aucun élément sélectionné.')

            return redirect(reverse('elements-rapport'))

        # Get the selected items
        items = Item.objects.filter(id__in=selected_item_ids).prefetch_related('media_files')

        # Get the location information using location_id
        location_id = request.POST.get('location_id')
        if not location_id:
            return HttpResponse("No location specified.", status=400)
        
        location = get_object_or_404(Location, id=location_id)

        # Prepare the ZIP file
        today_date = datetime.now().strftime('%Y-%m-%d')
        zip_subdir = f"{today_date}_elements_projet_{location.name}"
        zip_filename = f"{zip_subdir}.zip"
        s = BytesIO()  # Store the ZIP file in memory
        zf = zipfile.ZipFile(s, "w")

        # Create a Word document for each selected item
        for item in items:
            doc = Document()
            doc.add_heading(item.name, 0)  # Add item title
            doc.add_paragraph(f"Description: {item.description}")  # Add item description

            # Process ArcGIS-style GeoJSON data
            if item.geojson:
                try:
                    geojson_data = json.loads(item.geojson)  # Load the ArcGIS data
                    geometry = geojson_data.get('geometry', {})
                    
                    # Handle geometry types
                    if 'paths' in geometry:  # This is likely a LineString
                        paths = geometry.get('paths', [])
                        doc.add_heading("Type de Géométrie: LineString", level=1)
                        if paths:
                            for index, path in enumerate(paths):
                                for point_index, point in enumerate(path):
                                    doc.add_paragraph(f"  Point {point_index + 1}: Longitude: {point[0]}, Latitude: {point[1]}")
                        else:
                            doc.add_paragraph("Données de chemin non trouvées.")

                    elif 'rings' in geometry:  # This is likely a Polygon
                        rings = geometry.get('rings', [])
                        doc.add_heading("Type de Géométrie: Polygon", level=1)
                        if rings:
                            for ring_index, ring in enumerate(rings):
                                doc.add_paragraph(f"Anneau {ring_index + 1}:")
                                for point_index, point in enumerate(ring):
                                    if point_index == len(ring) - 1 and point == ring[0]:
                                        # If this is the last point and is identical to the first point, label it as "Point 1"
                                        point_label = "Point 1 (Identique au Point de départ)"
                                    else:
                                        point_label = f"Point {point_index + 1}"
                                    doc.add_paragraph(f"  {point_label}: Longitude: {point[0]}, Latitude: {point[1]}")
                        else:
                            doc.add_paragraph("Données d'anneaux non trouvées pour le polygone.")

                    elif 'x' in geometry and 'y' in geometry:  # This is likely a Point
                        x = geometry['x']
                        y = geometry['y']
                        doc.add_heading("Type de Géométrie: Point", level=1)
                        doc.add_paragraph(f"Coordonnées (Longitude, Latitude): {x}, {y}")

                    else:
                        doc.add_paragraph("Type de géométrie non pris en charge ou données de géométrie non trouvées.")

                except (KeyError, json.JSONDecodeError) as e:
                    print(f"Erreur lors de l'analyse des données ArcGIS: {e}")
                    doc.add_paragraph("Erreur lors de l'analyse des données géographiques.")

            # Ajouter les images et vidéos au document Word
            for media in item.media_files.all():
                media_file_path = os.path.join(settings.MEDIA_ROOT, media.file.name)
                if os.path.exists(media_file_path):
                    try:
                        if media.file.url.endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp')):
                            doc.add_picture(media_file_path, width=Inches(2))  # Ajouter l'image au document
                            doc.add_paragraph(f"Image: {os.path.basename(media.file.name)}")  # Ajouter le nom de l'image
                        elif media.file.url.endswith(('.mp4', '.avi', '.mov')):
                            doc.add_paragraph(f"Vidéo: {os.path.basename(media.file.name)}")  # Ajouter le nom de la vidéo
                            doc.add_paragraph("Le fichier vidéo est inclus dans le fichier ZIP.")  # Mentionner que la vidéo est dans le zip
                    except Exception as e:
                        print(f"Erreur lors de l'ajout du média: {e}")

            # Save the Word document to memory
            doc_io = BytesIO()
            doc.save(doc_io)
            doc_io.seek(0)

            # Add the Word document to the ZIP with a unique filename
            zf.writestr(f"{zip_subdir}/{item.name}_{item.id}.docx", doc_io.read())

            # Add media files (images and videos) to the ZIP
            for media in item.media_files.all():
                media_file_path = os.path.join(settings.MEDIA_ROOT, media.file.name)
                if os.path.exists(media_file_path):
                    with open(media_file_path, 'rb') as f:
                        zf.writestr(f"{zip_subdir}/{item.name}/{os.path.basename(media_file_path)}", f.read())

        # Close the ZIP file after adding all files
        zf.close()

        # Prepare the response to download the ZIP file directly
        response = HttpResponse(s.getvalue(), content_type="application/x-zip-compressed")
        response['Content-Disposition'] = f'attachment; filename={zip_filename}'

        return response

    return HttpResponse("Invalid request method.", status=400)


def import_kml_kmz(request):
    month = request.GET.get('month')
    year = request.GET.get('year')
    archived = request.GET.get('archived')

    locations = Location.objects.all().order_by('-created_at')

    # Apply month and year filtering
    if month and not year:
        current_year = datetime.now().year
        locations = locations.filter(created_at__year=current_year, created_at__month=month)
    elif year:
        locations = locations.filter(created_at__year=year)
        if month:
            locations = locations.filter(created_at__month=month)

    # Apply archived filtering
    if archived == 'archived':
        locations = locations.filter(archived=True)
    elif archived == 'non_archived':
        locations = locations.filter(archived=False)

    paginator = Paginator(locations, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    months = [{'name': datetime(2000, i, 1).strftime('%B'), 'value': i} for i in range(1, 13)]
    years = range(2020, datetime.now().year + 1)

    context = {
        'page_obj': page_obj,
        'months': months,
        'years': years,
    }
    return render(request, 'dashboard_app/web/import_kml_kmz.html', context)

def upload_kml_kmz(request, location_id):
    location = get_object_or_404(Location, id=location_id)
    
    if request.method == 'POST' and 'file' in request.FILES:
        uploaded_file = request.FILES['file']
        file_extension = uploaded_file.name.split('.')[-1].lower()

        if file_extension == 'kml':
            try:
                process_kml_file(uploaded_file, location, request)
                messages.success(request, 'Le fichier KML a été importé avec succès !')
                return redirect('import_kml_kmz')
            except Exception as e:
                messages.error(request, f"Erreur lors de l'importation du fichier KML: {e}")
                return redirect('import_kml_kmz')
        elif file_extension == 'kmz':
            try:
                # هنا تم تمرير الكائن request إلى الدالة
                process_kmz_file(uploaded_file, location, request)
                messages.success(request, 'Le fichier KMZ a été importé avec succès !')
                return redirect('import_kml_kmz')
            except Exception as e:
                messages.error(request, f"Erreur lors de l'importation du fichier KMZ: {e}")
                return redirect('import_kml_kmz')
        else:
            messages.error(request, 'Le fichier téléchargé n\'est pas au format KML ou KMZ.')
            return redirect('import_kml_kmz')

    messages.error(request, 'Veuillez sélectionner un fichier à télécharger.')
    return redirect('import_kml_kmz')

def process_kml_file(kml_file, location, request, media_files=None):
    # إعداد التحويل من WGS84 (EPSG:4326) إلى Web Mercator (EPSG:3857)
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True)

    try:
        tree = ET.parse(kml_file)
        root = tree.getroot()

        namespace = {"kml": "http://www.opengis.net/kml/2.2"}
        document = root.find("kml:Document", namespace)

        if document is not None:
            existing_items = Item.objects.filter(location=location)
            existing_item_names = [item.name for item in existing_items]

            duplicate_items = []
            new_items = []

            for placemark in document.findall("kml:Placemark", namespace):
                name = placemark.find("kml:name", namespace).text if placemark.find("kml:name", namespace) is not None else "Sans nom"
                description = placemark.find("kml:description", namespace).text if placemark.find("kml:description", namespace) is not None else "Sans description"

                # تحقق إذا كان العنصر موجودًا بالفعل
                if name in existing_item_names:
                    duplicate_items.append(name)
                    continue  # تجاوز العناصر المكررة

                geometry = None
                esri_data = None

                # معالجة ملفات الوسائط إذا كانت موجودة
                media_file_url = None
                if media_files:
                    extended_data = placemark.find("kml:ExtendedData", namespace)
                    if extended_data is not None:
                        for data in extended_data.findall("kml:Data", namespace):
                            if data.get("name") == "media_file":
                                media_file_name = data.find("kml:value", namespace).text
                                media_file_url = media_files.get(media_file_name)

                if placemark.find("kml:Point", namespace) is not None:
                    # معالجة النقاط
                    coordinates = placemark.find("kml:Point/kml:coordinates", namespace).text.strip()
                    lon, lat = [float(value) for value in coordinates.split(",")[:2]]
                    x, y = transformer.transform(lon, lat)
                    geometry = {
                        "spatialReference": {"latestWkid": 3857, "wkid": 102100},
                        "x": x,
                        "y": y
                    }

                elif placemark.find("kml:LineString", namespace) is not None:
                    # معالجة الخطوط
                    coordinates = placemark.find("kml:LineString/kml:coordinates", namespace).text.strip()
                    paths = [[transformer.transform(float(coord.split(",")[0]), float(coord.split(",")[1])) for coord in coordinates.split()]]
                    geometry = {
                        "spatialReference": {"latestWkid": 3857, "wkid": 102100},
                        "paths": paths
                    }

                elif placemark.find("kml:Polygon", namespace) is not None:
                    # معالجة المضلعات
                    coordinates = placemark.find("kml:Polygon/kml:outerBoundaryIs/kml:LinearRing/kml:coordinates", namespace).text.strip()
                    rings = [[transformer.transform(float(coord.split(",")[0]), float(coord.split(",")[1])) for coord in coordinates.split()]]
                    geometry = {
                        "spatialReference": {"latestWkid": 3857, "wkid": 102100},
                        "rings": rings
                    }

                if geometry:
                    # تحويل البيانات إلى صيغة ArcGIS ESRI
                    esri_data = {
                        "geometry": geometry,
                        "symbol": {
                            "type": "esriSLS" if "paths" in geometry else "esriSFS",
                            "color": [255, 165, 0],
                            "width": 2 if "paths" in geometry else None,
                            "style": "esriSLSSolid" if "paths" in geometry else "esriSFSSolid"
                        },
                        "attributes": {},
                        "popupTemplate": None
                    }

                    # إضافة العنصر الجديد إلى قاعدة البيانات
                    item = Item.objects.create(
                        name=name,
                        description=description,
                        location=location,
                        geojson=json.dumps(esri_data)
                    )
                    new_items.append(name)  # إضافة الاسم إلى قائمة العناصر الجديدة

                    # إذا كان هناك ملف وسائط مرتبط، يتم حفظه في MediaModel
                    if media_file_url:
                        MediaModel.objects.create(
                            item=item,
                            file=media_file_url,
                            created_at=datetime.now()
                        )

            # عرض الرسائل للمستخدم
            if duplicate_items:
                messages.warning(request, f"Les éléments suivants sont déjà ajoutés: {', '.join(duplicate_items)}")
            if new_items:
                messages.success(request, f"Les nouveaux éléments ont été ajoutés avec succès: {', '.join(new_items)}")

    except ET.ParseError as e:
        print(f"خطأ أثناء تحليل ملف KML: {e}")

def process_kmz_file(kmz_file, location, request):
    try:
        print("بدء معالجة ملف KMZ")
        media_files = {}

        # فك ضغط ملف KMZ
        with zipfile.ZipFile(kmz_file, 'r') as z:
            print("تم فك ضغط ملف KMZ بنجاح.")
            print("قائمة الملفات داخل KMZ:", z.namelist())

            for file_name in z.namelist():
                print(f"جاري معالجة الملف: {file_name}")
                
                # إذا كان الملف KML، نقوم بمعالجته
                if file_name.endswith('.kml'):
                    with z.open(file_name) as kml_file:
                        print(f"جاري معالجة ملف KML: {file_name}")
                        process_kml_file(kml_file, location, request, media_files)
                
                # إذا كان الملف من نوع صورة أو فيديو، نقوم بحفظه كملف وسائط
                elif file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tif', '.mp4', '.avi', '.mov')):
                    try:
                        print(f"محاولة حفظ ملف الوسائط: {file_name}")
                        # اختر عنصرًا مرتبطًا بالموقع لحفظ الوسائط
                        item = location.items.first()
                        if item:
                            temp_media_instance = MediaModel(item=item)
                            media_path = upload_to(temp_media_instance, file_name)

                            # حفظ الملف في الموقع المحدد
                            temp_file_path = default_storage.save(media_path, z.open(file_name))
                            
                            # تأكد من أن الملف تم حفظه في الموقع المطلوب
                            if default_storage.exists(temp_file_path):
                                media_files[file_name] = temp_file_path

                    except Exception as e:
                        print(f"خطأ أثناء حفظ ملف الوسائط {file_name}: {e}")

    except Exception as e:
        print(f"Erreur lors du traitement du fichier KMZ: {e}")

def export_kml_kmz(request):
    month = request.GET.get('month')
    year = request.GET.get('year')
    archived = request.GET.get('archived')

    locations = Location.objects.all().order_by('-created_at')

    # Apply month and year filtering
    if month and not year:
        current_year = datetime.now().year
        locations = locations.filter(created_at__year=current_year, created_at__month=month)
    elif year:
        locations = locations.filter(created_at__year=year)
        if month:
            locations = locations.filter(created_at__month=month)

    # Apply archived filtering
    if archived == 'archived':
        locations = locations.filter(archived=True)
    elif archived == 'non_archived':
        locations = locations.filter(archived=False)

    paginator = Paginator(locations, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    months = [{'name': datetime(2000, i, 1).strftime('%B'), 'value': i} for i in range(1, 13)]
    years = range(2020, datetime.now().year + 1)

    context = {
        'page_obj': page_obj,
        'months': months,
        'years': years,
    }
    return render(request, 'dashboard_app/web/export_kml_kmz.html', context)

def generate_location_kml(request, location_id):
    # Récupérer les informations du lieu spécifié
    location = get_object_or_404(Location, id=location_id)
    elements = Item.objects.filter(location=location)

    # Création de l'élément racine du fichier KML
    kml = ET.Element('kml', xmlns="http://www.opengis.net/kml/2.2")
    document = ET.SubElement(kml, 'Document')
    ET.SubElement(document, 'name').text = location.name

    # Ajouter les styles
    # Style pour les polygones
    polygon_style = ET.SubElement(document, 'Style', id="polygonStyle")
    poly_linestyle = ET.SubElement(polygon_style, 'LineStyle')
    ET.SubElement(poly_linestyle, 'color').text = 'FF0099CC'  # Couleur de contour en format ABGR
    ET.SubElement(poly_linestyle, 'width').text = '3'
    poly_fillstyle = ET.SubElement(polygon_style, 'PolyStyle')
    ET.SubElement(poly_fillstyle, 'color').text = '99330000'  # Couleur de remplissage en format ABGR

    # Style pour les lignes
    line_style = ET.SubElement(document, 'Style', id="lineStyle")
    line_linestyle = ET.SubElement(line_style, 'LineStyle')
    ET.SubElement(line_linestyle, 'color').text = 'FF0099CC'  # Couleur de la ligne en format ABGR
    ET.SubElement(line_linestyle, 'width').text = '5'

    # Style pour les points
    point_style = ET.SubElement(document, 'Style', id="pointStyle")
    point_iconstyle = ET.SubElement(point_style, 'IconStyle')
    ET.SubElement(point_iconstyle, 'color').text = 'FF0099CC'  # Couleur de l'icône en format ABGR
    ET.SubElement(point_iconstyle, 'scale').text = '2'
    icon = ET.SubElement(point_iconstyle, 'Icon')
    ET.SubElement(icon, 'href').text = 'http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png'

    # Créer un transformateur pour convertir les coordonnées du système de projection à WGS84
    transformer = Transformer.from_crs("EPSG:3857", "EPSG:4326", always_xy=True)  # Modifier "EPSG:3857" selon le système d'origine

    # Ajouter les éléments au fichier KML
    for element in elements:
        placemark = ET.SubElement(document, 'Placemark')
        ET.SubElement(placemark, 'name').text = element.name
        ET.SubElement(placemark, 'description').text = element.description

        # Traiter les données ArcGIS-style GeoJSON
        if element.geojson:
            try:
                geojson_data = json.loads(element.geojson)
                geometry = geojson_data.get('geometry', {})

                # Gérer les types de géométries
                if 'paths' in geometry:  # LineString
                    line_string = ET.SubElement(placemark, 'LineString')
                    coordinates = ET.SubElement(line_string, 'coordinates')
                    path_coords = []
                    for path in geometry.get('paths', []):
                        for point in path:
                            # Convertir les coordonnées en WGS84
                            lon, lat = transformer.transform(point[0], point[1])
                            path_coords.append(f"{lon},{lat},0")
                    coordinates.text = " ".join(path_coords)
                    ET.SubElement(placemark, 'styleUrl').text = '#lineStyle'  # Appliquer le style

                elif 'rings' in geometry:  # Polygon
                    polygon = ET.SubElement(placemark, 'Polygon')
                    outer_boundary = ET.SubElement(polygon, 'outerBoundaryIs')
                    linear_ring = ET.SubElement(outer_boundary, 'LinearRing')
                    coordinates = ET.SubElement(linear_ring, 'coordinates')
                    ring_coords = []
                    for ring in geometry.get('rings', []):
                        for point in ring:
                            # Convertir les coordonnées en WGS84
                            lon, lat = transformer.transform(point[0], point[1])
                            ring_coords.append(f"{lon},{lat},0")
                    coordinates.text = " ".join(ring_coords)
                    ET.SubElement(placemark, 'styleUrl').text = '#polygonStyle'  # Appliquer le style

                elif 'x' in geometry and 'y' in geometry:  # Point
                    point = ET.SubElement(placemark, 'Point')
                    coordinates = ET.SubElement(point, 'coordinates')
                    # Convertir les coordonnées en WGS84
                    lon, lat = transformer.transform(geometry['x'], geometry['y'])
                    coordinates.text = f"{lon},{lat},0"
                    ET.SubElement(placemark, 'styleUrl').text = '#pointStyle'  # Appliquer le style

                else:
                    ET.SubElement(placemark, 'description').text += "\nType de géométrie non pris en charge."

            except (KeyError, json.JSONDecodeError) as e:
                print(f"Erreur lors de l'analyse des données ArcGIS: {e}")

    # Convertir l'arbre XML en chaîne de caractères
    kml_data = ET.tostring(kml, encoding='utf-8', method='xml')

    # Préparer la réponse pour télécharger le fichier KML
    response = HttpResponse(kml_data, content_type="application/vnd.google-earth.kml+xml")
    response['Content-Disposition'] = f'attachment; filename="{location.name}.kml"'

    return response

def generate_location_kmz(request, location_id):
    # Get the specified location and associated items
    location = get_object_or_404(Location, id=location_id)
    elements = Item.objects.filter(location=location)

    # Create the root element of the KML file
    kml = ET.Element('kml', xmlns="http://www.opengis.net/kml/2.2")
    document = ET.SubElement(kml, 'Document')
    ET.SubElement(document, 'name').text = location.name

    # Adding styles for points, lines, and polygons
    polygon_style = ET.SubElement(document, 'Style', id="polygonStyle")
    poly_linestyle = ET.SubElement(polygon_style, 'LineStyle')
    ET.SubElement(poly_linestyle, 'color').text = 'FF0099CC'  # Couleur de contour en format ABGR
    ET.SubElement(poly_linestyle, 'width').text = '3'
    poly_fillstyle = ET.SubElement(polygon_style, 'PolyStyle')
    ET.SubElement(poly_fillstyle, 'color').text = '99330000'  # Couleur de remplissage en format ABGR

    # Style pour les lignes
    line_style = ET.SubElement(document, 'Style', id="lineStyle")
    line_linestyle = ET.SubElement(line_style, 'LineStyle')
    ET.SubElement(line_linestyle, 'color').text = 'FF0099CC'  # Couleur de la ligne en format ABGR
    ET.SubElement(line_linestyle, 'width').text = '5'

    # Style pour les points
    point_style = ET.SubElement(document, 'Style', id="pointStyle")
    point_iconstyle = ET.SubElement(point_style, 'IconStyle')
    ET.SubElement(point_iconstyle, 'color').text = 'FF0099CC'  # Couleur de l'icône en format ABGR
    ET.SubElement(point_iconstyle, 'scale').text = '2'
    icon = ET.SubElement(point_iconstyle, 'Icon')
    ET.SubElement(icon, 'href').text = 'http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png'

    # Transformer for converting coordinates to WGS84
    transformer = Transformer.from_crs("EPSG:3857", "EPSG:4326", always_xy=True)

    # Set up temporary directory for KMZ content
    kmz_dir = os.path.join(settings.MEDIA_ROOT, 'kmz_temp')
    os.makedirs(kmz_dir, exist_ok=True)

    # List of files to include in the KMZ
    file_paths = []

    # Add elements to the KML file
    for element in elements:
        placemark = ET.SubElement(document, 'Placemark')
        ET.SubElement(placemark, 'name').text = element.name
        description = ET.SubElement(placemark, 'description')
        description.text = element.description if element.description else ""

        # Process the GeoJSON data for coordinates
        if element.geojson:
            try:
                geojson_data = json.loads(element.geojson)
                geometry = geojson_data.get('geometry', {})

                # Handle different geometry types
                if 'paths' in geometry:  # LineString
                    line_string = ET.SubElement(placemark, 'LineString')
                    coordinates = ET.SubElement(line_string, 'coordinates')
                    path_coords = []
                    for path in geometry.get('paths', []):
                        for point in path:
                            # Convert coordinates to WGS84
                            lon, lat = transformer.transform(point[0], point[1])
                            path_coords.append(f"{lon},{lat},0")
                    coordinates.text = " ".join(path_coords)
                    ET.SubElement(placemark, 'styleUrl').text = '#lineStyle'

                elif 'rings' in geometry:  # Polygon
                    polygon = ET.SubElement(placemark, 'Polygon')
                    outer_boundary = ET.SubElement(polygon, 'outerBoundaryIs')
                    linear_ring = ET.SubElement(outer_boundary, 'LinearRing')
                    coordinates = ET.SubElement(linear_ring, 'coordinates')
                    ring_coords = []
                    for ring in geometry.get('rings', []):
                        for point in ring:
                            # Convert coordinates to WGS84
                            lon, lat = transformer.transform(point[0], point[1])
                            ring_coords.append(f"{lon},{lat},0")
                    coordinates.text = " ".join(ring_coords)
                    ET.SubElement(placemark, 'styleUrl').text = '#polygonStyle'

                elif 'x' in geometry and 'y' in geometry:  # Point
                    point = ET.SubElement(placemark, 'Point')
                    coordinates = ET.SubElement(point, 'coordinates')
                    # Convert coordinates to WGS84
                    lon, lat = transformer.transform(geometry['x'], geometry['y'])
                    coordinates.text = f"{lon},{lat},0"
                    ET.SubElement(placemark, 'styleUrl').text = '#pointStyle'

            except (KeyError, json.JSONDecodeError) as e:
                print(f"Error processing GeoJSON: {e}")

        # Get media files related to this element
        media_files = MediaModel.objects.filter(item=element)
        for media in media_files:
            media_file_path = os.path.join(settings.MEDIA_ROOT, media.file.name)
            media_basename = os.path.basename(media.file.name)
            target_path = os.path.join(kmz_dir, media_basename)
            if not os.path.exists(target_path):
                with open(target_path, 'wb') as dest:
                    dest.write(open(media_file_path, 'rb').read())
            file_paths.append(target_path)
            description.text += f'<br/><img src="{media_basename}" />'

    # Convert the KML tree to a string
    kml_data = ET.tostring(kml, encoding='utf-8', method='xml')

    # Create a KMZ file
    kmz_filename = f"{location.name}.kmz"
    kmz_path = os.path.join(kmz_dir, kmz_filename)
    with zipfile.ZipFile(kmz_path, 'w', zipfile.ZIP_DEFLATED) as kmz:
        kmz.writestr("doc.kml", kml_data)
        for file_path in file_paths:
            kmz.write(file_path, os.path.basename(file_path))

    # Serve the KMZ file as a download
    response = HttpResponse(open(kmz_path, 'rb'), content_type='application/vnd.google-earth.kmz')
    response['Content-Disposition'] = f'attachment; filename="{kmz_filename}"'

    # Clean up temporary files
    for file_path in file_paths:
        os.remove(file_path)
    os.remove(kmz_path)

    return response

def generate_location_word(request, location_id):
    # Récupérer les informations du lieu spécifié
    location = get_object_or_404(Location, id=location_id)
    elements = Item.objects.filter(location=location)

    # Préparer un fichier zip pour contenir les documents
    today_date = datetime.now().strftime('%Y-%m-%d')
    zip_subdir = f"{today_date}_{location.name}"
    zip_filename = f"{zip_subdir}.zip"
    s = BytesIO()  # Stocker le fichier zip en mémoire
    zf = zipfile.ZipFile(s, "w")

    # Créer un document Word pour chaque élément
    for element in elements:
        doc = Document()
        doc.add_heading(element.name, 0)  # Ajouter le titre de l'élément
        doc.add_paragraph(f"Description: {element.description}")  # Ajouter la description de l'élément

        # Traiter les données ArcGIS-style GeoJSON
        if element.geojson:
            try:
                geojson_data = json.loads(element.geojson)  # Charger les données GeoJSON
                geometry = geojson_data.get('geometry', {})

                # Gérer les types de géométries
                if 'paths' in geometry:  # Probablement un LineString
                    paths = geometry.get('paths', [])
                    doc.add_heading("Type de Géométrie: LineString", level=1)
                    if paths:
                        for index, path in enumerate(paths):
                            for point_index, point in enumerate(path):
                                doc.add_paragraph(f"  Point {point_index + 1}: Longitude: {point[0]}, Latitude: {point[1]}")
                    else:
                        doc.add_paragraph("Données de chemin non trouvées.")

                elif 'rings' in geometry:  # Probablement un Polygon
                    rings = geometry.get('rings', [])
                    doc.add_heading("Type de Géométrie: Polygon", level=1)
                    if rings:
                        for ring_index, ring in enumerate(rings):
                            doc.add_paragraph(f"Anneau {ring_index + 1}:")
                            for point_index, point in enumerate(ring):
                                point_label = f"Point {point_index + 1}"
                                doc.add_paragraph(f"  {point_label}: Longitude: {point[0]}, Latitude: {point[1]}")
                    else:
                        doc.add_paragraph("Données d'anneaux non trouvées pour le polygone.")

                elif 'x' in geometry and 'y' in geometry:  # Probablement un Point
                    x = geometry['x']
                    y = geometry['y']
                    doc.add_heading("Type de Géométrie: Point", level=1)
                    doc.add_paragraph(f"Coordonnées (Longitude, Latitude): {x}, {y}")

                else:
                    doc.add_paragraph("Type de géométrie non pris en charge ou données de géométrie non trouvées.")

            except (KeyError, json.JSONDecodeError) as e:
                print(f"Erreur lors de l'analyse des données ArcGIS: {e}")
                doc.add_paragraph("Erreur lors de l'analyse des données géographiques.")

        # Ajouter les images et vidéos au document Word
        for media in element.media_files.all():
            media_file_path = os.path.join(settings.MEDIA_ROOT, media.file.name)
            if os.path.exists(media_file_path):
                try:
                    if media.file.url.endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp')):
                        doc.add_picture(media_file_path, width=Inches(2))  # Ajouter l'image au document
                        doc.add_paragraph(f"Image: {os.path.basename(media.file.name)}")  # Ajouter le nom de l'image
                    elif media.file.url.endswith(('.mp4', '.avi', '.mov')):
                        doc.add_paragraph(f"Vidéo: {os.path.basename(media.file.name)}")  # Ajouter le nom de la vidéo
                        doc.add_paragraph("Le fichier vidéo est inclus dans le fichier ZIP.")  # Mentionner que la vidéo est dans le zip
                except Exception as e:
                    print(f"Erreur lors de l'ajout du média: {e}")

        # Sauvegarder le document Word dans la mémoire (pas sur le serveur)
        doc_io = BytesIO()
        doc.save(doc_io)
        doc_io.seek(0)

        # Ajouter le document Word au fichier zip avec un nom de fichier unique
        zf.writestr(f"{zip_subdir}/{element.name}_{element.id}.docx", doc_io.read())

        # Ajouter les fichiers média (images et vidéos) au fichier zip
        for media in element.media_files.all():
            media_file_path = os.path.join(settings.MEDIA_ROOT, media.file.name)
            if os.path.exists(media_file_path):
                with open(media_file_path, 'rb') as f:
                    zf.writestr(f"{zip_subdir}/{element.name}/{os.path.basename(media_file_path)}", f.read())

    # Fermer le fichier zip après avoir ajouté tous les fichiers
    zf.close()

    # Préparer la réponse pour télécharger directement le fichier zip
    response = HttpResponse(s.getvalue(), content_type="application/x-zip-compressed")
    response['Content-Disposition'] = f'attachment; filename="{zip_filename}"'

    return response


def user_list(request):
    """Liste tous les utilisateurs."""
    users = User.objects.all()  # Récupérer tous les utilisateurs

    # Gérer les actions du formulaire
    if request.method == 'POST':
        action = request.POST.get('action')
        user_id = request.POST.get('user_id')

        if action == 'add':  # Ajouter un nouvel utilisateur
            username = request.POST['username']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            is_admin = request.POST.get('is_admin') == 'true'  # Vérifier si c'est un administrateur

            if password1 == password2:
                if User.objects.filter(username=username).exists():
                    messages.warning(request, "Le nom d'utilisateur existe déjà.")
                elif User.objects.filter(email=email).exists():
                    messages.warning(request, "L'email existe déjà.")
                else:
                    user = User.objects.create_user(
                        username=username,
                        first_name=first_name,
                        last_name=last_name,
                        email=email,
                        password=password1
                    )
                    if is_admin:
                        user.is_staff = True  # Rendre l'utilisateur administrateur
                        user.is_superuser = True  # Rendre l'utilisateur super administrateur
                    user.save()  # Enregistrer l'utilisateur
                    messages.success(request, "L'utilisateur a été ajouté avec succès.")
                    return redirect('user-list')
            else:
                messages.warning(request, "Les mots de passe ne correspondent pas.")
        
        elif action == 'delete':
            user = get_object_or_404(User, id=user_id)  # Récupérer l'utilisateur à supprimer
            if user.is_superuser and User.objects.filter(is_superuser=True).count() <= 1:
                messages.warning(request, "Vous ne pouvez pas supprimer le seul administrateur.")
            else:
                user.delete()  # Supprimer l'utilisateur
                messages.success(request, "L'utilisateur a été supprimé avec succès.")
        
        elif action == 'archive':
            user = get_object_or_404(User, id=user_id)  # Récupérer l'utilisateur à archiver
            user.is_active = False  # Archiver l'utilisateur
            user.save()
            messages.success(request, "L'utilisateur a été archivé avec succès.")
        
        elif action == 'activate':
            user = get_object_or_404(User, id=user_id)  # Récupérer l'utilisateur à activer
            user.is_active = True  # Activer l'utilisateur
            user.save()
            messages.success(request, "L'utilisateur a été activé avec succès.")

        elif action == 'edit':
            user = get_object_or_404(User, id=user_id)  # Récupérer l'utilisateur à modifier
            user.username = request.POST['username']
            user.email = request.POST['email']
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            if request.POST['password']:
                user.set_password(request.POST['password'])  # Changer le mot de passe si fourni
            user.save()  # Enregistrer les modifications
            messages.success(request, "Les informations de l'utilisateur ont été mises à jour avec succès.")

    return render(request, 'dashboard_app/web/user_list.html', {'users': users})
