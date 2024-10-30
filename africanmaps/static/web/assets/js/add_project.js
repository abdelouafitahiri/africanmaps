let activeGraphic = null;
let graphicsLayer = null;

window.deleteGraphicAndClose = function () {
  if (activeGraphic && graphicsLayer) {
    graphicsLayer.remove(activeGraphic); // إزالة الرسم
    activeGraphic = null; // إعادة تعيين activeGraphic إلى null
  }
  closePopupModal();
};

window.closePopupModal = function () {
  const modalElement = document.getElementById("popupModal");
  const modal = bootstrap.Modal.getInstance(modalElement);
  if (modal) {
    modal.hide();
  }
};

window.openPopupModal = function () {
  const modalElement = document.getElementById("popupModal");
  const modal = new bootstrap.Modal(modalElement);
  modal.show();

  // تعبئة الحقول بالبيانات من activeGraphic إذا كانت موجودة
  document.getElementById("featureName").value = activeGraphic && activeGraphic.attributes ? activeGraphic.attributes.name || '' : '';
  document.getElementById("featureDescription").value = activeGraphic && activeGraphic.attributes ? activeGraphic.attributes.description || '' : '';
  document.getElementById("geojsonData").value = activeGraphic ? JSON.stringify(activeGraphic.toJSON()) : '';
};

// إضافة حدث إزالة الرسم عند إغلاق الـ modal
document.addEventListener("DOMContentLoaded", function() {
  const modalElement = document.getElementById("popupModal");

  modalElement.addEventListener("hidden.bs.modal", function () {
    if (activeGraphic && graphicsLayer) {
      graphicsLayer.remove(activeGraphic); // إزالة الرسم من الطبقة
      activeGraphic = null; // إعادة تعيين activeGraphic إلى null
    }
  });
});


require([
  "esri/Map",
  "esri/views/MapView",
  "esri/layers/GraphicsLayer",
  "esri/widgets/Sketch/SketchViewModel",
  "esri/widgets/Sketch",
  "esri/widgets/Search",
  "esri/widgets/Expand",
  "esri/widgets/BasemapGallery",
  "esri/widgets/Fullscreen",
  "esri/Basemap",
  "esri/Graphic",
  "esri/geometry/Point",
  "esri/geometry/Polygon",
  "esri/geometry/Polyline"
], function(Map, MapView, GraphicsLayer, SketchViewModel, Sketch, Search, Expand, BasemapGallery, Fullscreen, Basemap, Graphic, Point, Polygon, Polyline) {

  const map = new Map({
    basemap: "satellite" // Changer la carte de base par défaut à Imagerie
  });

  const view = new MapView({
    container: "viewDiv",
    map: map,
    center: [-6.8498, 34.0209],
    zoom: 16,
    ui: {
      components: ["zoom"] // Supprimer les autres composants y compris l'attribution
    }

  });

  

  graphicsLayer = new GraphicsLayer();
  map.add(graphicsLayer);

  const sketchViewModel = new SketchViewModel({
    view: view,
    layer: graphicsLayer,
    snappingOptions: {
        enabled: true,
        featureEnabled: true,
        selfEnabled: true,
        featureSources: [{ layer: graphicsLayer }]
    },
    // تخصيص الألوان للبوليغون
    polygonSymbol: {
        type: "simple-fill", 
        color: [19,23,44, 0.5],
        outline: {
        color: [255, 165, 0],
        width: 2,
    }
    },
    // تخصيص الألوان للخطوط
    polylineSymbol: {
        type: "simple-line",
        color: [255, 165, 0],
        width: 2,
    },
    // تخصيص الألوان للنقاط
    pointSymbol: {
        type: "simple-marker",
        style: "circle",
        color: [19,23,44, 0.95],
        size: "13px",
        outline: {
          color: [255, 165, 0],
          width: 2
        }
    },
            
    activeLineSymbol: {
        type: "simple-line", // Active drawing symbol
        color: [19,23,44],  // Green color for the polyline during active drawing
        width: 2,
        style: "solid"  // Make sure the line style is solid, no dashed line
    },

  });

  // إعداد Sketch وربطه مع SketchViewModel
  const sketch = new Sketch({
      view: view,
      layer: graphicsLayer,
      viewModel: sketchViewModel,
      layout: "vertical",
      visibleElements: {
          undoRedoMenu: false,
          settingsMenu: true,
          featureCount: false,
          duplicateFeature: false,
          deleteFeature: false
      }
  });

  // تمكين خيارات التلميحات في الـ Sketch
  sketch.tooltipOptions.enabled = true;
  


  // إنشاء زر Undo
  const undoButton = document.createElement("div");
  undoButton.className = "esri-widget--button esri-interactive";
  undoButton.title = "Undo";
  undoButton.innerHTML = '<span class="esri-icon-undo"></span>';
  undoButton.onclick = () => {
      sketchViewModel.undo();
  };

  // إنشاء زر Redo
  const redoButton = document.createElement("div");
  redoButton.className = "esri-widget--button esri-interactive";
  redoButton.title = "Redo";
  redoButton.innerHTML = '<span class="esri-icon-redo"></span>';
  redoButton.onclick = () => {
      sketchViewModel.redo();
  };

  undoButton.style.visibility = "hidden";
  redoButton.style.visibility = "hidden";

  function showUndoRedoButtons() {
      undoButton.style.visibility = "visible";
      redoButton.style.visibility = "visible";
  }

  function hideUndoRedoButtons() {
      undoButton.style.visibility = "hidden";
      redoButton.style.visibility = "hidden";
  }

  const fullscreen = new Fullscreen({
      view: view 
  });

  view.ui.add(fullscreen, "top-right");


  // إنشاء عنصر Search Widget
  const searchWidget = new Search({
    view: view,
    allPlaceholder: "Search for a place",
    locationEnabled: true // لتفعيل زر "Use current location"
  });

  // نستخدم عنصر Expand لتفعيل البحث عند النقر
  const searchExpand = new Expand({
      view: view,
      content: searchWidget,
      expandIconClass: "esri-icon-search", // أيقونة البحث
      expandTooltip: "Click to search", // نص الإرشاد عند تمرير الفأرة
      expanded: false // تأكد من أنه غير مفعل تلقائيًا حتى يظهر فقط عند النقر
  });

  
  // إنشاء عنصر BasemapGallery
  const basemapGallery = new BasemapGallery({
      view: view
  });

  // استخدام عنصر Expand لعرض BasemapGallery بشكل أفضل
  const basemapExpand = new Expand({
      view: view,
      content: basemapGallery,
      expandIconClass: "esri-icon-basemap", // أيقونة خريطة أساس
      expandTooltip: "Toggle Basemap Gallery" // نص توضيحي يظهر عند تمرير الماوس
  });


  // نقل أداة التكبير والتصغير إلى الأعلى اليسار
  view.ui.move("zoom", "top-right");

  
  
  const sketchExpand = new Expand({
      view: view,
      content: sketch,
      expandIconClass: "analysis-overlay",
      expandTooltip: "Click to draw",
      expanded: false,
      mode: "floating"
  });

  view.ui.add(sketchExpand, {
      position: "top-left",
      index: 1
  });

  view.ui.add(undoButton, "top-left");
  view.ui.add(redoButton, "top-left");


  
  // إضافة عنصر Expand إلى واجهة المستخدم في الموضع المطلوب
  view.ui.add(basemapExpand, {
      position: "top-right"
  });

  // إضافة أداة Expand إلى واجهة المستخدم مع أداة البحث
  view.ui.add(searchExpand, {
      position: "top-right",
      index: 2 // ترتيب أعلى بقليل من أداة التكبير وأداة الرسم
  });

  sketch.on("create", function (event) {
    if (event.state === "start") {
      showUndoRedoButtons(); 

    } else if (event.state === "complete") {
      activeGraphic = event.graphic; // تخزين العنصر المرسوم كعنصر نشط
      openPopupModal();
      hideUndoRedoButtons(); // إخفاء الأزرار عند اكتمال الرسم
    }
  });


  // Se déplacer vers l'emplacement de l'utilisateur au chargement de la carte
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      function (position) {
        const { latitude, longitude } = position.coords;
        view.center = [longitude, latitude];
        view.zoom = 18;

        // Ajouter un point pour l'emplacement de l'utilisateur
        const pointGraphic = {
          geometry: {
            type: "point",
            longitude: longitude,
            latitude: latitude
          },
          symbol: {
            type: "simple-marker",
            style: "circle",
            color: [36, 105, 92, 0.95],
            size: "16px",
            outline: { color: [220, 220, 220, 1], width: 1.5 }
          }
        };
        graphicsLayer.add(pointGraphic);
      },
      function () {
        console.error("Impossible d'obtenir la position de l'utilisateur.");
      },
      { enableHighAccuracy: true }

    );
  }

  // Afficher la fenêtre modale lors du clic sur l'élément dessiné
  view.on("click", function(event) {
    view.hitTest(event).then(function(response) {
      const graphic = response.results[0]?.graphic;
      if (graphic && graphic.layer === graphicsLayer) {
        activeGraphic = graphic;
        openPopupModal();
      }
    });
  });
});


// Utilisation de MutationObserver pour changer la langue de l'interface en français
const observer = new MutationObserver((mutations) => {
  mutations.forEach((mutation) => {
    if (mutation.type === "childList") {
      document.querySelectorAll(".esri-sketch__button").forEach((button) => {
        const title = button.getAttribute("title");
        switch (title) {
          case "Select feature":
            button.setAttribute("title", "Sélectionner un élément");
            break;
          case "Select by rectangle":
            button.setAttribute("title", "Sélectionner par rectangle");
            break;
          case "Select by lasso":
            button.setAttribute("title", "Sélectionner par lasso");
            break;
          case "Draw a polygon":
            button.setAttribute("title", "Dessiner un polygone");
            break;
          case "Draw a polyline":
            button.setAttribute("title", "Dessiner une ligne");
            break;
          case "Draw a point":
            button.setAttribute("title", "Dessiner un point");
            break;
          case "Draw a rectangle":
            button.setAttribute("title", "Dessiner un rectangle");
            break;
          case "Draw a circle":
            button.setAttribute("title", "Dessiner un cercle");
            break;
          case "Undo":
            button.setAttribute("title", "Annuler");
            break;
          case "Redo":
            button.setAttribute("title", "Rétablir");
            break;
          case "Sketch settings":
            button.setAttribute("title", "Paramètres du croquis");
            break;
          default:
            break;
        }
      });
      document.querySelectorAll(".esri-sketch__menu-title, .esri-sketch__item-action-title").forEach((element) => {
          if (element.textContent === "Sketch settings") {
            element.textContent = "Paramètres du croquis";
          } else if (element.textContent === "Snapping enabled") {
            element.textContent = "Accrochage activé";
          }

        });
      document.querySelectorAll(".esri-widget--button[title='Zoom in']").forEach((element) => {
          element.setAttribute("title", "Zoom avant");
          const fallbackText = element.querySelector(".esri-icon-font-fallback-text");
          if (fallbackText) {
              fallbackText.textContent = "Zoom avant";
          }
      });
      document.querySelectorAll(".esri-widget--button[title='Zoom out']").forEach((element) => {
          element.setAttribute("title", "Zoom arrière");
          const fallbackText = element.querySelector(".esri-icon-font-fallback-text");
          if (fallbackText) {
              fallbackText.textContent = "Zoom arrière";
          }
      });
      document.querySelectorAll(".esri-sketch__menu-title, .esri-sketch__item-action-title").forEach((element) => {
          switch (element.textContent.trim()) {
              case "Undo":
                  element.textContent = "Annuler";
                  break;
              case "Redo":
                  element.textContent = "Rétablir";
                  break;
              case "Delete":
                  element.textContent = "Supprimer";
                  break;
              // Ajoutez d'autres cas si nécessaire
          }
      });
      document.querySelectorAll(".esri-search__input").forEach((element) => {
          element.setAttribute("placeholder", "Trouver une adresse ou un lieu");
          element.setAttribute("title", "Trouver une adresse ou un lieu");
          element.setAttribute("aria-label", "Recherche");
      });
      document.querySelectorAll(".esri-search__submit-button[title='Search']").forEach((element) => {
          element.setAttribute("title", "Rechercher");
          element.setAttribute("aria-label", "Rechercher");
      });

      document.querySelectorAll(".esri-search__suggestions-list--current-location .esri-menu__list-item").forEach((element) => {
        if (element.textContent.trim() === "Use current location") {
            // Modifier le texte
            element.textContent = "Utiliser la position actuelle";

            // Ajouter une icône devant le texte
            const iconSpan = document.createElement("span");
            iconSpan.className = "esri-icon-locate-circled"; // Classe de l'icône existante ou une autre classe d'icône
            iconSpan.style.marginRight = "5px"; // Optionnel : pour ajouter un espace entre l'icône et le texte

            // Insérer l'icône avant le texte
            element.prepend(iconSpan);
        }
      });

      document.querySelectorAll(".esri-search__no-value-text").forEach((element) => {
          if (element.textContent.trim() === "Please enter a search term.") {
              element.textContent = "Veuillez saisir un terme de recherche.";
          }
      });
      document.querySelectorAll("*").forEach((element) => {
          if (element.textContent.trim() === "Loading") {
              element.textContent = "Chargement";
          }
      });
      }
      // Traduction des éléments de l'interface utilisateur de la popup
      document.querySelectorAll(".esri-popup__button[title='Zoom to']").forEach((element) => {
          element.setAttribute("title", "Zoomer");
          element.querySelector(".esri-popup__action-text").textContent = "Zoomer";
      });

      document.querySelectorAll(".esri-popup__feature-menu-header").forEach((element) => {
          element.textContent = element.textContent.replace("results", "résultats");
      });

      document.querySelectorAll(".esri-popup__header-container[title='Collapse']").forEach((element) => {
          element.setAttribute("title", "Réduire");
      });

      document.querySelectorAll(".esri-popup__button--dock[title='Undock']").forEach((element) => {
          element.setAttribute("title", "Détacher");
          element.setAttribute("aria-label", "Détacher");
      });

      document.querySelectorAll(".esri-popup__button[title='Close']").forEach((element) => {
          element.setAttribute("title", "Fermer");
          element.setAttribute("aria-label", "Fermer");
      });

      document.querySelectorAll(".esri-popup__header-title").forEach((element) => {
          if (element.textContent.trim() === "Search result") {
              element.textContent = "Résultat de la recherche";
          }
      });

      document.querySelectorAll(".esri-search-result-renderer__more-results-item a").forEach((element) => {
          if (element.textContent.trim() === "Show more results") {
              element.textContent = "Afficher plus de résultats";
          }
          else if (element.textContent.trim() === "Hide") {
              element.textContent = "Cacher";
          }

      });
      // Traduction des éléments de l'interface utilisateur pour les avertissements de recherche

      document.querySelectorAll(".esri-search__warning-header").forEach((element) => {
        if (element.textContent.trim() === "No results") {
            element.textContent = "Aucun résultat";
        }
      });

      document.querySelectorAll(".esri-search__warning-text").forEach((element) => {
        if (element.textContent.includes("There were no results found for")) {
          const searchTerm = element.textContent.match(/"(.*?)"/)[0]; // Trouver le texte entre guillemets
          element.textContent = `Aucun résultat trouvé pour ${searchTerm}.`;
      }
      });

  });
});

// Observer les modifications du DOM pour changer les titres des boutons
observer.observe(document.body, {
  childList: true,
  subtree: true
});
