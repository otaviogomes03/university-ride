from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from django.views.generic import RedirectView

from .forms import EmailAuthenticationForm
from .views import cadastro


urlpatterns = [
    path("", RedirectView.as_view(pattern_name="cadastro", permanent=False), name="inicio"),
    path("cadastro/", cadastro, name="cadastro"),
    path(
        "entrar/",
        LoginView.as_view(
            template_name="contas/entrar.html",
            authentication_form=EmailAuthenticationForm,
            redirect_authenticated_user=True,
        ),
        name="entrar",
    ),
    path("sair/", LogoutView.as_view(next_page="entrar"), name="sair"),
]
