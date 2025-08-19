# FastAPI Backend with Domain Driven Design (DDD)

A modern Python backend built with FastAPI following Domain Driven Design principles, featuring clean architecture and separation of concerns.

## 🏗️ Architecture

This project follows **Domain Driven Design (DDD)** with a clean, layered architecture:

### **Layers**

1. **Domain Layer** - Business entities, value objects, domain services
2. **Application Layer** - Use cases, application services, DTOs
3. **Infrastructure Layer** - Database, external services, repositories
4. **Interface Layer** - API controllers, schemas, web interfaces

### **Project Structure**

```
app/
├── domains/                    # Domain Layer
│   ├── users/                 # Users Domain
│   │   ├── domain.py          # Entities, Value Objects, Domain Logic
│   │   ├── repository.py      # Repository Interface
│   │   └── services.py        # Domain Services
│   └── wines/                 # Wines Domain
│       ├── domain.py          # Wine Entity
│       ├── repository.py      # Repository Interface
│       └── services.py        # Domain Services
│
├── application/               # Application Layer
│   ├── users/
│   │   ├── dto.py            # Data Transfer Objects
│   │   └── use_cases.py      # Use Cases
│   └── wines/
│       ├── dto.py            # Wine DTOs
│       └── use_cases.py      # Wine Use Cases
│
├── infrastructure/            # Infrastructure Layer
│   ├── database/
│   │   ├── connection.py     # Database Connection
│   │   └── models.py         # SQLAlchemy Models
│   └── repositories/
│       ├── user_repository.py # Repository Implementation
│       └── wine_repository.py # Wine Repository Implementation
│
├── interfaces/               # Interface Layer
│   └── api/
│       ├── schemas.py        # API Schemas
│       ├── router.py         # Main API Router
│       └── controllers/      # API Controllers
│
└── core/                    # Core Utilities
    └── container.py         # Dependency Injection
```

## 🚀 Features

- **Domain Driven Design** - Clean separation of business logic
- **FastAPI** - Modern, fast web framework
- **SQLAlchemy ORM** - Powerful database operations
- **SQLite** - Lightweight, file-based database
- **Alembic** - Database migration management
- **Pydantic** - Data validation and serialization
- **Dependency Injection** - Clean architecture
- **Auto-generated API Documentation** - Interactive docs at `/docs`

## 🎯 DDD Benefits

- **Business Logic Isolation** - Domain logic is separate from technical concerns
- **Testability** - Easy to unit test domain entities and services
- **Maintainability** - Changes in one layer don't affect others
- **Scalability** - Easy to add new domains and features
- **Domain Expertise** - Code reflects business understanding

## 📋 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Application

```bash
python3 run.py
```

### 3. Access the API

- **API Base URL**: http://localhost:8000
- **Interactive Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 🔧 API Endpoints

### Users (DDD Implementation)

- `POST /api/v1/users/` - Create a new user
- `GET /api/v1/users/` - Get all users (with pagination)
- `GET /api/v1/users/{user_id}` - Get a specific user
- `PUT /api/v1/users/{user_id}` - Update a user
- `DELETE /api/v1/users/{user_id}` - Delete a user

### Wines (DDD Implementation)

- `POST /api/v1/wines/` - Create a new wine
- `GET /api/v1/wines/` - Get all wines (with pagination)
- `GET /api/v1/wines/{wine_id}` - Get a specific wine
- `PUT /api/v1/wines/{wine_id}` - Update a wine
- `DELETE /api/v1/wines/{wine_id}` - Delete a wine

## 🧪 Testing

### Manual Testing

```bash
# Create a user
curl -X POST "http://localhost:8000/api/v1/users/" \
     -H "Content-Type: application/json" \
     -d '{
       "email": "user@example.com",
       "username": "testuser",
       "password": "securepassword123",
       "full_name": "Test User"
     }'

# Create a wine
curl -X POST "http://localhost:8000/api/v1/wines/" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Château Margaux",
       "year": 2015,
       "grape": "Cabernet Sauvignon",
       "country": "France",
       "region": "Bordeaux",
       "color": "Red",
       "description": "A prestigious red wine"
     }'

# Get all users
curl "http://localhost:8000/api/v1/users/"

# Get all wines
curl "http://localhost:8000/api/v1/wines/"
```

## 🏛️ DDD Concepts Implemented

### **Domain Layer**
- **Entities**: `User`, `Wine` with business methods
- **Value Objects**: `Email`, `Username` with validation
- **Domain Services**: `UserService`, `WineService` with business rules
- **Repository Interface**: Abstract contract for data access

### **Application Layer**
- **Use Cases**: `CreateUserUseCase`, `GetUserUseCase`, `CreateWineUseCase`, etc.
- **DTOs**: Clean data transfer objects
- **Application Services**: Orchestrate domain objects

### **Infrastructure Layer**
- **SQLAlchemy Models**: Database persistence
- **Repository Implementation**: Concrete data access
- **Database Connection**: Technical infrastructure

### **Interface Layer**
- **API Controllers**: Handle HTTP requests
- **Pydantic Schemas**: API validation and serialization

## 🔄 Request Flow (DDD)

### **Create User Flow:**
```
HTTP POST Request → API Controller → Use Case → Domain Service → Repository → Database
     ↓                    ↓              ↓              ↓              ↓              ↓
JSON Payload → UserCreateRequest → CreateUserUseCase → UserService → UserRepository → SQLite
```

### **Detailed Flow:**
1. **Interface Layer**: `users_controller.py` receives HTTP request
   - Validates request with `UserCreateRequest` schema
   - Creates `CreateUserDTO` from request data
   - Calls `CreateUserUseCase`

2. **Application Layer**: `CreateUserUseCase` orchestrates the operation
   - Receives `CreateUserDTO`
   - Calls `UserService.create_user()`
   - Returns `UserResponse` DTO

3. **Domain Layer**: `UserService` contains business logic
   - Creates `Email` and `Username` value objects
   - Validates business rules (unique email/username)
   - Creates `User` domain entity
   - Calls repository to persist

4. **Infrastructure Layer**: `SQLAlchemyUserRepository` handles persistence
   - Converts domain entity to SQLAlchemy model
   - Saves to database
   - Returns domain entity

### **Response Flow:**
```
Database → Repository → Domain Service → Use Case → Controller → HTTP Response
    ↓           ↓              ↓              ↓           ↓              ↓
SQLite → UserModel → User Entity → UserResponse → UserResponse → JSON Response
```

## 🎨 Adding New Domains

To add a new domain (e.g., Products):

1. **Create Domain Layer**:
   ```bash
   app/domains/products/
   ├── domain.py      # Product entity, value objects
   ├── repository.py  # Repository interface
   └── services.py    # Domain services
   ```

2. **Create Application Layer**:
   ```bash
   app/application/products/
   ├── dto.py         # DTOs
   └── use_cases.py   # Use cases
   ```

3. **Create Infrastructure Layer**:
   ```bash
   app/infrastructure/repositories/product_repository.py
   ```

4. **Create Interface Layer**:
   ```bash
   app/interfaces/api/controllers/products_controller.py
   ```

## 🛠️ Development

### Database Migrations

```bash
# Create migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head
```

### Environment Variables

- `DATABASE_URL`: Database connection string (default: SQLite)
- `DEBUG`: Enable debug mode
- `SECRET_KEY`: Secret key for security

## 📚 DDD Resources

- [Domain Driven Design by Eric Evans](https://www.domainlanguage.com/ddd/)
- [Clean Architecture by Robert C. Martin](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Follow DDD principles
4. Add tests for domain logic
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License. 