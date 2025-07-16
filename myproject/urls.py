from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Scraping API",
        default_version='v1',
        description="API exposant des données scrapées",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

def home(request):
    return redirect('schema-swagger-ui')

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),

    # Swagger UI
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    # Inclure scraping_data avec namespace
    path('api/', include('scraping_data.urls', namespace='scraping_data')),
    path('api-tester/', include('api_tester.urls')),
]
