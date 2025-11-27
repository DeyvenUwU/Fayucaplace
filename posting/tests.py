from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from posting.models import Categoria, SubCategoria, Publicacion


class PublicacionAPITests(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='u1', password='pass12345')
		self.other = User.objects.create_user(username='u2', password='pass12345')
		self.cat = Categoria.objects.create(nombre='Cat A')
		self.sub = SubCategoria.objects.create(categoria=self.cat, nombre='Sub 1')
		self.client = APIClient()
		# Autenticar
		self.client.login(username='u1', password='pass12345')

	def test_create_article_publicacion(self):
		url = '/api/publicaciones/'
		data = {
			'titulo': 'Articulo Test', 
			'descripcion': 'Desc',
			'subcategoria': self.sub.id,
			'precio': '12.50',
			'cantidad': 3
		}
		r = self.client.post(url, data, format='multipart')
		self.assertEqual(r.status_code, 201)
		self.assertEqual(Publicacion.objects.count(), 1)
		pub = Publicacion.objects.first()
		self.assertIsNotNone(pub.articulo)

	def test_list_publicaciones(self):
		Publicacion.objects.create(titulo='P1', descripcion='D', idUsuario=self.user)
		r = self.client.get('/api/publicaciones/')
		self.assertEqual(r.status_code, 200)
		self.assertGreaterEqual(len(r.json()), 1)

	def test_update_publicacion_owner(self):
		pub = Publicacion.objects.create(titulo='Orig', descripcion='D', idUsuario=self.user)
		url = f'/api/publicaciones/{pub.id}/'
		r = self.client.put(url, {'titulo': 'Nuevo', 'descripcion': 'DX'}, format='multipart')
		self.assertEqual(r.status_code, 200)
		pub.refresh_from_db()
		self.assertEqual(pub.titulo, 'Nuevo')

	def test_update_publicacion_not_owner_forbidden(self):
		pub = Publicacion.objects.create(titulo='Orig', descripcion='D', idUsuario=self.other)
		url = f'/api/publicaciones/{pub.id}/'
		r = self.client.put(url, {'titulo': 'Hack', 'descripcion': 'X'}, format='multipart')
		# IsOwnerOrReadOnly should forbid modification
		self.assertIn(r.status_code, (403, 401))

	def test_delete_publicacion_owner(self):
		pub = Publicacion.objects.create(titulo='Del', descripcion='D', idUsuario=self.user)
		url = f'/api/publicaciones/{pub.id}/'
		r = self.client.delete(url)
		self.assertEqual(r.status_code, 204)
		self.assertFalse(Publicacion.objects.filter(id=pub.id).exists())

	def test_filter_search(self):
		Publicacion.objects.create(titulo='Celular nuevo', descripcion='D', idUsuario=self.user)
		Publicacion.objects.create(titulo='Laptop usada', descripcion='D', idUsuario=self.user)
		r = self.client.get('/api/publicaciones/?search=celu')
		self.assertEqual(r.status_code, 200)
		data = r.json()
		self.assertEqual(len(data), 1)
		self.assertIn('Celular nuevo', data[0]['titulo'])
