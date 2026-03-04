# User Management Service

## Overview
Service for managing user profiles. Librarians may create, update, delete users. It forwards credential creation to the Authentication Service.

## Configuration
- DB settings and JWT secret in `application.yml`. Use environment variables in production.
- `app.auth.base-url` should point to the Authentication Service (e.g., http://localhost:8080).

## Endpoints
- `GET /api/users` — list users (LIBRARIAN)
- `GET /api/users/{id}` — get user (LIBRARIAN or self)
- `POST /api/users` — create user (LIBRARIAN)
  - Body: `{ "username", "email", "fullName", "role", "initialPassword" }`
- `PUT /api/users/{id}` — update user (LIBRARIAN or self)
- `DELETE /api/users/{id}` — delete user (LIBRARIAN)

## Notes
- JWTs issued by Authentication Service must include `jti` (user id) and `role` claim.
- All endpoints require Authorization: `Bearer <token>`.
- Password handling: the service delegates creation of credentials to the Authentication Service via `POST /api/auth/register`.
