# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

[PROJECT_NAME] is a [description]

**Key Technical Achievement**: [achievement description]

**Supabase Project ID**: [supabase-project-id]

## Documentation Structure

- **Main Overview**: `./README.md` - Project overview and quick start
- **Frontend Details**: `./frontend/README.md` - Next.js app, routes, components, hooks
- **Backend Details**: `./backend/README.md` - Services, APIs, deployment


### Infrastructure
- **Database**: Supabase PostgreSQL with RLS
- **File Storage**: GCS
- **Serverless (backend)**: Modal
- **Authentication**: Supabase Auth

## Development Commands

### Directory Structure
**IMPORTANT**: This is a wrapper repository with git submodules:
- `./` - Wrapper repository (main project)
- `./frontend/` - Frontend submodule (separate git repo)
- `./backend/` - Backend submodule (separate git repo)

**Git Operations**: Always run git commands from the correct directory:
- Wrapper operations: Run from root directory
- Frontend operations: `cd frontend` first
- Backend operations: `cd backend` first

### Frontend (Next.js - ShipFast)
```bash
cd frontend
npm run dev             # Start development server (http://localhost:3000)
npm run build           # Build for production
npm run lint            # Run ESLint
```

## Important Notes

- **Submodule Updates**: When pulling changes, use `git submodule update --init --recursive`
- **Separate Repos**: Frontend and backend are independent git repositories

## Development Best Practices

- **NO AUTO-COMMITS**: Never commit changes automatically - always explain changes and let user test first
- **Explain Changes**: Always explain what the issue was and what fixes were implemented before making changes
- **Test First**: Always test changes locally before committing

## Testing

- Frontend: [Testing approach]
- Backend: [Testing approach]