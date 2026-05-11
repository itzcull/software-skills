# C4 Core Model

## Purpose

The C4 model is a lightweight way to visualize software architecture through progressive disclosure. It avoids a single overloaded diagram by splitting architectural communication into views that match different audiences and levels of detail.

The core metaphor is a map: start zoomed out, then move inward only when the reader needs more detail.

## Level 1: System Context

**Audience:** business stakeholders, product managers, executives, architects, and engineers new to the system.

**Scope:** one software system as an opaque box, plus people and external software systems that interact with it.

**Use it to show:**

- System boundary
- Primary users or personas
- External systems
- Enterprise integration points
- High-level purpose and scope

**Omit:** containers, databases, programming languages, frameworks, internal modules, network topology, classes, functions, and deployment details.

## Level 2: Container

In C4, a container is any separately runnable or deployable unit that executes code or stores data. It does not necessarily mean a Docker container.

**Audience:** software architects, engineering leads, DevOps, platform teams, and developers.

**Scope:** the major applications, services, data stores, clients, message brokers, and other runtime units inside one software system.

**Common containers:**

- Server-side web application
- API service
- Single-page application
- Mobile app
- Desktop app
- Relational database schema
- Document database
- File store or object store
- Message broker or queue
- Worker process
- Scheduled job

**Use it to show:**

- Major technology choices
- Responsibilities of deployable units
- Inter-process communication
- Protocols, formats, and runtime dependencies
- Data ownership at a high level

The Container view is usually the most valuable C4 view for engineering teams because it connects product-level intent to deployable software structure.

## Level 3: Component

**Audience:** developers and maintainers working inside a specific container.

**Scope:** the significant logical building blocks within one container.

**Use it to show:**

- Internal module boundaries
- Controllers, services, repositories, adapters, workers, or domain components
- How components collaborate inside the container
- How internal components interact with external containers or systems

Create Component views only when they clarify structure that cannot be inferred easily from the codebase. Avoid them for small services where the container responsibility is narrow and code organization is already clear.

## Level 4: Code

**Audience:** developers working on complex implementation details.

**Scope:** classes, interfaces, functions, objects, and implementation-level relationships.

**Default stance:** avoid Level 4 diagrams. Static code diagrams drift quickly and are usually superseded by IDE navigation, generated documentation, source code, tests, and localized ADRs.

Use Code diagrams only for unusually complex, mission-critical logic where a static structural explanation materially reduces risk.

## Supplementary Views

### System Landscape

Shows an organization's broader portfolio of software systems and the people or teams that interact with them. Use it when the question is about enterprise-level system relationships rather than one product boundary.

### Dynamic

Shows how elements collaborate over time to complete a use case, user story, transaction, or workflow. It complements the static model by adding sequence and runtime behavior.

Dynamic diagrams are especially useful for:

- Authentication flows
- Checkout or payment transactions
- Event-driven workflows
- Asynchronous message propagation
- Cross-service orchestration
- Failure-prone distributed transactions

Use numbered interactions to make sequence explicit.

### Deployment

Shows how containers map to infrastructure. Use it when operational reliability, cloud topology, network boundaries, redundancy, or runtime placement matters.

Deployment diagrams may include:

- Deployment nodes
- Cloud accounts, regions, zones, and clusters
- Virtual machines, Kubernetes clusters, serverless platforms, or managed services
- Container instances
- Load balancers and network boundaries
- Environment differences such as staging and production

In modern cloud-native systems, Deployment views are often more useful than Code views.

## Default View Selection

| Need | Default View |
|---|---|
| Explain what the system is and who uses it | System Context |
| Explain deployable software structure | Container |
| Explain internals of one complex application | Component |
| Explain one runtime workflow | Dynamic |
| Explain cloud or infrastructure mapping | Deployment |
| Explain many systems across an organization | System Landscape |
| Explain classes or implementation details | Code, only by exception |

## Related Skills

- Use `system-design` to explore architecture choices, scalability patterns, and distributed-system tradeoffs before modeling.
- Use `architecture-decision-record` to record why an architectural choice was made.
- Use `domain-driven-design` when model boundaries depend on domain language, bounded contexts, and ownership.
