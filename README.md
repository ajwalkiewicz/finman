# Finance Manager

A comprehensive finance management application for tracking cyclic transactions, expenses, and money flow between accounts. Built with FastAPI backend and Vue 3 frontend, featuring multi-currency support and detailed analytics.

## ✨ Features

- **🔄 Transaction Management**: Track cyclic transactions with customizable day-of-month scheduling
- **💱 Multi-Currency Support**: Support for PLN, EUR, USD, and GTQ currencies with real-time exchange rates
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

### Infrastructure
- **Docker**: Containerization for consistent deployment
- **Docker Compose**: Multi-container application orchestration
- **Nginx**: Reverse proxy and static file serving
- **Make**: Build automation and task management

## 🚀 Getting Started

### Prerequisites
- **Docker and Docker Compose** (recommended for easy setup)
- **OR** Python 3.8+ and Node.js 16+ for local development

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
   - 📚 **API Documentation**: http://localhost:8010/docs

5. **Manage services**:
   ```bash
   make logs    # View logs
   make stop    # Stop services
   make restart # Restart services
   ```

### 🛠️ Available Make Commands

| Command | Description |
|---------|-------------|
| `make build` | Build Docker images |
| `make start` | Start all services |
| `make stop` | Stop all services |
| `make restart` | Restart services |
| `make logs` | View service logs |
| `make status` | Check service status |
| `make clean` | Stop and remove all containers and volumes |

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

   🌐 API available at: `http://localhost:8000`

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

   🌐 Frontend available at: `http://localhost:3000`

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
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/registration-status` | Check if user registration is enabled |
| `GET` | `/password-requirements` | Get password requirements for frontend |
| `POST` | `/token` | Login and get access token |
| `POST` | `/register` | Register new user (if enabled) |
| `GET` | `/users/me` | Get current user information |
| `PUT` | `/users/me/password` | Change current user's password |

### 💰 Transactions
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/transactions/` | List all transactions (with pagination) |
| `POST` | `/transactions/` | Create new transaction |
| `GET` | `/transactions/{transaction_id}` | Get specific transaction |
| `PUT` | `/transactions/{transaction_id}` | Update transaction |
| `DELETE` | `/transactions/{transaction_id}` | Delete transaction |

### 🏦 Accounts
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/accounts/` | List all user accounts |
| `POST` | `/accounts/` | Create new account |
| `PUT` | `/accounts/{account_id}` | Update account |
| `DELETE` | `/accounts/{account_id}` | Delete account |

### 📊 Analytics
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/analytics/expenses` | Get expense summary by currency |
| `GET` | `/analytics/accounts` | Get account flow analysis with transactions |

### 💳 Subscription Management
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/subscription/` | Get current user's subscription information |
| `PUT` | `/subscription/` | Update user's subscription type |
| `GET` | `/subscription/limits` | Get all subscription types and their limits |

### 📚 API Documentation
- **Swagger UI**: `http://localhost:8010/docs` (disabled in production)
- **ReDoc**: `http://localhost:8010/redoc` (disabled in production)
- **OpenAPI Schema**: `http://localhost:8010/openapi.json` (disabled in production)

### 🛡️ Rate Limiting
- **Global Rate Limit**: 100 requests per minute per IP
- **Redis-based**: Distributed rate limiting using Redis

## 📊 Data Management

### 📤 Data Import
The application automatically imports data from `data.csv` on startup if no transactions exist. 

**CSV Format**:
| Column | Description | Required |
|--------|-------------|----------|
| `title` | Transaction title | ✅ |
| `origin_account` | Source account name | ❌ |
| `destination_account` | Target account name | ❌ |
| `amount` | Transaction amount | ✅ |
| `currency` | Currency code (PLN/EUR/USD/GTQ) | ✅ |
| `day_of_month` | Day of month (1-31) | ✅ |
| `description` | Additional details | ❌ |

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
  - **Swagger UI**: `http://localhost:8000/docs`
  - **ReDoc**: `http://localhost:8000/redoc`
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

### 🎯 Short-term Goals
- [ ] User management scripts (add/remove/update users)
- [ ] Toast notifications system
- [ ] Admin panel development
- [ ] Enhanced backup mechanisms

### 🔮 Long-term Vision
- [ ] Refactor frontend components for better reusability
- [ ] Migration from SQLAlchemy to SQLModel
- [ ] UV-based project management
- [ ] PostgreSQL database migration
- [ ] Money flow graphs for individual accounts
- [ ] Interactive transaction visualizations
- [ ] Database encryption
- [ ] Email notification system
- [ ] GDPR compliance modal
- [ ] Cookie consent management
- [ ] Spectator mode with data blurring

### 🎨 Nice-to-have Features
- [ ] Exchange rate caching with invalidation periods
- [ ] Advanced data visualization charts
- [ ] Multi-language support
- [ ] Dark/light theme toggle
- [ ] Advanced filtering and search
- [ ] Transaction categorization
- [ ] Budget planning tools
- [ ] Financial goal tracking

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

This project is currently unlicensed. Please contact the maintainers for licensing information.

## 🤝 Support

If you encounter any issues or have questions:
- Check the [API documentation](http://localhost:8010/docs) when running locally
- Review existing issues in the repository
- Create a new issue with detailed information

---

**Made with ❤️ for better financial management**
