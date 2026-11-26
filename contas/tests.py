from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse


User = get_user_model()


class CadastroTests(TestCase):
    def setUp(self):
        self.dados = {
            "nome_completo": "Ana Maria Ferreira",
            "email": "ana@universidade.edu.br",
            "password1": "ExemploSeguro#9817",
            "password2": "ExemploSeguro#9817",
        }

    def test_exibe_tela_de_cadastro(self):
        resposta = self.client.get(reverse("cadastro"))
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, "Crie sua conta")
        self.assertContains(resposta, "csrfmiddlewaretoken")

    def test_cadastra_usuario_com_senha_criptografada_e_faz_login(self):
        resposta = self.client.post(reverse("cadastro"), self.dados)
        self.assertRedirects(resposta, reverse("busca_carona"))

        usuario = User.objects.get(username="ana@universidade.edu.br")
        self.assertEqual(usuario.email, "ana@universidade.edu.br")
        self.assertEqual(usuario.first_name, "Ana")
        self.assertEqual(usuario.last_name, "Maria Ferreira")
        self.assertTrue(usuario.check_password(self.dados["password1"]))
        self.assertEqual(str(self.client.session["_auth_user_id"]), str(usuario.pk))

    def test_impede_email_duplicado_ignorando_maiusculas(self):
        User.objects.create_user(
            username="ana@universidade.edu.br",
            email="ana@universidade.edu.br",
            password="OutraSenha#9817",
        )
        dados = {**self.dados, "email": "ANA@UNIVERSIDADE.EDU.BR"}
        resposta = self.client.post(reverse("cadastro"), dados)
        self.assertEqual(resposta.status_code, 200)
        self.assertIn("email", resposta.context["form"].errors)
        self.assertEqual(User.objects.count(), 1)

    def test_rejeita_senhas_diferentes(self):
        dados = {**self.dados, "password2": "SenhaDiferente#9817"}
        resposta = self.client.post(reverse("cadastro"), dados)
        self.assertIn("password2", resposta.context["form"].errors)
        self.assertFalse(User.objects.exists())

    def test_rejeita_senha_fraca(self):
        dados = {**self.dados, "password1": "123", "password2": "123"}
        resposta = self.client.post(reverse("cadastro"), dados)
        self.assertIn("password2", resposta.context["form"].errors)
        self.assertFalse(User.objects.exists())

    def test_login_e_logout(self):
        self.client.post(reverse("cadastro"), self.dados)
        self.client.post(reverse("sair"))
        self.assertNotIn("_auth_user_id", self.client.session)

        resposta = self.client.post(
            reverse("entrar"),
            {"username": "ANA@UNIVERSIDADE.EDU.BR", "password": self.dados["password1"]},
        )
        self.assertRedirects(resposta, reverse("busca_carona"))
        self.assertIn("_auth_user_id", self.client.session)

    def test_post_sem_token_csrf_e_rejeitado(self):
        cliente = Client(enforce_csrf_checks=True)
        resposta = cliente.post(reverse("cadastro"), self.dados)
        self.assertEqual(resposta.status_code, 403)
        self.assertFalse(User.objects.exists())
