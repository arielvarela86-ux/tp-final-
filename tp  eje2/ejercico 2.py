import json


class StockInvalidoError(Exception):   
    pass



class DispositivoEcológico:
    
     def __init__(self, nombre: str, precio: float, stock: int):
        self.nombre = nombre
        self.precio = precio
        self._stock = 0  
        self.stock = stock  

     @property
     def stock(self) -> int:
        
        return self._stock

     @stock.setter
     def stock(self, valor: int):
        if not isinstance(valor, int) or valor < 0:
            raise StockInvalidoError(f"Stock inválido detectado ({valor}). El stock no puede ser menor a 0.")
        self._stock = valor

     def obtener_ficha_tecnica(self) -> str:
        
        return f"Dispositivo: {self.nombre} | Precio: ${self.precio:.2f} | Stock: {self._stock} unidades"

     def a_diccionario(self) -> dict:
         return {
            "tipo": "DispositivoGenerico",
            "nombre": self.nombre,
            "precio": self.precio,
            "stock": self._stock
        }


class PanelSolar(DispositivoEcológico):
    
    def __init__(self, nombre: str, precio: float, stock: int, potencia_w: float, eficiencia: float):
        super().__init__(nombre, precio, stock)
        self.potencia_w = potencia_w
        self.eficiencia = eficiencia

    
    def obtener_ficha_tecnica(self) -> str:
        base_info = super().obtener_ficha_tecnica()
        return f"[Panel Solar] {base_info} | Potencia: {self.potencia_w}W | Eficiencia: {self.eficiencia * 100:.1f}%"

    def a_diccionario(self) -> dict:
        d = super().a_diccionario()
        d["tipo"] = "PanelSolar"
        d["potencia_w"] = self.potencia_w
        d["eficiencia"] = self.eficiencia
        return d



class GestorInventario:
    

    @staticmethod
    def guardar_catalogo_json(lista_dispositivos, ruta_archivo):
        
        try:
            
            datos_serializables = [disp.a_diccionario() for disp in lista_dispositivos]
            
            with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
                json.dump(datos_serializables, archivo, indent=4, ensure_ascii=False)
                
            print(f"  Éxito: Catálogo exportado correctamente en '{ruta_archivo}'.")
        except IOError as e:
            print(f"  Error de E/S al intentar guardar el archivo: {e}")



if __name__ == "__main__":
    print("=" * 70)
    print("  SISTEMA DE GESTIÓN DE INVENTARIO - ECOTECH SOLUTIONS")
    print("=" * 70)

    
    print("\n--- 1. Prueba de Validación de Negocio (Excepción) ---")
    try:
        print("Intentando instanciar un Panel Solar con stock negativo (-10)...")
        PanelSolar("SolarMaster 300", 299.99, -10, 350, 0.20)
    except StockInvalidoError as e:
        print(f" [Excepción Capturada Correctamente]: {e}")

    
    print("\n--- 2. Creación de Productos Válidos y Fichas Técnicas (Polimorfismo) ---")
    try:
        panel_1 = PanelSolar("EcoPanel Max", 349.50, 25, 400, 0.22)
        panel_2 = PanelSolar("SolarLite Pro", 220.00, 40, 300, 0.19)
        disp_generico = DispositivoEcológico("Kit Medidor de Energía", 89.99, 15)

        catalogo_productos = [panel_1, panel_2, disp_generico]

        
        for producto in catalogo_productos:
            print(f"• {producto.obtener_ficha_tecnica()}")

    except StockInvalidoError as e:
        print(f"Error inesperado al crear productos: {e}")

    
    print("\n--- 3. Persistencia del Catálogo en Disco ---")
    archivo_destino = "catalogo_ecotech.json"
    GestorInventario.guardar_catalogo_json(catalogo_productos, archivo_destino)
    
    print("=" * 70)