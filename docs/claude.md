# Kundali Application - Master Control Document

## Project Overview
Building a production-ready astrology application using Flutter for frontend with a multi-agent development approach. Each agent has specialized skills and documentation to maintain code quality and consistency.

## Project Structure
```
FInalProject/
├── client/                        # Flutter Frontend Application
│   ├── lib/
│   │   ├── core/                 # Core utilities, constants, helpers
│   │   ├── data/                 # Data layer (models, repositories, services)
│   │   ├── presentation/         # UI layer (screens, widgets, state management)
│   │   └── main.dart             # App entry point
│   ├── android/                  # Android platform configuration
│   ├── ios/                      # iOS platform configuration
│   ├── linux/ & macos/           # Desktop platform configurations
│   ├── pubspec.yaml              # Flutter dependencies
│   └── analysis_options.yaml      # Dart analysis configuration
│
├── server/                        # Python FastAPI Backend
│   ├── main.py                   # FastAPI application entry
│   ├── database.py               # Database configuration
│   ├── routes/                   # API endpoint routes
│   ├── models/                   # SQLAlchemy database models
│   ├── pydantic_schemas/         # Request/Response schemas
│   ├── services/                 # Business logic services
│   ├── middleware/               # Custom middleware
│   ├── ml/                       # Machine Learning components
│   ├── utils/                    # Helper utilities
│   ├── rule_engine/              # Astrological rule engine
│   ├── swisseph_data/            # Swiss Ephemeris data files
│   └── venv/                     # Python virtual environment
│
├── docs/                         # Project Documentation
│   ├── claude.md                 # Master control document (THIS FILE)
│   ├── design/                   # Design system documentation
│   │   ├── design-system.md
│   │   ├── ui-mockups.md
│   │   └── color-palette.md
│   ├── api/                      # API documentation
│   │   ├── api-documentation.md
│   │   ├── data-models.md
│   │   └── error-handling.md
│   ├── state-management/         # State management documentation
│   │   ├── state-patterns.md
│   │   └── data-flow.md
│   └── testing/                  # Testing documentation
│       ├── test-strategy.md
│       └── playwright-setup.md
│
├── tests/                        # Root-level test configurations
├── requirements.txt              # Python dependencies
├── pubspec.yaml                  # Flutter package management
├── Procfile                      # Deployment configuration
├── pytest.ini                    # Testing configuration
├── TODO.md                       # Project todos and tracking
└── [Config files]                # Various documentation and configs
```

## 🤖 Agent Architecture

### 1. Frontend Agent (UI/UX)
**Primary Role**: Design and implement all user interface components, layouts, and user experience flows.

**Skills & Responsibilities**:
- Create Flutter widgets and layouts
- Implement responsive designs
- Handle navigation and routing
- Manage theming and styling
- Ensure accessibility standards

**Documentation Reference**:
- `.claude/agents/flutter-ui-developer.md` - Complete UI/UX guidelines
- `docs/design/design-system.md` - Design system and components
- `docs/design/ui-mockups.md` - Screen mockups and wireframes
- `docs/design/color-palette.md` - Color schemes and theming

**Key Constraints**:
- Must follow Material Design 3 / Cupertino guidelines
- All widgets must be reusable and modular
- Implement dark/light theme support
- Focus on mystical, cosmic aesthetics

---

### 2. State Management Agent
**Primary Role**: Handle all state management, business logic, and data flow throughout the application.

**Skills & Responsibilities**:
- Implement Riverpod state management
- Manage app-wide state
- Handle user session state
- Coordinate data updates
- Optimize performance and reactivity

**Documentation Reference**:
- `.claude/agents/state-architect.md` - State architecture
- `docs/state-management/state-patterns.md` - State management patterns
- `docs/state-management/data-flow.md` - Data flow diagrams

**Key Constraints**:
- Use **Riverpod** for state management
- Immutable state patterns
- Clear separation of concerns
- Efficient rebuild optimization

---

### 3. API/Data Agent
**Primary Role**: Analyze backend API structure and implement seamless frontend-backend integration.

**Skills & Responsibilities**:
- Analyze backend API in `/server` folder
- Generate/maintain API documentation
- Create data models and DTOs
- Implement API client services
- Handle error handling and retries
- Manage data caching strategies

**Documentation Reference**:
- `.claude/agents/api-data-architect.md` - API integration guidelines
- `docs/api/api-complete-reference.md` - Backend API specifications
- `docs/api/data-models.md` - Data model schemas
- `docs/api/error-handling.md` - Error handling patterns

**Key Constraints**:
- Must analyze existing `/server` backend code
- Auto-generate API documentation if missing
- Type-safe API calls
- Proper error boundary handling

---

### 4. Testing Agent (Playwright MCP)
**Primary Role**: Implement comprehensive testing strategy using Playwright MCP for end-to-end testing.

**Skills & Responsibilities**:
- Write E2E tests with Playwright
- Create widget tests
- Implement integration tests
- Setup CI/CD test automation
- Performance testing
- Accessibility testing

**Documentation Reference**:
- `.claude/agents/test-automation-qa.md` - Testing guidelines
- `docs/testing/test-strategy.md` - Overall test strategy
- `docs/testing/playwright-setup.md` - Playwright MCP configuration

**Key Constraints**:
- Use Playwright MCP for browser testing
- Minimum 80% code coverage goal
- Test critical user flows first
- Automated regression testing

---

## 📋 Workflow Phases

### Phase 1: Foundation Setup (Current)
- [ ] Initialize Flutter project structure
- [ ] Setup all agent documentation
- [ ] Configure MCP Playwright
- [ ] Create design system
- [ ] Analyze backend API structure

### Phase 2: Design & Architecture
- [ ] Complete UI mockups for all screens
- [ ] Define state management architecture
- [ ] Document API endpoints and data models
- [ ] Create reusable widget library
- [ ] Setup testing infrastructure

### Phase 3: Core Development
- [ ] Implement authentication flow
- [ ] Build main dashboard/home screen
- [ ] Create horoscope display features
- [ ] Implement birth chart generation
- [ ] Add planetary positions feature
- [ ] Build compatibility checker

### Phase 4: Integration
- [ ] Connect frontend to backend APIs
- [ ] Implement state management flows
- [ ] Add error handling
- [ ] Setup data caching
- [ ] Optimize performance

### Phase 5: Testing & Polish
- [ ] Write comprehensive E2E tests
- [ ] Perform accessibility audit
- [ ] UI/UX polish and animations
- [ ] Performance optimization
- [ ] Bug fixing

---

## 🎯 Agent Collaboration Rules

### When Frontend Agent Needs Help:
- **State Management Agent**: For complex state logic, data flow
- **API Agent**: For data fetching requirements, model definitions
- **Testing Agent**: For widget testing, visual regression testing

### When State Management Agent Needs Help:
- **Frontend Agent**: For UI state requirements, user interactions
- **API Agent**: For data transformation, async operations
- **Testing Agent**: For state testing, integration tests

### When API Agent Needs Help:
- **State Management Agent**: For state sync, data updates
- **Frontend Agent**: For UI-specific data formatting
- **Testing Agent**: For API mocking, integration tests

### When Testing Agent Needs Help:
- **All Agents**: For understanding test scenarios, edge cases
- **Focus**: Automating tests after features are built

---

## Documentation Index

### [Agent Documentation](./agents/)
Guidelines and instructions for autonomous agents working on specific components.

### [Design Documentation](./design/)
Architecture and design decisions for the project.

### [API Documentation](./api/)
Complete API endpoint reference and specifications.

### [State Management](./state-management/)
Frontend state management with Riverpod.

### [Testing Documentation](./testing/)
Testing strategies and test coverage.

## Key Boundaries

### Client vs Server
- **Client**: Frontend (Flutter), state management (Riverpod), UI components
- **Server**: Backend APIs, database operations, authentication, ML/calculations

⚠️ **CRITICAL**: Never mix client and server concerns. Keep separation of concerns strict.

---

## 🚀 Getting Started

### For Each Agent Session:
1. **Identify Your Agent Role** - Read your specific agent documentation
2. **Check Dependencies** - Review what other agents have completed
3. **Follow Constraints** - Adhere to your agent's key constraints
4. **Update Progress** - Mark completed tasks in workflow phases
5. **Document Changes** - Update relevant documentation files

### Current Priority:
- **API Agent**: Analyze `/server` folder and generate API documentation
- **Frontend Agent**: Create comprehensive design system and UI mockups
- **State Management Agent**: Define state architecture with Riverpod after API analysis
- **Testing Agent**: Setup Playwright MCP infrastructure

---

## 🔧 Configuration

### State Management Choice:
✅ **Riverpod** (Decided)
- Document implementation patterns in `docs/state/state-patterns.md`
- Reference Riverpod best practices for all state management
- Use functional providers and consumers

### API Base Configuration:
📋 [TO BE ANALYZED] - From `/server` folder
- Document in `docs/api/api-documentation.md`
- Generate data models in `docs/api/data-models.md`

### Theme Configuration:
🎨 [TO BE DESIGNED] - Mystical/Cosmic theme
- Document in `docs/design/design-system.md`
- Include color palettes, typography, spacing system
- Define dark/light theme variants

---

## 📝 Notes for Claude Code

- Each agent should reference this master document before starting work
- Cross-agent communication happens through shared documentation
- All agents must maintain consistency with design system
- Testing agent validates work from all other agents
- Keep documentation up-to-date as project evolves
- Use agent-specific documentation as the source of truth for detailed guidance

---

## 🎨 Astrology App Core Features

### Priority Features:
1. **Daily Horoscope** - Personalized daily readings based on zodiac sign
2. **Birth Chart Generation** - Natal chart with planetary positions and aspects
3. **Compatibility Checker** - Relationship compatibility analysis between users
4. **Planetary Transits** - Current planetary positions and astrological meanings
5. **Moon Phases** - Current moon phase and lunar calendar
6. **Tarot Reading** - Digital tarot card readings (optional/Phase 2)

### User Experience Goals:
- Mystical yet modern interface
- Smooth animations and transitions
- Intuitive navigation and discovery
- Personalized experience based on user data
- Fast load times and responsiveness
- Offline capability for saved data and readings

---

## Project Status
- **Current Branch**: anup
- **Phase**: 1 - Foundation Setup
- **Last Updated**: 2025-11-20

## Quick Links
- Frontend Root: `./client/`
- Backend Root: `./server/`
- Documentation Root: `./docs/`

## Agent Control Instructions
1. Refer to this document as the primary source of truth
2. Check respective specialized docs for detailed information
3. Always respect client/server separation
4. Update relevant documentation when making changes
5. Use this document for cross-cutting concerns
6. Follow the workflow phases to track progress

---

*This document is maintained as the central reference point for the entire project. Last reviewed: 2025-11-20*
