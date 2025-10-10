class ProductNotFoundError(Exception):
    """
    Se lanza cuando se busca un producto que no existe.
    """
    def __init__(self, product_id: int = None):
        if product_id is not None:
            self.message = f"Producto con ID {product_id} no encontrado"
        else:
            self.message = "Producto no encontrado"
        super().__init__(self.message)

class InvalidProductDataError(Exception):
    """
    Se lanza cuando los datos de un producto son inválidos.
    """
    def __init__(self, message: str = "Datos de producto inválidos"):
        self.message = message
        super().__init__(self.message)

class ChatServiceError(Exception):
    """
    Se lanza cuando hay un error en el servicio de chat.
    """
    def __init__(self, message: str = "Error en el servicio de chat"):
        self.message = message
        super().__init__(self.message)