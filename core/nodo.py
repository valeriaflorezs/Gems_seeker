class Nodo:
    def __init__(self, nombre, poder, positionx, positiony):
        # Asegurar que poder sea entero
        try:
            self.poder = int(poder)
        except (ValueError, TypeError):
            raise ValueError(f"El poder debe ser un número. Se recibió: {poder}")
        
        self.nombre = nombre
        self.position = (positionx, positiony)
        self.derecho = None
        self.izquierdo = None
    
    def __str__(self):
        return f"Nombre: {self.nombre}, Poder: {self.poder}, Posicion: {self.position}"