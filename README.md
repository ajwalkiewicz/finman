# Finance Manager

A comprehensive finance management application for tracking cyclic transactions,
expenses, and money flow between accounts. Built with FastAPI backend, Vue 3
frontend, and Go proxy server, featuring multi-currency support and detailed analytics.

## ✨ Features

- **🔄 Transaction Management**: Track cyclic transactions with customizable day-of-month scheduling
- **💱 Multi-Currency Support**: Support for PLN, EUR, USD, and GTQ currencies with real-time exchange rates
- **⚡ High-Performance Proxy**: Go-based exchange rate service with Redis caching for optimal performance
- **🏦 Account Management**: Manage different types of accounts (bank, card, wallet, etc.) with flow visualization
- **📊 Expense Analytics**: Comprehensive expense tracking excluding transfers between accounts
- **📈 Money Flow Visualization**: Interactive charts showing money flow between different accounts
- **🔐 Secure Authentication**: JWT-based authentication with OAuth2 implementation
- **📱 Responsive Design**: Optimized for desktop and mobile devices
- **📤 Import/Export**: CSV import and export functionality for transactions
- **👥 User Management**: Role-based access with free, plus, and pro user types
- **🛡️ Security Features**: Rate limiting, password validation, and comprehensive security measures

## 🏗️ Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs with automatic documentation
- **SQLAlchemy**: SQL toolkit and ORM for database interactions
- **SQLite**: Lightweight database for storing transactions and user data
- **Python-JOSE**: JWT token authentication implementation
- **Passlib**: Secure password hashing with bcrypt
- **Uvicorn**: High-performance ASGI server
- **Pydantic**: Data validation and serialization

### Frontend
- **Vue 3**: Progressive JavaScript framework with Composition API
- **TypeScript**: Type-safe JavaScript for better development experience
- **Pinia**: Modern state management for Vue
- **Vue Router**: Client-side routing and navigation
- **Axios**: HTTP client for API communication
- **Tailwind CSS**: Utility-first CSS framework for styling

### Proxy Server
- **Go**: High-performance proxy service for exchange rates
- **Redis**: Caching layer for improved performance and reduced API calls
- **Fixer.io Integration**: Real-time currency exchange rate fetching

### Infrastructure
- **Docker**: Containerization for consistent deployment
- **Docker Compose**: Multi-container application orchestration
- **Nginx**: Reverse proxy and static file serving
- **Make**: Build automation and task management

## 🚀 Getting Started

### Prerequisites
- **Docker and Docker Compose** (recommended for easy setup)
- **OR** Python 3.10+, Node.js 16+, and Go 1.25+ for local development

### 🐳 Quick Start with Docker Compose (Recommended)

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd finman
   ```

2. **Configure environment** (optional):
   ```bash
   cp ./data/.env.example ./data/.env
   # Edit .env file with your configuration if needed
   ```

3. **Build and start services**:
   ```bash
   make build
   make start
   ```

4. **Access the application**:
   - 🌐 **Frontend**: http://localhost:3000
   - 🔧 **Backend API**: http://localhost:8010
   - 💱 **Exchange Rate Proxy**: http://localhost:8012
   - 📚 **API Documentation**: http://localhost:8010/docs (if enabled)

5. **Manage services**:
   ```bash
   make logs    # View logs
   make stop    # Stop services
   make restart # Restart services
   ```

### 🛠️ Available Make Commands

| Command        | Description                                |
|----------------|--------------------------------------------|
| `make build`   | Build Docker images                        |
| `make start`   | Start all services                         |
| `make stop`    | Stop all services                          |
| `make restart` | Restart services                           |
| `make logs`    | View service logs                          |
| `make status`  | Check service status                       |
| `make clean`   | Stop and remove all containers and volumes |

### 💻 Local Development Setup (Alternative)

#### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create and activate virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run development server**:
   ```bash
   python run.py
   ```

   🌐 API available at: http://localhost:8000

#### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start development server**:
   ```bash
   npm run dev
   ```

   🌐 Frontend available at: http://localhost:3000

#### Proxy Server Setup

1. **Navigate to proxy directory**
   ```bash
   cd proxy
   ```

2. **Install dependencies**
   - **Go** follow official instructions at https://go.dev/doc/install
   - **Redis**:
   ```bash
   sudo apt update
   sudo apt install redis-server
   sudo systemctl start redis-server
   ```

   > **WARNING**
   >
   > Remember about disabling Redis service when switching to docker setup
   >
   > ```bash
   > sudo systemctl stop redis-server
   > sudo systemctl disable redis-server
   > ```

3. **Start proxy server**
   ```bash
   go run ./cmd/api/main.go server
   ```

   🌐 Proxy available at: http://localhost:8012

> 📖 **For detailed proxy documentation**, see [proxy/README.md](./proxy/README.md)

### Fixer API and Secret Key

For proper and secure work, application requires secure key and Fixer API for
fetching current currencies rates.

> ⚠️ **WARNING**
>
> Store all environmental variables in `.env.` file to avoid accidentally
> publishing them

#### Secret Key

To generate secret key run following command:

```bash
openssl rand -hex 32
```

Use it's output as a key for `SECRET_KEY` environmental variable.

#### Fixer API

Project uses Fixer API to fetch real-time currency exchange rates.

1. Register in Fixer page: https://fixer.io/
2. Copy your API access key and store it in `FIXER_API_KEY` environmental variable.

> **IMPORTANT**
>
> If you do not want to use Fixer API, you can set default exchange rates in
> [proxy/rates.json](./proxy/rates.json)

## 🔐 Authentication & Security

### User Registration Control
User registration can be controlled using the `USER_REGISTRATION` environment variable:
- `USER_REGISTRATION=false` - Disable new user registration
- `USER_REGISTRATION=true` (default) - Allow new user registration
- When disabled, registration is hidden from frontend and API returns 403 error

### 👤 Username Requirements
- ✅ Minimum 6 characters
- ✅ English letters (a-z, A-Z), numbers (0-9), and underscores (_) only
- ✅ Pattern: `[a-zA-Z0-9_]{6,}`

### 🔒 Password Requirements
- ✅ Minimum 8 characters
- ✅ At least one uppercase letter (A-Z)
- ✅ At least one lowercase letter (a-z)
- ✅ At least one digit (0-9)
- ✅ At least one special character (!@#$%^&*()_+-=[]{}|;:,.<>?)
- ❌ Cannot be a common password
- ❌ Cannot contain more than 3 consecutive identical characters
- ❌ Cannot contain simple sequences (e.g., '1234', 'abcd')
- ❌ Cannot contain the username

### 🛡️ Security Features
- JWT-based authentication with OAuth2
- Password hashing with bcrypt
- Rate limiting on API endpoints
- CORS configuration for cross-origin requests
- Input validation with Pydantic schemas
- SQL injection protection via SQLAlchemy ORM

## 🔌 API Endpoints

### 🔐 Authentication & User Management
| Method | Endpoint                 | Description                            |
|--------|--------------------------|----------------------------------------|
| `GET`  | `/registration-status`   | Check if user registration is enabled  |
| `GET`  | `/password-requirements` | Get password requirements for frontend |
| `POST` | `/token`                 | Login and get access token             |
| `POST` | `/register`              | Register new user (if enabled)         |
| `GET`  | `/users/me`              | Get current user information           |
| `PUT`  | `/users/me/password`     | Change current user's password         |

### 💰 Transactions
| Method   | Endpoint                         | Description                             |
|----------|----------------------------------|-----------------------------------------|
| `GET`    | `/transactions/`                 | List all transactions (with pagination) |
| `POST`   | `/transactions/`                 | Create new transaction                  |
| `GET`    | `/transactions/{transaction_id}` | Get specific transaction                |
| `PUT`    | `/transactions/{transaction_id}` | Update transaction                      |
| `DELETE` | `/transactions/{transaction_id}` | Delete transaction                      |

### 🏦 Accounts
| Method   | Endpoint                 | Description            |
|----------|--------------------------|------------------------|
| `GET`    | `/accounts/`             | List all user accounts |
| `POST`   | `/accounts/`             | Create new account     |
| `PUT`    | `/accounts/{account_id}` | Update account         |
| `DELETE` | `/accounts/{account_id}` | Delete account         |

### 📊 Analytics
| Method | Endpoint              | Description                                 |
|--------|-----------------------|---------------------------------------------|
| `GET`  | `/analytics/expenses` | Get expense summary by currency             |
| `GET`  | `/analytics/accounts` | Get account flow analysis with transactions |

### 💳 Subscription Management
| Method | Endpoint               | Description                                 |
|--------|------------------------|---------------------------------------------|
| `GET`  | `/subscription/`       | Get current user's subscription information |
| `PUT`  | `/subscription/`       | Update user's subscription type             |
| `GET`  | `/subscription/limits` | Get all subscription types and their limits |

### Exchange Rate Proxy (Port 8012)
| Method | Endpoint               | Description                                 |
|--------|------------------------|---------------------------------------------|
| `GET`  | `/health`              | Check proxy service health and Redis connectivity |
| `GET`  | `/api/rates?base={currency}` | Get exchange rates with specified base currency (USD, EUR, PLN, GTQ) |

### API Documentation
- **Swagger UI**: http://localhost:8010/docs (disabled in production)
- **ReDoc**: http://localhost:8010/redoc (disabled in production)
- **OpenAPI Schema**: http://localhost:8010/openapi.json (disabled in production)

### 🛡️ Rate Limiting
- **Global Rate Limit**: 100 requests per minute per IP
- **Redis-based**: Distributed rate limiting using Redis

## 📊 Data Management

### 📤 Data Import

Application can import CSV data from the file. CSV must follow below format:

**CSV Format**:
| Column                | Description                     | Required |
|-----------------------|---------------------------------|----------|
| `title`               | Transaction title               | ✅       |
| `origin_account`      | Source account name             | ❌       |
| `destination_account` | Target account name             | ❌       |
| `amount`              | Transaction amount              | ✅       |
| `currency`            | Currency code (PLN/EUR/USD/GTQ) | ✅       |
| `day_of_month`        | Day of month (1-31)             | ✅       |
| `description`         | Additional details              | ❌       |

### 💡 Transaction Types
- **💸 Expenses**: Transactions without a destination account
- **💰 Income**: Transactions without an origin account
- **🔄 Transfers**: Transactions with both origin and destination accounts (not counted as expenses)

### 🌍 Supported Currencies
- **PLN** - Polish Złoty
- **EUR** - Euro
- **USD** - US Dollar
- **GTQ** - Guatemalan Quetzal

### 📈 Analytics Features
- Total expenses by currency (excluding transfers)
- Expense breakdown by category/title
- Money flow analysis between accounts
- Account balance visualization
- Real-time exchange rate conversion

## 👥 User Management

### User Types
- **🆓 Free**: Basic transaction tracking
- **➕ Plus**: Enhanced analytics and features
- **🏆 Pro**: Full feature access with advanced analytics

## 🔧 Development

### Backend Development
- Built with **FastAPI** for high-performance API development
- Automatic API documentation available at:
  - **Swagger UI**: http://localhost:8000/docs
  - **ReDoc**: http://localhost:8000/redoc
- SQLAlchemy ORM for database operations
- Pydantic for data validation and serialization

### Frontend Development
- **Vue 3** with Composition API for reactive components
- **TypeScript** for type safety and better DX
- **Pinia** for centralized state management
- **Vue Router** for client-side navigation
- **Tailwind CSS** for utility-first styling
- Responsive design optimized for mobile and desktop

### Code Quality
- Type checking with TypeScript
- Linting with ESLint
- Code formatting with Prettier
- API validation with Pydantic schemas

## 🚀 Roadmap

### ✅ Completed Features
- [x] OAuth2 authentication implementation
- [x] Easy VPS deployment with Docker
- [x] Backup mechanism
- [x] Analytics page improvements
- [x] Rate limiting implementation
- [x] CSV import/export functionality
- [x] User settings panel
- [x] Enhanced username validation
- [x] User subscription types (free/plus/pro)
- [x] Mobile-responsive design
- [x] Account color customization
- [x] Money flow graphs for individual accounts

### 🎯 Short-term Goals
- [ ] **Security Fixes** (Critical Priority)
  - [x] Fix environment variable configuration (SECRET_KEY loading)
  - [x] Disable API documentation in production environment
  - [ ] Implement input sanitization for XSS protection
  - [ ] Fix frontend container to run as non-root user
  - [ ] Implement token blacklisting on password change
  - [ ] Strengthen Content Security Policy headers
  - [ ] Fix user enumeration in registration responses
- [ ] Investigate if rate limiting works correctly behind nginx
      i.e. If it blocks right IP address, not all of them.
- [ ] Toast notifications system
- [ ] Admin panel development
- [ ] Enhanced backup mechanisms

### 🔮 Long-term Vision
- [ ] Exchange rate caching with invalidation periods
- [ ] Refactor frontend components for better reusability
- [ ] Migration from SQLAlchemy to SQLModel
- [ ] UV-based project management
- [ ] PostgreSQL database migration
- [ ] Interactive transaction visualizations
- [ ] Database encryption
- [ ] Email notification system
- [ ] GDPR compliance modal
- [ ] Cookie consent management
- [ ] Spectator mode with data blurring
- [ ] Create landing page for the app, with examples and explanations of
      how to use the app.

### 🎨 Nice-to-have Features
- [ ] Wider range if currencies
- [ ] Allow user to select which currencies to use
- [ ] Multi-language support
- [ ] Dark/light theme toggle
- [ ] Advanced filtering and search
- [ ] Transaction categorization
- [ ] Budget planning tools

## 📝 Contributing

We welcome contributions! Please feel free to submit issues, feature requests, or pull requests.

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Code Style
- Follow existing code conventions
- Add appropriate tests
- Update documentation as needed
- Ensure all tests pass

## 📄 License

Licensed under the GNU General Public License v3.0 — see [LICENSE](./LICENSE)
for details.

Copyright (c) 2025 Adam Walkiewicz

## 🤝 Support

If you encounter any issues or have questions:
- Check the [API documentation](http://localhost:8010/docs) when running locally
- Review existing issues in the repository
- Create a new issue with detailed information

---

**Made with ❤️ for better financial management**
