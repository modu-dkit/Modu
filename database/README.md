# Database setup

This project uses MySQL via Docker Compose.

## 1) Copy the example environment files

From the project root:

```bash
cp .env.example .env
cp backend/.env.example backend/.env
```

Then edit the copied files with your local database credentials.

## 2) Root env file

`/Users/cherylkong/Desktop/Modu/.env`

Example:

```env
MYSQL_ROOT_PASSWORD=root
MYSQL_DATABASE=modu
MYSQL_USER=modu
MYSQL_PASSWORD=change_me
MYSQL_HOST=localhost
MYSQL_PORT=3306
```

This is used by Docker Compose for the MySQL container.

## 3) Backend env file

`/Users/cherylkong/Desktop/Modu/backend/.env`

Example:

```env
DATABASE_URL=mysql+pymysql://modu:change_me@localhost:3306/modu?charset=utf8mb4
```

This is used by Alembic and the backend app when connecting to MySQL.

## 4) Start MySQL

From the project root:

```bash
docker compose up -d mysql
```

Check it is running:

```bash
docker compose ps
```

## 5) Initialize or migrate the database

From the backend directory:

```bash
cd backend
source .venv/bin/activate
alembic upgrade head
```

## 6) Verify tables

```bash
mysql -h 127.0.0.1 -P 3306 -u modu -pmodu -D modu -e "SHOW TABLES;"
```

## Important

- Do not commit real `.env` files.
- Keep `.env` and `backend/.env` local only.
- The committed files are `.env.example` and `backend/.env.example` only.
