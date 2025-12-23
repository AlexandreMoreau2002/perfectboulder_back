# Codex Usage Examples

Common scenarios when working with Codex on the perfectBoulder backend.

## Development Workflow

### Starting a Development Session

```bash
# Start the stack
codex task start

# Watch the logs
codex task logs

# In another terminal, open a shell if needed
codex task shell
```

### Making Code Changes

**Scenario**: Adding a new API endpoint

```bash
# 1. Ask Codex to implement
codex "Add a new REST endpoint GET /api/v1/climbs that returns a list of climbs"

# Codex will:
# - Create domain/climbs/entities.py
# - Create application/climbs/service.py
# - Create adapters/rest/climbs.py
# - Register route in main.py
# - Ask clarifying questions if needed

# 2. Test the changes
codex task health
curl http://localhost:8000/api/v1/climbs

# 3. Lint the code
codex task lint

# 4. Fix linting issues
codex task lint-fix
```

### Code Review & Cleanup

```bash
# Check code formatting
codex task format-check

# Apply formatting
codex task format

# Clean cache files
codex task clean
```

## Database Operations

### Exploring the Database

```bash
# Connect to PostgreSQL
codex task db-connect

# Inside psql:
# \dt              List tables
# \d table_name    Describe table
# SELECT * FROM climbs LIMIT 5;
# \q               Exit
```

### Schema Changes

```bash
# Ask Codex to create migration
codex "Create a migration to add a 'difficulty' column to climbs table"

# Codex will:
# - Check existing schema
# - Create migration file
# - Update models if needed
# - Test the migration
```

### Backup & Restore

```bash
# Backup before major changes
codex task db-backup

# Make changes...

# If something goes wrong, restore
codex task db-restore  # Requires confirmation
```

## GraphQL Development

### Adding GraphQL Types

```bash
# Ask Codex to extend GraphQL schema
codex "Add a GraphQL type for Climb with fields: id, name, grade, location"

# Codex will:
# - Update adapters/graphql/schema.py
# - Create Strawberry types
# - Add resolvers
# - Follow hexagonal pattern (delegate to services)
```

### Testing GraphQL

```bash
# Introspect schema
codex task graphql-introspect

# Or ask Codex to test a query
codex "Test this GraphQL query: { climbs { id name grade } }"
```

## Debugging

### Investigating Issues

```bash
# View logs in real-time
codex task logs

# Check database logs
codex task logs-db

# Check container status
codex task ps

# Check resource usage
codex task stats
```

### Common Problems

**Problem**: Database connection fails

```bash
# Ask Codex to diagnose
codex "The backend can't connect to the database. Please diagnose the issue."

# Codex will:
# - Check container status (codex task ps)
# - Check DB logs (codex task logs-db)
# - Verify environment variables
# - Test connection from backend container
# - Suggest fixes
```

**Problem**: Import errors

```bash
codex "I'm getting ImportError for psycopg. Help me fix this."

# Codex will:
# - Check requirements.txt
# - Verify installation in container
# - Suggest running deps-install if needed
```

## Testing (When Implemented)

```bash
# Run all tests
codex task test

# Run with coverage
codex task test-coverage

# Watch mode (re-run on changes)
codex task test-watch

# Ask Codex to write tests
codex "Write unit tests for the climbs service following AAA pattern"

# Codex will:
# - Create tests/application/test_climbs_service.py
# - Follow AAA pattern (Arrange, Act, Assert)
# - Mock external dependencies
# - Ensure 80% coverage
```

## Architecture Questions

### Understanding Existing Code

```bash
codex "Explain how the health check endpoint works"
codex "Where is the database connection configured?"
codex "Show me all GraphQL types defined in the schema"
```

### Following Patterns

```bash
# Codex knows the patterns from prompts/system.md
codex "Add a new feature for user authentication following hexagonal architecture"

# Codex will:
# - Create domain/auth/entities.py (User, Token)
# - Create application/auth/service.py (login, verify_token)
# - Create adapters/rest/auth.py (routes)
# - Add middleware for JWT verification
# - Follow all constraints from codex.agent.yml
```

## Refactoring

```bash
# Ask for explanations before refactoring
codex "Review the current structure of the application layer and suggest improvements"

# If refactoring is needed:
codex "Refactor the health service to follow the repository pattern"

# Codex will:
# - Ask for approval (constraint: minimal changes)
# - Show proposed changes
# - Refactor incrementally
# - Verify tests still pass
# - Update documentation
```

## Documentation

### Updating Docs

```bash
# After adding a feature
codex "Update README.md and COMMANDS.md to document the new climbs API"

# After changing configuration
codex "Update .env.example with the new REDIS_URL variable"
```

### Creating Context for Next AI

```bash
# After major changes
codex "Create a CONTEXT.md file documenting the new authentication system for the next AI"

# Or update .agent/ contracts
codex "Update .agent/backend.md with the new authentication middleware pattern"
```

## Advanced Scenarios

### Multi-Step Features

```bash
codex "Implement a complete CRUD API for climbs:
1. Create domain entities (Climb, ClimbRepository)
2. Create application service (ClimbService with CRUD methods)
3. Create REST endpoints (GET, POST, PUT, DELETE /api/v1/climbs)
4. Create GraphQL types and resolvers
5. Add proper error handling
6. Write unit tests
7. Update documentation

Ask me questions if anything is unclear."
```

### Infrastructure Changes

```bash
# Adding a new service
codex "Add Redis to docker-compose.yml for caching, following our infrastructure patterns"

# Codex will:
# - Update docker-compose.yml
# - Add redis service
# - Add environment variables
# - Update .env.example
# - Update COMMANDS.md
# - Request review (policy: docker-compose.yml requires review)
```

### Security Review

```bash
codex "Review the authentication endpoints for security vulnerabilities"

# Codex will check:
# - Secrets not logged (constraint)
# - Input validation (constraint)
# - JWT verification
# - SQL injection protection
# - CORS configuration
```

## Best Practices

### Always Provide Context

❌ Bad:
```bash
codex "Add an endpoint"
```

✅ Good:
```bash
codex "Add a REST endpoint GET /api/v1/climbs/{id} that:
- Accepts an integer climb ID
- Returns climb details (name, grade, location, description)
- Returns 404 if climb not found
- Follows our hexagonal architecture
- Uses the existing ClimbService from application layer"
```

### Leverage Task Shortcuts

❌ Bad:
```bash
codex "Run the docker compose up command to start the backend"
```

✅ Good:
```bash
codex task start
```

### Ask for Explanations

```bash
# Before implementing
codex "Before I ask you to add user authentication, explain:
1. Where user entities should live in our hexagonal architecture
2. How JWT tokens should be verified
3. Where middleware should be added
4. What security considerations apply"
```

### Use Definition of Done

```bash
codex "Add a new feature for climb favorites.
Remember Definition of Done:
1. Test the feature
2. Update relevant docs (README, COMMANDS)
3. Create context notes for next AI"
```

## Common Shortcuts

### Quick Checks
```bash
codex task health          # API health check
codex task lint            # Quick lint
codex task ps              # Container status
```

### Quick Fixes
```bash
codex task lint-fix        # Auto-fix linting
codex task format          # Format code
codex task clean           # Remove cache
```

### Quick Access
```bash
codex task shell           # Backend shell
codex task db-connect      # Database shell
codex task logs            # View logs
```

## Troubleshooting Codex

### Codex Not Following Constraints

If Codex violates a constraint (e.g., adds business logic to routes):

```bash
codex "Stop. You added business logic to the route, which violates our hexagonal architecture constraint.
Please refactor to move the logic to application/climbs/service.py and have the route delegate to it."
```

### Codex Being Too Cautious

If Codex asks too many questions:

```bash
codex "You have enough context from prompts/system.md. Proceed with implementing the feature following our established patterns."
```

### Codex Needs More Context

```bash
codex "Before implementing, read these files to understand the pattern:
- app/adapters/rest/health.py
- app/application/health/service.py
- app/domain/health/entities.py"
```
