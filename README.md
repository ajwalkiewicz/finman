# Finance Manager

A comprehensive finance management application for tracking cyclic transactions, expenses, and money flow between accounts.

## Features

- **Transaction Management**: Track cyclic transactions with customizable day-of-month scheduling
- **Multi-Currency Support**: Support for PLN, EUR, USD, and GTQ currencies
- **Account Management**: Manage different types of accounts (bank, card, wallet, etc.)
- **Expense Analytics**: View total expenses excluding transfers between accounts
- **Money Flow Visualization**: See money flow between different accounts
- **User Authentication**: Basic authentication system
- **Responsive Design**: Works on desktop and mobile devices

## Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **SQLite**: Lightweight database for storing transactions
- **Python-JOSE**: JWT token authentication
- **Passlib**: Password hashing
- **Uvicorn**: ASGI server

### Frontend
- **Vue 3**: Progressive JavaScript framework
- **TypeScript**: Type-safe JavaScript
- **Pinia**: State management
- **Vue Router**: Client-side routing
- **Axios**: HTTP client
- **Tailwind CSS**: Utility-first CSS framework

## Project Structure

```
/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI application
│   │   ├── database.py      # Database models and connection
│   │   ├── schemas.py       # Pydantic schemas
│   │   ├── crud.py          # Database operations
│   │   ├── auth.py          # Authentication utilities
│   │   └── utils.py         # Utility functions and CSV import
│   ├── requirements.txt     # Python dependencies
│   └── run.py              # Application runner
├── frontend/
│   ├── src/
│   │   ├── components/      # Vue components
│   │   ├── views/          # Page components
│   │   ├── stores/         # Pinia stores
│   │   ├── services/       # API services
│   │   ├── types/          # TypeScript type definitions
│   │   └── router/         # Vue Router configuration
│   ├── package.json        # Node.js dependencies
│   └── vite.config.ts      # Vite configuration
└── data.csv               # Initial data for import
```

## Getting Started

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the development server:
   ```bash
   python run.py
   ```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run serve
   ```

The frontend will be available at `http://localhost:3000`

## Default Credentials

The application creates a default admin user:
- **Username**: admin
- **Password**: admin123

## API Endpoints

### Authentication
- `POST /token` - Login and get access token
- `POST /register` - Register new user
- `GET /users/me` - Get current user info

### Transactions
- `GET /transactions/` - List all transactions
- `POST /transactions/` - Create new transaction
- `GET /transactions/{id}` - Get specific transaction
- `PUT /transactions/{id}` - Update transaction
- `DELETE /transactions/{id}` - Delete transaction

### Accounts
- `GET /accounts/` - List all accounts
- `POST /accounts/` - Create new account

### Analytics
- `GET /analytics/expenses` - Get expense summary by currency
- `GET /analytics/accounts` - Get account flow analysis

## Data Import

The application automatically imports data from `data.csv` on startup if no transactions exist. The CSV should have the following columns:
- Title
- Origin (account name or empty)
- Destination (account name or empty)
- Amount (with currency, e.g., "100 PLN")
- Day of Month (1-31)
- Description

## Features Overview

### Transaction Types
- **Expenses**: Transactions without a destination account
- **Income**: Transactions without an origin account
- **Transfers**: Transactions with both origin and destination accounts (not counted as expenses)

### Currency Support
- PLN (Polish Złoty)
- EUR (Euro)
- USD (US Dollar)
- GTQ (Guatemalan Quetzal)

### Analytics
- Total expenses by currency (excluding transfers)
- Expense breakdown by category/title
- Money flow analysis between accounts
- Account balance visualization

## Development

### Backend Development
The backend uses FastAPI with automatic API documentation available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Frontend Development
The frontend is built with Vue 3 and TypeScript, using:
- Composition API for reactive state management
- Pinia for global state management
- Vue Router for navigation
- Tailwind CSS for styling

## Security

- JWT-based authentication
- Password hashing with bcrypt
- CORS configuration for cross-origin requests
- Input validation with Pydantic schemas

## TODO:

Short term goals
1. Ensure security of an application
   1. Disable creating new accounts
   2. Use OAuth2 DONE
2. Create an easy way to publish the app on VPS
3. Create a backup mechanism
4. Fix analytics page
5. Script to add/remove/update users

Long term
1. Repay technological debt
2. Show money flow graph for each account
3. Import transactions from CSV
4. Export transactions to CSV
5. Add graph with money flow and transactions
6. Use better database than sqlite
7. Add user settings panel
8. Add admin panel
9. Add GDPR modal
10. Add Cookie modal
11. Add support for mail
12. Add encryption for database

Optimization
1. Refactor frontend to use more components and less code duplication
2. Move from SQLAlchemy to SQLModel
3. Use UV for project management
4. 

5. Add timestamp and invalidation period for exchange rate from proxy server
   So, frontend won;t need to ask it for data every time, only when the 
   validation period expires

Nice to have:
1. Set different colors for accounts labels
2. Spectator mode where the numbers and names of transactions and accounts are blurred

## License

TODO: add license
