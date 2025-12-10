# 💎 Gems Seeker: Videojuego Educativo con Árbol Binario de Búsqueda

## ℹ️ Resumen del Proyecto

Gems Seeker es un videojuego educativo y recreativo, diseñado para niños, cuyo objetivo principal es **estimular la lógica, la atención y la estrategia** mediante un entorno lúdico y amigable.

El núcleo de la jugabilidad y la complejidad técnica del proyecto reside en la implementación desde cero de un **Árbol Binario de Búsqueda (BST)** que actúa como el **inventario dinámico** del jugador, donde el poder de la gema es la clave de ordenamiento.

* **Género:** Aventura / Puzzle educativo
* **Público Objetivo:** Niños y niñas en edad escolar
* **Materia:** Estructura de Datos 2

## 🛠️ Stack Tecnológico

| Componente | Tecnología | Propósito |
| :--- | :--- | :--- |
| **Lenguaje Base** | Python | Lógica central del juego y manejo de datos. |
| **Motor de Juego** | Pygame | Interfaz gráfica 2D, manejo de sprites y eventos. |
| **Estructura Central** | **Árbol Binario de Búsqueda (BST)** | Gestiona el inventario de gemas (basado en el nivel de `poder`). |

## 💻 Integración de Estructuras de Datos (BST)

La jugabilidad está directamente ligada a las operaciones del BST, logrando unir la teoría y la práctica en una experiencia lúdica y formativa.

| Operación BST | Aplicación en el Juego |
| :--- | :--- |
| **Inserción** | Recolección de nuevas gemas. |
| **Búsqueda** | El **evento Trampa** y la apertura de **Cofres** requieren buscar la gema exacta por su nivel de poder. |
| **Eliminación (Sucesor/Predecesor)** | Mecánica de **Enemigo** (si no se tiene la gema solicitada, se elimina el nodo más cercano en poder). |
| **Mínimo / Máximo** | El **Portal de Salida** consume la gema de **mayor poder** (`encontrar_maximo()`). |
| **Recorridos** | Visualización del Inventario detallado (recorridos `Inorden`, `Preorden` y `Postorden`). |
| **Lógica Cercana** | Si no se tiene la gema exacta para un Cofre, se busca la gema **más cercana** en poder disponible en el inventario. |

## 🎮 Mecánicas de Juego

El juego desafía al usuario a aplicar la lógica de datos de forma intuitiva:

* **Cofres:** Requieren una gema con un poder específico (exacto o cercano) para ser abiertos.
* **Enemigos:** Al atrapar al jugador, solicitan una gema. Si no se tiene la gema exacta, el juego busca y elimina el nodo sucesor o predecesor en el árbol para poder continuar.
* **Portal Final:** Se requiere eliminar la gema más poderosa del inventario para cruzar y ganar la partida.

## 🚀 Ejecución Local

**Requisitos:** Asegúrate de tener Python 3.x y Pygame instalados.

1.  Clona el repositorio:
    ```bash
    git clone [https://github.com/tu-usuario/Gems_seeker.git](https://github.com/tu-usuario/Gems_seeker.git)
    ```
2.  Ejecuta el juego:
    ```bash
    python main.py
    ```

**Controles Principales:**

* `W`/`A`/`S`/`D` o flechas: Movimiento.
* `ESPACIO`: Ejecutar evento especial (Trampa, Gema Especial o Búsqueda).
* `I`, `P`, `O`: Mostrar el inventario usando los diferentes recorridos del BST.

## 👥 Autoras

* Katherin Barrera
* Nátaly Cárdenas
* **Valeria Florez**
* Laura Rivera
