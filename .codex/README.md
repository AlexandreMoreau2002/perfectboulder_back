# .codex Configuration Directory

This directory contains configuration files for **Codex AI** (or similar AI development assistants) to understand the project context, architecture, and development workflow.

## Directory Structure

```
.codex/
├── README.md              # This file
├── config.toml            # Main Codex configuration
├── codex.agent.yml        # Agent role, constraints, and policies
├── codex.tasks.yml        # Predefined development tasks
├── profiles/
│   └── dev.toml          # Development profile (low reasoning, fast)
└── prompts/
    ├── system.md         # Project architecture and patterns
    └── devops.md         # Infrastructure and deployment context
```

## File Purposes

### `config.toml`
Main configuration file that:
- Defines the AI model and parameters
- Points to workspace root
- References prompt files for context
- Sets up execution policies (confirmations, dry-run)
- Configures logging and secret redaction

### `codex.agent.yml`
Defines the AI agent's:
- **Role**: Backend engineer for perfectBoulder
- **Objectives**: What the agent should accomplish
- **Constraints**: Hard rules that must never be violated
  - Architecture patterns (Hexagonal)
  - Security requirements
  - Code quality standards
  - Development rules from `.agent/` contracts
- **Policies**: What requires confirmation or review
- **Context paths**: Files the agent should be aware of

### `codex.tasks.yml`
Predefined tasks the agent can execute:
- Development: `start`, `stop`, `reset`
- Monitoring: `logs`, `ps`, `stats`
- Code quality: `lint`, `format`
- Database: `db-connect`, `db-backup`, `db-restore`
- Testing: `test`, `test-coverage`
- API testing: `health`, `graphql-introspect`
- Utilities: `clean`, `deps-update`

### `prompts/system.md`
Deep context about the project:
- Architecture principles (Hexagonal)
- Technology stack details
- Configuration patterns
- Development workflow
- Common patterns and anti-patterns
- Security guidelines

### `prompts/devops.md`
Infrastructure and operations context:
- Docker setup and services
- Makefile commands
- Database administration
- Deployment patterns
- Monitoring and debugging
- Code quality tools

### `profiles/dev.toml`
Environment-specific overrides:
- Lower reasoning effort (faster responses)
- Temperature 0.0 (deterministic)
- Dev environment variables

## How Codex Uses This

When Codex is invoked on this project:

1. **Loads `config.toml`** - Gets base configuration
2. **Reads prompt files** - Understands project context
3. **Parses `codex.agent.yml`** - Knows its role, constraints, policies
4. **Loads `codex.tasks.yml`** - Has predefined tasks available
5. **Applies profile** - Uses dev/prod specific settings

## Key Constraints

The agent is configured with strict constraints from `.agent/` contracts:

### Non-Negotiables
- ❌ Never add dependencies without explicit instruction
- ❌ Never commit `.env` files
- ❌ Never log secrets
- ❌ No speculative features
- ✅ Ask before assuming (1-3 targeted questions)
- ✅ Minimal, localized changes

### Architecture
- Hexagonal: `domain` → `application` → `adapters` → `infra`
- No business logic in routes
- "Escalier" import ordering (sorted by length)

### Definition of Done (Mandatory)
Every task must conclude with:
1. **Test**: Verify code works
2. **Update docs**: If behavior changed
3. **Create context**: Help next AI (CONTEXT.md or `.agent/` notes)

## Running Tasks

Example Codex commands (if using Codex CLI):

```bash
# Start development environment
codex task start

# Run linter
codex task lint

# Auto-fix linting issues
codex task lint-fix

# Connect to database
codex task db-connect

# Run tests with coverage
codex task test-coverage

# Check API health
codex task health
```

## Confirmation Required

The following commands require explicit confirmation:
- `reset-volumes` (destroys database data)
- `db-restore` (overwrites database)
- `docker compose down -v`
- `DROP DATABASE`, `TRUNCATE`

## Review Required

Changes to these files/directories require review:
- `app/domain/**` (core business logic)
- `app/config.py` (settings)
- `docker-compose.yml` (infrastructure)
- `Dockerfile` (container image)
- `requirements.txt` (dependencies)

## Extending

### Adding New Tasks

Edit `codex.tasks.yml`:

```yaml
my-task:
  desc: "Description of what this does"
  cmd: "command to execute"
  confirm: true  # Optional: require confirmation
```

### Adding Context

Create new `.md` files in `prompts/` and reference in `config.toml`:

```toml
[prompts]
paths = [
  ".codex/prompts/system.md",
  ".codex/prompts/devops.md",
  ".codex/prompts/my-new-context.md"
]
```

### Creating New Profiles

Add files to `profiles/`:

```toml
# profiles/prod.toml
model_reasoning_effort = "high"
temperature = 0.0
[env.vars]
ENV = "production"
```

## Integration with Parent Repo

This `.codex` configuration is **backend-specific**. The parent repo has:
- `/.agent/` - Cross-repo AI agent contracts (source of truth)
- `/CLAUDE.md` - High-level guidance for Claude Code

The hierarchy:
1. **`/.agent/`** - Authoritative rules for all AI agents
2. **`/CLAUDE.md`** - Claude Code specific guidance (monorepo level)
3. **`/backend/.codex/`** - Codex specific configuration (service level)

All three must stay in sync. If rules in `.agent/` change, update `.codex/` accordingly.
