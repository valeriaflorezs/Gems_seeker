from core.nodo import Nodo

class ArbolBST:
    def __init__(self):
        self.raiz = None
    
    def insertar(self, nombre, poder, positionx, positiony):
        # Convertir poder a entero antes de insertar
        try:
            poder_int = int(poder)
        except (ValueError, TypeError):
            print(f"Error: El poder '{poder}' no es un número válido")
            return False
        
        nuevo_nodo = Nodo(nombre, poder_int, positionx, positiony)
        
        if self.raiz is None:
            self.raiz = nuevo_nodo
            return True
        
        return self._insertar(self.raiz, poder_int, nombre, positionx, positiony)
    
    def _insertar(self, nodo, poder, nombre, positionx, positiony):
        if poder < nodo.poder:
            if nodo.izquierdo is None:
                nodo.izquierdo = Nodo(nombre, poder, positionx, positiony)
                return True
            else:
                return self._insertar(nodo.izquierdo, poder, nombre, positionx, positiony)
        elif poder > nodo.poder:
            if nodo.derecho is None:
                nodo.derecho = Nodo(nombre, poder, positionx, positiony)
                return True
            else:
                return self._insertar(nodo.derecho, poder, nombre, positionx, positiony)
        else:
            # Poder duplicado
            return False
    
    def buscar(self, poder):
        # Convertir poder a entero antes de buscar
        try:
            poder_int = int(poder)
        except (ValueError, TypeError):
            return None
        
        return self._buscar(self.raiz, poder_int)
    
    def _buscar(self, nodo, poder):
        if nodo is None:
            return None
        if poder == nodo.poder:
            return nodo
        elif poder < nodo.poder:
            return self._buscar(nodo.izquierdo, poder)
        else:
            return self._buscar(nodo.derecho, poder)
    
    def eliminar(self, poder):
        # Convertir poder a entero antes de eliminar
        try:
            poder_int = int(poder)
        except (ValueError, TypeError):
            print(f"Error: El poder '{poder}' no es un número válido")
            return False
        
        self.raiz = self._eliminar(self.raiz, poder_int)
        return True
    
    def _eliminar(self, nodo, poder):
        if nodo is None:
            return None
        
        if poder < nodo.poder:
            nodo.izquierdo = self._eliminar(nodo.izquierdo, poder)
        elif poder > nodo.poder:
            nodo.derecho = self._eliminar(nodo.derecho, poder)
        else:
            # Caso 1: sin hijos
            if nodo.izquierdo is None and nodo.derecho is None:
                return None
            # Caso 2: un solo hijo
            elif nodo.izquierdo is None:
                return nodo.derecho
            elif nodo.derecho is None:
                return nodo.izquierdo
            # Caso 3: dos hijos
            else:
                sucesor = self._minimo(nodo.derecho)
                # Copiar datos del sucesor
                nodo.poder = sucesor.poder
                nodo.nombre = sucesor.nombre
                nodo.position = sucesor.position
                # Eliminar el sucesor
                nodo.derecho = self._eliminar(nodo.derecho, sucesor.poder)
        
        return nodo
    
    def _minimo(self, nodo):
        actual = nodo
        while actual.izquierdo is not None:
            actual = actual.izquierdo
        return actual
    
    def encontrar_minimo(self):
        if self.raiz is None:
            return None
        return self._minimo(self.raiz)
    
    def encontrar_maximo(self):
        if self.raiz is None:
            return None
        actual = self.raiz
        while actual.derecho is not None:
            actual = actual.derecho
        return actual
    
    def inorden(self):
        resultado = []
        self._inorden(self.raiz, resultado)
        return resultado
    
    def _inorden(self, nodo, resultado):
        if nodo:
            self._inorden(nodo.izquierdo, resultado)
            resultado.append(nodo)
            self._inorden(nodo.derecho, resultado)
    
    def preorden(self):
        resultado = []
        self._preorden(self.raiz, resultado)
        return resultado
    
    def _preorden(self, nodo, resultado):
        if nodo:
            resultado.append(nodo.nombre)
            self._preorden(nodo.izquierdo, resultado)
            self._preorden(nodo.derecho, resultado)
    
    def postorden(self):
        resultado = []
        self._postorden(self.raiz, resultado)
        return resultado
    
    def _postorden(self, nodo, resultado):
        if nodo:
            self._postorden(nodo.izquierdo, resultado)
            self._postorden(nodo.derecho, resultado)
            resultado.append(nodo.nombre)
    
    def encontrar_sucesor_predecesor(self, poder):
        nodo = self.buscar(poder)
        if nodo is None:
            return None, None
        
        # Sucesor
        sucesor = None
        if nodo.derecho is not None:
            sucesor = self._minimo(nodo.derecho)
        else:
            actual = self.raiz
            while actual is not None:
                if nodo.poder < actual.poder:
                    sucesor = actual
                    actual = actual.izquierdo
                elif nodo.poder > actual.poder:
                    actual = actual.derecha
                else:
                    break
        
        # Predecesor
        predecesor = None
        if nodo.izquierdo is not None:
            predecesor = self._maximo(nodo.izquierdo)
        else:
            actual = self.raiz
            while actual is not None:
                if nodo.poder > actual.poder:
                    predecesor = actual
                    actual = actual.derecho
                elif nodo.poder < actual.poder:
                    actual = actual.izquierdo
                else:
                    break
        
        return sucesor, predecesor
    
    def esta_vacio(self):
        return self.raiz is None
    
    def mostrar_inventario(self):
        gemas = self.inorden()
        if not gemas:
            print("Inventario vacío")
            return
        
        print("\n=== INVENTARIO DE GEMAS ===")
        for i, gema in enumerate(gemas, 1):
            print(f"{i}. {gema.nombre} - Poder: {gema.poder}")