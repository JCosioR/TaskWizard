# Implementacion multitenancy
1. Agregar tenant_id column a todos los modelos tenant-specific de SQLAlchemy
2. Usar inyección de dependencia de FastAPI para extraer el tenant_id de los request headers (X-Tenant-ID), subdominios o JWT
2. Implementar filtros en todas las queries: db.query(Model).filter(Model.tenant_id == current_tenant)
3. Se puede usar PostgreSQL Row-Level Security para restringir automáticamente el acceso basado en la sesión activa del tenant ID
- Schema por tenant:
4. Usualmente usado con PostgreSQL, donde cada tenant tiene su propio schema aislado dentro de una base de datos.
5. Implementar un middleware o dependencia que identiique el tenant e instruya a SQLAlchemy a cambiar la ruta de búsqueda o remapear dinámicamente el nombre del schema para esa request.
- Base de datos separada:
4. Cada tenant tiene una conexión URL a base de datos completamente separada.
5. Se pueden manejar vía Pydantic Settings para validar las variablees de entorno por diferentes endpoints de tenants.

1. Crear tabla Tenants
La tabla tenants debe llevar __tablename__, id y name
2. Relacionar Tenants con UserDB
Se agrega una columna tenant_id
3. Actualizar queries
Todas las queries deben filtrar por tenant_id