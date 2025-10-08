# Auth design

- OAuth2 password grant via FastAPI `OAuth2PasswordBearer`.
- JWT (HS256) with configurable secret and 24h expiry.
- Simple SQLite user store for demo; migrate to real IdP or Postgres in production.
- Protected routes use dependency injection `get_current_user`.
