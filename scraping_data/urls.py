from django.urls import path
from .views import (
    ProductListView,
    ProductDetailView,
    ProductFetchAPIView,
    SwaggerScrapeAPIView,
    afficher_rapport_swagger,
    rapport_swagger_pdf,
    lancer_scraping,
    list_projects,
    add_project,       # ajouté
    edit_project,      # ajouté
    delete_project,    # ajouté
)

app_name = 'scraping_data'

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('products/fetch/', ProductFetchAPIView.as_view(), name='product-fetch'),

    path('rapport-swagger/', afficher_rapport_swagger, name='rapport-swagger-html'),
    path('rapport-swagger/pdf/', rapport_swagger_pdf, name='rapport-swagger-pdf'),

    path('swagger/endpoints/', SwaggerScrapeAPIView.as_view(), name='swagger-endpoints'),
    path('lancer-scraping/', lancer_scraping, name='lancer-scraping'),

    path('list-projects/', list_projects, name='list-projects'),

    # Ajouts pour CRUD projets Swagger
    path('projects/add/', add_project, name='add-project'),
    path('projects/<int:pk>/edit/', edit_project, name='edit-project'),
    path('projects/<int:pk>/delete/', delete_project, name='delete-project'),
]