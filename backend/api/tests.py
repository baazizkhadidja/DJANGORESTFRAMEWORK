import pytest
from django.urls import reverse
from rest_framework import status
from api.models import Product, Category
from rest_framework.test import APIClient
from api.serializer import ProductSerializer



@pytest.mark.django_db
class TestProductAPI:

    @pytest.fixture
    def client(self):
        return APIClient()

    @pytest.fixture
    def category(self):
        """Crée une catégorie pour les produits"""
        return Category.objects.create(name="Électronique")

    @pytest.fixture
    def product(self, category):
        """Crée un produit pour les tests"""
        return Product.objects.create(title="Laptop", price=999, categorie=category)

    def test_get_all_products(self, client, product):
        """GET /products/ doit retourner la liste des produits"""
        url = reverse('product-list')
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1
        assert 'title' in response.data[0]

    def test_create_product(self, client, category):
        """POST /products/ doit créer un nouveau produit"""
        url = reverse('product-list')
        data = {
            "title": "Smartphone",
            "price": 599,
            "categorie": category.id
        }
        response = client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Product.objects.count() == 1
        assert Product.objects.first().title == "Smartphone"

    def test_get_single_product(self, client, product):
        """GET /products/<id>/ doit retourner un produit"""
        url = reverse('product-detail', kwargs={'pk': product.pk})
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == "Laptop"

    def test_update_product(self, client, product, category):
        """PUT /products/<id>/ doit modifier un produit"""
        url = reverse('product-detail', kwargs={'pk': product.pk})
        data = {
            "title": "Laptop Pro",
            "price": 1299,
            "categorie": category.id
        }
        response = client.put(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        product.refresh_from_db()
        assert product.title == "Laptop Pro"

    def test_delete_product(self, client, product):
        """DELETE /products/<id>/ doit supprimer le produit"""
        url = reverse('product-detail', kwargs={'pk': product.pk})
        response = client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Product.objects.count() == 0

    def test_get_nonexistent_product(self, client):
        """GET /products/999/ doit renvoyer 404"""
        url = reverse('product-detail', kwargs={'pk': 999})
        response = client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_product_str(self, product):
        assert str(product) == "Laptop"

    def test_invalid_serializer(self,category):
        data = {"title": "", "price": None, "categorie": category.id}
        serializer = ProductSerializer(data=data)
        assert not serializer.is_valid()
        assert "title" in serializer.errors
