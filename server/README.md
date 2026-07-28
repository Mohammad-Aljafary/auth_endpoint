# Auth Endpoint Server

This project is a FastAPI service that exposes Supabase-backed authentication endpoints and a small set of protected sample routes. It is designed to help you quickly stand up a simple auth API for sign-up, sign-in, sign-out, and user profile access.

## Environment Variables

Create a `.env` file in the server directory with the following values:

```env
SUPABASE_URL=https://<your-project-ref>.supabase.co
SUPABASE_ANON_KEY=<your-anon-or-publishable-key>
# Optional, but recommended for confirmed sign-ups:
SUPABASE_SERVICE_ROLE_KEY=<your-service-role-key>
```

Requirements:
- `SUPABASE_URL` is required.
- One of `SUPABASE_ANON_KEY`, `SUPABASE_PUBLISHABLE_KEY`, or `SUPABASE_KEY` is required for public client access.
- `SUPABASE_SERVICE_ROLE_KEY` is optional and enables admin-based user creation when available.

## Run the Server

From the project directory, start the API with:

```bash
uv run uvicorn main:app --reload
```

The app will be available at:
- http://127.0.0.1:8000
- http://127.0.0.1:8000/docs for the Swagger UI

## API Reference

| Method | Endpoint | Description | Auth required |
| --- | --- | --- | --- |
| GET | `/public/info` | Returns public information for anonymous users. | No |
| POST | `/auth/signup` | Creates a new user account through Supabase Auth. | No |
| POST | `/auth/login` | Authenticates a user and returns a JWT plus refresh token. | No |
| GET | `/protected/profile` | Returns sample protected profile information. | Yes |
| GET | `/protected/dashboard` | Returns sample protected dashboard information. | Yes |

For the protected routes, include an Authorization header in the request:

```http
Authorization: Bearer <access_token>
```

There is also a `POST /auth/logout` endpoint for sign-out, which should be called with a valid bearer token.
