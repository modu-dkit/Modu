# Backend setup

## Prerequisities
Install the backend and development dependencies from `backend/`:

```
python -m pip install -r requirements-dev.txt
```

Start the API from `backend/` with:

```
python -m uvicorn app.main:app --reload
```

The interactive API documentation is available at
`http://127.0.0.1:8000/docs`

### Google Sign-In (current backend features)

Google Sign-In is currently implemented in the FastAPI backend only. The
frontend directory does not yet contain an Expo application or a Google
Sign-In button.

The current flow is:

1. A future frontend obtains a Google Identity Services ID token.
2. It sends the token to `POST /auth/google`.
3. The backend verifies the token with Google
4. The backend creates a local user in the `users` table if one does not exist.
5. The backend returns a Modu JWT access token valid for 60 minutes by default.
6. The frontend sends that token as `Authorization: Bearer <token>` to private routes.

Implemented routes:

```text
POST /auth/google   Verify Google ID token and create/find a Modu user
GET  /private       Example protected route
```

Configure the backend by copying `backend/.env.example` to `backend/.env`,
then set a real Google OAuth client ID and a long random JWT secret:

```env
GOOGLE_CLIENT_ID=your-google-web-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-google-client-secret
JWT_SECRET_KEY=replace-with-a-long-random-secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

The Google client secret is not required for this current ID-token flow. Do
not commit real credentials or local `.env` files.

Future work:

Implement access token + refresh token so user session persists
