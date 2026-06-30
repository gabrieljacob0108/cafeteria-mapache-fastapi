# 🦝 Sistema Mapache - Backend Modular en Python

Sistema backend desarrollado en Python que simula un ecosistema comercial completo, incluyendo ventas, inventario, recompensas y múltiples módulos de negocio.

---

## 🚀 Tecnologías utilizadas

- Python 🐍  
- FastAPI ⚡  
- Flask 🌐  
- MongoDB 🍃  
- Git & GitHub  

---

## 🧩 Descripción del proyecto

Este proyecto representa el desarrollo de un backend modular enfocado en simular procesos reales de negocio como:

- gestión de ventas  
- manejo de inventario  
- sistemas de recompensas  
- automatización de compras  

El objetivo es construir múltiples sistemas conectados que reflejen escenarios reales del mundo comercial.

---

## 📦 Módulos del sistema

### ☕ Cafetería Mapache (FastAPI)
- API REST para gestión de productos y ventas  
- flujo de compra simulado  
- manejo de pedidos  

---

### 🛒 Supermercado
- lógica de compra  
- validación de stock  
- simulación de carrito  

---

### 📦 Almacén
- gestión de inventario  
- control de existencias  
- actualización de productos  

---

### 🎁 Sistema de Tokens
- sistema de recompensas por compra  
- acumulación y uso de puntos  

---

### 🤖 Máquina Expendedora
- simulación de compra automática  
- toma de decisiones del usuario  

---

### 🍰 Pastelería (Flask)
- sistema de ventas sencillo  
- estructura independiente  

---

## 🗄️ Base de datos

Se utiliza MongoDB para almacenar datos como:

- usuarios  
- productos  
- historial de compras  

Además, se están incorporando conocimientos en SQL (PostgreSQL) para ampliar el sistema.

---

## ▶️ Cómo ejecutar el proyecto

### 📌 Requisitos

- Python 3.10 o superior  
- Cuenta en MongoDB Atlas  
- Archivo `.env` configurado con la conexión a la base de datos  

---

### ⚙️ Instalación

Instalar dependencias:

```bash
pip install fastapi uvicorn flask pymongo python-dotenv
