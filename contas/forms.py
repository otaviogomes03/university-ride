from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Q


class CadastroForm(UserCreationForm):
    """Cria uma conta usando o e-mail como nome de usuário."""

    nome_completo = forms.CharField(
        label="Nome completo",
        max_length=150,
        widget=forms.TextInput(
            attrs={"placeholder": "Seu nome e sobrenome", "autocomplete": "name"}
        ),
    )
    # O User.username do Django tem limite de 150 caracteres.
    email = forms.EmailField(
        label="E-mail",
        max_length=150,
        widget=forms.EmailInput(
            attrs={"placeholder": "voce@universidade.edu.br", "autocomplete": "email"}
        ),
    )

    class Meta:
        model = User
        fields = ("nome_completo", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].label = "Senha"
        self.fields["password2"].label = "Confirmar senha"
        self.fields["password1"].widget.attrs.update(
            {"placeholder": "Crie uma senha", "autocomplete": "new-password"}
        )
        self.fields["password2"].widget.attrs.update(
            {"placeholder": "Repita sua senha", "autocomplete": "new-password"}
        )

    def clean_nome_completo(self):
        nome = " ".join(self.cleaned_data["nome_completo"].split())
        if len(nome.split()) < 2:
            raise forms.ValidationError("Informe seu nome e sobrenome.")
        return nome

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(Q(username__iexact=email) | Q(email__iexact=email)).exists():
            raise forms.ValidationError("Este e-mail já está cadastrado.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        primeiro_nome, sobrenome = self.cleaned_data["nome_completo"].split(" ", 1)
        email = self.cleaned_data["email"]
        user.username = email
        user.email = email
        user.first_name = primeiro_nome
        user.last_name = sobrenome
        if commit:
            user.save()
        return user


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label="E-mail",
        max_length=150,
        widget=forms.EmailInput(
            attrs={"placeholder": "seu@email.com", "autocomplete": "email"}
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password"].widget.attrs.update(
            {"placeholder": "Sua senha", "autocomplete": "current-password"}
        )

    def clean_username(self):
        return self.cleaned_data["username"].strip().lower()
