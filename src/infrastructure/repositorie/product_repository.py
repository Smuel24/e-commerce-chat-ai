from src.domain.repositories import IProductRepository
from src.domain.entities import Product
from src.infrastructure.db.models import ProductModel
from sqlalchemy.orm import Session

class SQLProductRepository(IProductRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        models = self.db.query(ProductModel).all()
        return [self._model_to_entity(m) for m in models]

    def get_by_id(self, product_id: int):
        model = self.db.query(ProductModel).filter(ProductModel.id == product_id).first()
        return self._model_to_entity(model) if model else None

    def get_by_brand(self, brand: str):
        models = self.db.query(ProductModel).filter(ProductModel.brand == brand).all()
        return [self._model_to_entity(m) for m in models]

    def get_by_category(self, category: str):
        models = self.db.query(ProductModel).filter(ProductModel.category == category).all()
        return [self._model_to_entity(m) for m in models]

    def save(self, product: Product):
        if product.id:
            # Actualizar producto existente
            model = self.db.query(ProductModel).filter(ProductModel.id == product.id).first()
            if not model:
                return None
            for key, value in self._entity_to_model(product).__dict__.items():
                if key != "_sa_instance_state":
                    setattr(model, key, value)
        else:
            # Crear nuevo producto
            model = self._entity_to_model(product)
            self.db.add(model)
            self.db.flush()  # Para generar el id
            self.db.refresh(model)
            product.id = model.id
        self.db.commit()
        return self._model_to_entity(model)

    def delete(self, product_id: int):
        model = self.db.query(ProductModel).filter(ProductModel.id == product_id).first()
        if model:
            self.db.delete(model)
            self.db.commit()
            return True
        return False

    # Métodos auxiliares
    def _model_to_entity(self, model):
        if not model: return None
        return Product(
            id=model.id,
            name=model.name,
            brand=model.brand,
            category=model.category,
            size=model.size,
            color=model.color,
            price=model.price,
            stock=model.stock,
            description=model.description,
        )

    def _entity_to_model(self, entity):
        return ProductModel(
            id=entity.id,
            name=entity.name,
            brand=entity.brand,
            category=entity.category,
            size=entity.size,
            color=entity.color,
            price=entity.price,
            stock=entity.stock,
            description=entity.description,
        )