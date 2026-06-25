# 🍕 Pizza Cart - Proyecto Etapa 2

Este repositorio contiene la implementación completa del proyecto (Etapa 1 y Etapa 2), abarcando tanto el backend (API) como el frontend interactivo, además de un conjunto completo de pruebas automatizadas.

---

## 🏗️ Arquitectura Elegida

La arquitectura seleccionada para este proyecto es **SPA (Single Page Application)** con una separación clara entre el Cliente (Frontend) y el Servidor (Backend) a través de una **API REST**.

Esta arquitectura permite que el usuario interactúe con la aplicación de forma fluida y sin recargas de página, ya que el navegador solo descarga el HTML/CSS una vez y luego utiliza JavaScript para solicitar únicamente los datos (en formato JSON) que necesita actualizar.

A continuación, un diagrama que ilustra cómo se comunican las piezas de nuestro proyecto:

```mermaid
graph LR
    subgraph Cliente ["💻 Navegador Web (Frontend)"]
        UI["Interfaz de Usuario\n(HTML5 / CSS3)"]
        AppLogic["Lógica de Aplicación\n(app.js)"]
        FetchAPI["Capa de Acceso a Datos\n(Fetch API)"]
        
        UI <-->|Eventos y DOM| AppLogic
        AppLogic <-->|Llamadas asíncronas| FetchAPI
    end

    subgraph Servidor ["⚙️ Servidor (Backend)"]
        FlaskAPI["API REST\n(Python / Flask)"]
        DB[("Base de Datos\n(SQLite)")]
        
        FlaskAPI <-->|Consultas SQL| DB
    end

    FetchAPI <-->|Peticiones HTTP (JSON)| FlaskAPI
    
    classDef frontend fill:#d4f1f4,stroke:#05445E,stroke-width:2px,color:#000;
    classDef backend fill:#fdf6e3,stroke:#b58900,stroke-width:2px,color:#000;
    
    class UI,AppLogic,FetchAPI frontend;
    class FlaskAPI,DB backend;
```

---

## 🛠️ Tecnologías Utilizadas

El stack tecnológico se eligió buscando simplicidad, rendimiento y claridad conceptual:

### **Frontend (Cliente)**
* **HTML5:** Estructura semántica de la aplicación.
* **CSS3 (Vanilla):** Sistema de diseño a medida (sin frameworks externos), utilizando variables CSS (`:root`), flexbox, grid layout y animaciones suaves para una experiencia de usuario moderna y "premium".
* **JavaScript (Vanilla):** Lógica asíncrona usando `async/await` y la API `fetch` para comunicarse con el servidor sin recargar la página.

### **Backend (Servidor)**
* **Python:** Lenguaje principal de desarrollo.
* **Flask:** Micro-framework web utilizado para construir los endpoints de la API REST (`/api/products`, `/api/cart`).
* **SQLite:** Motor de base de datos relacional ligero e integrado. Ideal para este proyecto ya que no requiere instalación de servidores extra.

### **Testing Automatizado**
* **Selenium (con Python):** Para pruebas End-to-End (E2E) controlando el navegador mediante scripts tradicionales.
* **Cypress (con Node.js/JS):** Para pruebas E2E modernas, ejecutadas directamente en el mismo ciclo de vida del navegador, ofreciendo validaciones instantáneas ("Time Travel").

---

## 🚧 Dificultades Encontradas y Cómo se Resolvieron

A lo largo del desarrollo nos topamos con varios desafíos técnicos que fueron resueltos exitosamente:

1. **Problema de Mimetypes (Estilos CSS rotos en Windows):**
   * **Dificultad:** Al ejecutar Flask en entornos Windows, el navegador bloqueaba la carga de `styles.css` arrojando un error en consola. Esto ocurría porque Windows enviaba el archivo con un formato incorrecto (`text/plain` en lugar de `text/css`).
   * **Solución:** Se importó el módulo nativo `mimetypes` en `app.py` y se forzó explícitamente a Flask a reconocer la extensión `.css` y `.js` antes de arrancar el servidor web.

2. **Acumulación de Estado en Base de Datos (Tests E2E):**
   * **Dificultad:** Al ejecutar pruebas automatizadas, los asserts matemáticos (ej: comprobar que el total diera $8000) fallaban. Esto sucedía porque las pruebas compartían la misma base de datos real, y los productos de una prueba se quedaban guardados y sumaban al total de la siguiente prueba.
   * **Solución:** En lugar de hacer que cada test dependa de una base de datos vacía, reescribimos los tests en Cypress para que fueran **secuenciales**. Cada test ahora lee el estado en el que quedó el carrito del test anterior y acumula matemáticamente los valores, simulando el viaje completo de un usuario sin perder contexto.

3. **Interacciones más veloces que las animaciones UI:**
   * **Dificultad:** En Selenium, el robot intentaba hacer clic en el botón "Eliminar" del carrito inmediatamente después de presionar "Carrito". Sin embargo, el carrito tiene una animación CSS que tarda 0.3 segundos en deslizarse por la pantalla, provocando el error `Element Not Interactable`.
   * **Solución:** Se implementaron "esperas explícitas" (`WebDriverWait` en Selenium) para forzar al script a esperar a que la animación terminara y el botón estuviera físicamente presente y clickeable en pantalla.
