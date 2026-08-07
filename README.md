# 🐾 Repositorio Backend: Ecosistema Mapache (Python Lab)

[![Python](https://shields.io)](https://python.org)
[![FastAPI](https://shields.io)](https://tiangolo.com)
[![Litestar](https://shields.io)](https://litestar.dev)
[![Flask](https://shields.io)](https://palletsprojects.com)
[![PostgreSQL](https://shields.io)](https://postgresql.org)
[![MongoDB](https://shields.io)](https://mongodb.com)

Repositorio centralizado que recopila laboratorios de desarrollo backend en **Python**. Diseñado para explorar arquitecturas REST asíncronas, modelado de bases de datos relacionales y NoSQL, integración de lógica de negocio orientada a objetos (POO) y prácticas de desarrollo seguro.

---

## 🚀 Proyectos Integrados

### 🍦 1. Heladería Gato Sentado (API Asíncrona)
* **Tecnologías:** `Litestar` | `SQLAlchemy (Async)` | `PostgreSQL` | `Pydantic` | `CORS`
* **Descripción:** API REST asíncrona para la gestión de pedidos personalizados de helados, control de catálogo (recipientes, sabores, toppings) y actualización en tiempo real del saldo histórico en caja mediante relaciones relacionales (`1:N`).

### ☕ 2. Cafetería Mapache FastAPI
* **Tecnologías:** `FastAPI` | `Python` | `Uvicorn`
* **Descripción:** Implementación de servicios web y endpoints para el flujo de pedidos, procesamiento de solicitudes HTTP y lógica de negocio para atención en cafetería.

### 📦 3. Sistema de Almacén / Tiendas Gabriel
* **Tecnologías:** `Python` | `Manejo de Archivos` | `Estructuras de Datos`
* **Descripción:** Módulo backend enfocado en la automatización de inventarios, reabastecimiento y control de stock centralizado.

### 🤖 4. Máquina Expendedora
* **Tecnologías:** `Python` | `Programación Orientada a Objetos (POO)`
* **Descripción:** Simulación de lógica comercial mediante clases, encapsulamiento y manejo de estados para control de saldo, dispensado de productos y devolución exacta de cambio.

### 🍰 5. Pastelería Backend
* **Tecnologías:** `Flask` | `Python`
* **Descripción:** Aplicación web backend orientada al control de stock de insumos, gestión de recetas/productos y registro comercial de ventas.

### 🛒 6. Gestor de Supermercado
* **Tecnologías:** `MongoDB` | `PyMongo` | `NoSQL`
* **Descripción:** Sistema de administración dinámica de inventarios en base de datos no relacional, permitiendo esquemas flexibles para catálogo de productos no estructurados.

### 🔑 7. Sistema de Tokens Mapache
* **Tecnologías:** `Python` | `Security` | `Bcrypt`
* **Descripción:** Módulo de seguridad encargado de la generación, hashing, firma y validación de tokens de acceso y puntos de fidelización.

---

## 🧩 Arquitectura e Integración de Módulos

Este ecosistema simula un flujo comercial interconectado mediante lógica de negocio aplicada:
* **Gestión de Inventarios:** El Almacén actúa como nodo central de suministro. Cuando el stock del Supermercado o la Máquina Expendedora cae por debajo del umbral mínimo, notifican al Almacén para procesar las existencias.
* **Fidelización y Puntos:** La Cafetería, Pastelería y la Heladería integran sus transacciones con el Sistema de Tokens. Cada compra procesada genera puntos automáticamente según el volumen de venta y el historial del usuario.

---

## 🛠️ Stack Tecnológico

* **Lenguaje Principal:** Python 3.10+
* **Frameworks Backend:** FastAPI, Litestar, Flask
* **Bases de Datos:** PostgreSQL (SQLAlchemy Async / asyncpg), MongoDB (NoSQL)
* **Validación & Seguridad:** Pydantic, Bcrypt, python-dotenv, CORSConfig
* **Control de Versiones:** Git / GitHub

---

## 📦 Configuración y Ejecución Local

### 1. Clonar el repositorio
```bash
git clone https://github.com
cd cafeteria-mapache-fastapi
```

### 2. Crear y activar el entorno virtual
```bash
python -m venv venv

# En Linux/macOS:
source venv/bin/activate

# En Windows:
venv\Scripts\activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Variables de Entorno
Crea un archivo `.env` en la raíz del proyecto definiendo las credenciales de conexión:
```env
DATABASE_URL=postgresql+asyncpg://postgres:tu_password@localhost:5432/gato_sentado
MONGODB_PWD=tu_password_de_mongo
```

---

## 👤 Autor

**Gabriel Jacob Rojas Peralta**  
*Desarrollador Backend Junior | Python & FastAPI*  

* 📧 **Email:** [gabrieljacob4468@gmail.com](mailto:gabrieljacob4468@gmail.com)
* 💼 **LinkedIn:** [Gabriel Jacob Rojas Peralta](https://www.linkedin.com/in/gabriel-jacob-rojas-peralta-2278703a9/)
* 🐙 **GitHub:** [@gabrieljacob0108](https://github.com/gabrieljacob0108/cafeteria-mapache-fastapi)

