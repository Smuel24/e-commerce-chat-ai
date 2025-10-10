from src.infrastructure.db.models import ProductModel
from src.infrastructure.db.database import SessionLocal, init_db

def load_initial_data():
    session = SessionLocal()
    try:
        # Verifica si ya existen productos
        if session.query(ProductModel).count() > 0:
            print("Productos ya cargados en la base de datos.")
            return

        # Lista de productos de ejemplo
        products = [
            ProductModel(
                name="Nike Air Zoom Pegasus",
                brand="Nike",
                category="Running",
                size="42",
                color="Negro",
                price=120.0,
                stock=15,
                description="Zapatillas de running ligeras y cómodas."
            ),
            ProductModel(
                name="Adidas Ultraboost 21",
                brand="Adidas",
                category="Running",
                size="41",
                color="Blanco",
                price=180.0,
                stock=10,
                description="Máxima amortiguación para largas distancias."
            ),
            ProductModel(
                name="Puma Smash V2",
                brand="Puma",
                category="Casual",
                size="43",
                color="Azul",
                price=65.0,
                stock=20,
                description="Clásico diseño casual para el día a día."
            ),
            ProductModel(
                name="Nike Air Force 1",
                brand="Nike",
                category="Casual",
                size="44",
                color="Blanco",
                price=110.0,
                stock=25,
                description="Ícono urbano con estilo retro."
            ),
            ProductModel(
                name="Adidas Stan Smith",
                brand="Adidas",
                category="Casual",
                size="42",
                color="Verde",
                price=90.0,
                stock=18,
                description="El clásico Stan Smith renovado."
            ),
            ProductModel(
                name="Puma Flyer Runner",
                brand="Puma",
                category="Running",
                size="40",
                color="Rojo",
                price=75.0,
                stock=12,
                description="Para quienes buscan velocidad y comodidad."
            ),
            ProductModel(
                name="Nike Classic Cortez",
                brand="Nike",
                category="Casual",
                size="41",
                color="Negro",
                price=85.0,
                stock=14,
                description="Un clásico de los 70 para tus looks diarios."
            ),
            ProductModel(
                name="Adidas Gazelle",
                brand="Adidas",
                category="Casual",
                size="43",
                color="Gris",
                price=95.0,
                stock=10,
                description="Estilo retro para todos los días."
            ),
            ProductModel(
                name="Puma Derby",
                brand="Puma",
                category="Formal",
                size="42",
                color="Marrón",
                price=130.0,
                stock=8,
                description="Elegancia y confort para ocasiones formales."
            ),
            ProductModel(
                name="Nike Air Max 90",
                brand="Nike",
                category="Running",
                size="44",
                color="Azul",
                price=200.0,
                stock=5,
                description="Estilo y tecnología Air para tus entrenamientos."
            ),
        ]

        session.add_all(products)
        session.commit()
        print("Datos iniciales cargados correctamente.")
    except Exception as e:
        session.rollback()
        print(f"Error cargando datos iniciales: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    print("Inicializando tablas de la base de datos...")
    init_db()
    print("Cargando datos iniciales de productos...")
    load_initial_data()
    print("¡Listo! Base de datos inicializada y datos cargados.")