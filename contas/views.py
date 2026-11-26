from django.contrib.auth import login
from django.db import IntegrityError, transaction
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from .forms import CadastroForm


@require_http_methods(["GET", "POST"])
def cadastro(request):
    if request.user.is_authenticated:
        return redirect("busca_carona")

    form = CadastroForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        try:
            with transaction.atomic():
                user = form.save()
        except IntegrityError:
            # Trata também uma possível disputa entre cadastros simultâneos.
            form.add_error("email", "Este e-mail já está cadastrado.")
        else:
            login(request, user)
            return redirect("busca_carona")

    return render(request, "contas/cadastro.html", {"form": form})
