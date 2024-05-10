from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile


from apostilas.models import Apostila, Avaliacao, ViewApostila


class BaseTestMixin(TestCase):
    def get_user(self, username='test', password='123456'):
        user = User.objects.create_user(
            username=username,
            password=password
        )
        user.save()
        return user

    def make_apostila(self):
        user = self.get_user()
        file_content = b'test test'
        arquivo = SimpleUploadedFile("arquivo.txt", file_content)

        apostila = Apostila.objects.create(
            user=user,
            titulo='apostila test',
            arquivo=arquivo

        )
        apostila.save()
        return apostila

    def make_view_apostila(self):
        apostila = self.make_apostila()

        view_apostila = ViewApostila.objects.create(
            ip='192.0.2.0',
            apostila=apostila
        )
        view_apostila.save()
        return view_apostila

    def make_avaliacao(self):
        avaliacao = Avaliacao.objects.create(
            avaliacao='bom'
        )
        avaliacao.save()
        return avaliacao