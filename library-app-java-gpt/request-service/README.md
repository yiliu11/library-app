# Book Request Service

## Overview
Microservice to allow staff to request books and librarians to approve/reject them.

## Configuration
- Configure DB and JWT secret in `application.yml` or provide env vars.
- JWT secret must match the Authentication Service secret.

## Endpoints
- `POST /api/requests` — create request (STAFF only)
  - Body: `{ "title": "...", "author": "...", "reason": "..." }`
- `GET /api/requests/mine` — list own requests (authenticated)
- `GET /api/requests` — list all requests (LIBRARIAN only) with optional `?status=PENDING`
- `GET /api/requests/{id}` — get request by id (librarian or owner)
- `PUT /api/requests/{id}/approve` — approve request (LIBRARIAN only) body `{ "comments": "..." }`
- `PUT /api/requests/{id}/reject` — reject request (LIBRARIAN only) body `{ "comments": "..." }`

## Database
- PostgreSQL recommended.
- schema.sql in resources provides table creation.

## Notes
- JWT must contain `jti` (user id) and `role` claim. The filter builds an Authentication principal that controllers use.
- Validation is performed via `@Valid`. Errors return consistent JSON via GlobalExceptionHandler.
