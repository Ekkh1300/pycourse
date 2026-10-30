# Project 2 — Book API

A simple REST API for managing a book collection using FastAPI.

## Requirements:
1. Build a FastAPI application with CRUD endpoints for books
2. Each book has: id, title, author, year, pages (optional)
3. Use Pydantic models for data validation
4. Store books in memory (Python list)
5. Auto-increment IDs

## API Endpoints:
- `GET /books` - Return list of all books (status 200)
- `GET /books/{id}` - Return single book by id (status 200, or 404 if not found)
- `POST /books` - Create a new book (status 201, return created book)
- `PUT /books/{id}` - Update book by id (status 200, or 404 if not found)
- `DELETE /books/{id}` - Delete book by id (status 204)
- `GET /books/search?title=...&author=...&sort=year` - Search books

## Example Usage:
```bash
# Install dependencies
python -m venv .venv
.venv\Scripts\activate
pip install fastapi uvicorn pydantic

# Run the server
uvicorn main:app --reload

# Visit the API docs:
# Open http://127.0.0.1:8000/docs in your browser

# Test the endpoints:
curl http://127.0.0.1:8000/books
curl -X POST http://127.0.0.1:8000/books \
  -H "Content-Type: application/json" \
  -d '{"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "year": 1925}'
```

## Expected Output (GET /books):
```json
[
  {"id": 1, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "year": 1924}
]
```