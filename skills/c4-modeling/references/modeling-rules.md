# C4 Modeling Rules

## Quality Standard

A C4 diagram must be understandable without the author explaining it live. Every shape, boundary, line, label, and technology annotation should reduce ambiguity.

## Abstraction Rules

- Use one primary C4 abstraction level per diagram.
- Do not place containers, databases, modules, classes, or tables in a System Context view.
- Do not place database tables, classes, functions, or low-level packages in a Container view.
- Do not create Component views unless the internals of a specific container require explanation.
- Avoid Code views unless the user explicitly requests them or the implementation is unusually complex.
- If the user needs multiple abstraction levels, create multiple diagrams instead of one crowded diagram.

## Element Rules

Every element should include:

- **Name:** concrete and recognizable in the domain or codebase
- **Type:** person, software system, container, component, deployment node, or infrastructure element
- **Responsibility:** a short phrase explaining what it does
- **Technology:** included when useful at that view level

Avoid generic names such as:

- Backend
- Frontend
- Logic
- Business Logic
- Manager
- Processor
- Data
- Database

Prefer names that combine responsibility and technology where appropriate:

- Customer Web App, React SPA
- Orders API, Kotlin/Spring Boot service
- Payments Database, PostgreSQL schema
- Delivery Assignment Worker, Go service
- Order Events, Kafka topic

## Relationship Rules

Every relationship must include:

- Directional arrow
- Descriptive verb phrase
- Protocol, format, or mechanism when known
- Sequence number when used in Dynamic diagrams

Good relationship labels:

- Submits order via HTTPS/JSON
- Publishes order-created event to Kafka
- Reads customer profile from PostgreSQL
- Exchanges token using OAuth 2.0
- Streams status updates over WebSocket

Poor relationship labels:

- Data
- Uses
- Talks to
- API
- Sync
- Business logic

Use bidirectional arrows only when bidirectionality is intentional and clearer than two explicitly labeled arrows.

## Notation Rules

C4 does not mandate colors, icons, or shapes, but the notation must be explicit.

- Use consistent shapes for the same ontological type.
- Use boundaries to show system, container, or deployment scopes.
- Include a legend when colors, icons, line styles, or border styles carry meaning.
- Keep visual styling subordinate to semantic clarity.
- Prefer automatic layout for generated diagrams unless manual layout is required for readability.

## Review Checklist

Before presenting a C4 artifact, verify:

- The view has a clear title and scope.
- The target audience can understand the diagram without lower-level detail.
- The system boundary is explicit.
- Each element has a name and responsibility.
- Each relationship is directional and labeled.
- Protocols and formats are included where known.
- No abstraction levels are mixed.
- No unexplained notation is present.
- No inferred relationship is presented as verified fact.
- The diagram is not trying to answer too many questions at once.

## Common Anti-Patterns

### Boxes And Lines

Shapes and connections appear meaningful but lack labels, direction, responsibilities, or type definitions.

**Fix:** add element descriptions, relationship labels, arrow direction, and a legend.

### Everything Diagram

One diagram includes users, systems, services, classes, tables, queues, deployments, and workflows.

**Fix:** split into Context, Container, Dynamic, Deployment, or Component views.

### Implementation Leak

A high-level stakeholder diagram includes database tables, classes, functions, or framework internals.

**Fix:** move those details to Component or Code views, or remove them entirely.

### Unmaintainable Code Diagram

A static class-level diagram attempts to mirror fast-changing source code.

**Fix:** rely on source code, generated docs, tests, IDE navigation, or a focused ADR unless the diagram explains unusually complex logic.

### Diagram Drift

Hand-drawn diagrams become stale after deployments, service renames, or dependency changes.

**Fix:** define the model in text, version it with code, and generate views from the model.
