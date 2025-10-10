from typing import List, Dict, Any
from src.domain.entities import Product
from src.domain.repositories import IProductRepository
from src.domain.exceptions import ProductNotFoundError, InvalidProductDataError
from src.application.dtos import ProductDTO

class ProductService:
    """
    Servicio de aplicación para productos.
    """

    def __init__(self, product_repository: IProductRepository):
        self.product_repository = product_repository

    def get_all_products(self) -> List[Product]:
        """Lista todos los productos"""
        return self.product_repository.get_all()

    def get_product_by_id(self, product_id: int) -> Product:
        """Busca producto por ID, lanza excepción si no existe"""
        product = self.product_repository.get_by_id(product_id)
        if not product:
            raise ProductNotFoundError(product_id)
        return product

    def search_products(self, filters: Dict[str, Any]) -> List[Product]:
        """
        Filtra productos por criterios.
        filters: dict con posibles claves: 'brand', 'category', 'name', etc.
        """
        products = self.product_repository.get_all()
        for key, value in filters.items():
            if key == "brand":
                products = [p for p in products if p.brand.lower() == value.lower()]
            elif key == "category":
                products = [p for p in products if p.category.lower() == value.lower()]
            elif key == "name":
                products = [p for p in products if value.lower() in p.name.lower()]
            elif key == "size":
                products = [p for p in products if value.lower() in p.size.lower()]
            elif key == "color":
                products = [p for p in products if value.lower() in p.color.lower()]
            # Puedes agregar más filtros aquí si es necesario
        return products

    def create_product(self, product_dto: ProductDTO) -> Product:
        """Crea un nuevo producto a partir del DTO"""
        try:
            product = Product(
                id=None,
                name=product_dto.name,
                brand=product_dto.brand,
                category=product_dto.category,
                size=product_dto.size,
                color=product_dto.color,
                price=product_dto.price,
                stock=product_dto.stock,
                description=product_dto.description
            )
        except ValueError as e:
            raise InvalidProductDataError(str(e))
        return self.product_repository.save(product)

    def update_product(self, product_id: int, product_dto: ProductDTO) -> Product:
        """Actualiza producto existente, lanza excepción si no existe"""
        product = self.product_repository.get_by_id(product_id)
        if not product:
            raise ProductNotFoundError(product_id)
        # Actualizar campos
        product.name = product_dto.name
        product.brand = product_dto.brand
        product.category = product_dto.category
        product.size = product_dto.size
        product.color = product_dto.color
        product.price = product_dto.price
        product.stock = product_dto.stock
        product.description = product_dto.description
        try:
            product.__post_init__()  # Validar nuevos datos
        except ValueError as e:
            raise InvalidProductDataError(str(e))
        return self.product_repository.save(product)

    def delete_product(self, product_id: int) -> bool:
        """Elimina producto, lanza excepción si no existe"""
        product = self.product_repository.get_by_id(product_id)
        if not product:
            raise ProductNotFoundError(product_id)
        return self
