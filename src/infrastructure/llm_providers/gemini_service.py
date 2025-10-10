import os
import google.generativeai as genai

class GeminiService:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY no está definida en variables de entorno.")
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    def format_products_info(self, products):
        """
        Convierte una lista de productos a un string legible.
        Formato: "- Nombre | Marca | Precio | Stock"
        """
        lines = []
        for p in products:
            lines.append(f"- {p.name} | {p.brand} | ${p.price} | Stock: {p.stock}")
        return "\n".join(lines) if lines else "No hay productos disponibles."

    async def generate_response(self, user_message, products, context):
        """
        user_message: str
        products: lista de entidades Product (con atributos name, brand, price, stock)
        context: lista de mensajes previos [{'role': 'user'/'assistant', 'message': str}]
        """
        productos_txt = self.format_products_info(products)
        
        historial = ""
        for entry in context:
            rol = "Usuario" if entry["role"] == "user" else "Asistente"
            historial += f"{rol}: {entry['message']}\n"

        prompt = f"""Eres un asistente virtual experto en ventas de zapatos para un e-commerce.
Tu objetivo es ayudar a los clientes a encontrar los zapatos perfectos.

PRODUCTOS DISPONIBLES:
{productos_txt}

INSTRUCCIONES:
- Sé amigable y profesional
- Usa el contexto de la conversación anterior
- Recomienda productos específicos cuando sea apropiado
- Menciona precios, tallas y disponibilidad
- Si no tienes información, sé honesto

{historial}Usuario: {user_message}

Asistente:"""

        try:
            response = await self.model.generate_content_async(prompt)
            return response.text.strip() if hasattr(response, "text") else str(response)
        except Exception as e:
            return "Lo siento, hubo un problema al contactar con el asistente de IA. Intenta nuevamente más tarde."