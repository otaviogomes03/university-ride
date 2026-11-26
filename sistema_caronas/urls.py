from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Conecta a sua funcionalidade na URL /busca/
    path('busca/', include('busca_match.urls')), 
    path('pagamento/', include('pagamento.urls')),
    path('', include('contas.urls')),
]