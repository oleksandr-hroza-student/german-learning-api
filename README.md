# German Learning API

A Flask REST API for a German-learning app focused on noun genders and flashcards.

The app uses Firebase Authentication for users, Firestore for user data, and a local SQLite database for German noun/gender lookup.

## Current Features

- Firebase Authentication with protected Flask routes
- User profiles stored in Firestore
- German noun lookup using SQLite
- Flashcard creation from submitted words
- Duplicate flashcard prevention
- View and delete flashcards
- Pytest unit/integration tests
- GitHub Actions CI

## Architecture

The backend is split into three main layers:

Route → Service → Repository

- Routes handle HTTP requests, authentication and validation
- Services handle application logic
- Repositories handle SQLite and Firestore access

User IDs are taken from verified Firebase tokens rather than request data.

## Tech Stack

- Python
- Flask
- Firebase Authentication
- Firestore
- SQLite
- Pytest
- GitHub Actions

Planned:
- spaCy
- OpenAI API
- Docker
- Public deployment

## Why SQLite?

Most noun genders can be looked up locally, so there is no need to send every word to an AI model.

This keeps the main lookup fast and cheap, while AI can later be used for ambiguous words and explanations.

## API

- `POST /api/me`
- `GET /api/me`
- `PATCH /api/me`
- `POST /api/nouns/process`
- `POST /api/flashcards`
- `GET /api/flashcards`
- `DELETE /api/flashcards/<card_id>`

## Testing

The project includes tests for:

- Routes
- Services
- Repositories
- Real integration cases

GitHub Actions automatically runs the main test suite on pushes and pull requests.

## Status

Currently under active development.

Next steps:
- Flashcard review/progress system
- Natural-text noun extraction with spaCy
- AI fallback/explanations
- Docker and deployment
