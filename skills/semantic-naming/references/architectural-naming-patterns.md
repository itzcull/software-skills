# Architectural Naming Patterns

Architecture gives names additional meaning. Use architectural suffixes only when the construct obeys the constraints of that architecture.

## Domain-Driven Design

Use domain nouns for model concepts and keep technical suffixes out of the core domain unless the suffix is itself a domain term.

| Construct | Naming guidance | Constraint |
|---|---|---|
| Entity | Singular domain noun | Has identity independent of attributes |
| Value Object | Domain noun describing the value | Immutable; equality by value |
| Aggregate Root | Singular domain noun for the consistency boundary | Only external mutation gateway for child entities |
| Specification | Predicate-like rule name | Encapsulates a testable condition |
| Policy | Rule or decision name | Encapsulates context-dependent decision logic |
| Domain Service | Domain operation noun or agent | Pure domain logic; no infrastructure dependency |

Prefer `EmailAddress` over `EmailString`, `FundsTransferService` over `TransferManager`, and `EligibleForDiscountSpecification` over `DiscountHelper`.

## CQRS

CQRS names separate write intent from read intent.

Commands:

- Name commands as imperative business intent plus `Command`.
- Prefer `BookHotelRoomCommand` over `SetReservationStatusCommand`.
- Keep commands passive; execution belongs in a handler.
- Do not let commands invoke other commands or queries.

Queries:

- Name queries for the data being requested plus `Query`.
- Prefer `GetFlightDetailsQuery` or `ActiveInvoicesQuery` over vague `InvoiceQuery`.
- Keep queries side-effect free.
- Return read-optimized DTOs or results, not domain aggregates by default.

Handlers:

- Pair payload and handler names directly: `ApproveInvoiceCommand` and `ApproveInvoiceCommandHandler`.
- A handler should have one primary responsibility: execute that payload.
- If multiple commands must run in sequence, name the orchestrator separately as a process manager, coordinator, or saga.

Events:

- Name events as facts in past tense: `InvoiceApprovedEvent`, `RoomBookedEvent`.
- Do not name an event as a command. `ApproveInvoiceEvent` confuses intent with fact.

## Clean Architecture

Use cases and interactors represent application business rules.

- A use case name should describe one user-visible application capability: `RegisterUserUseCase`, `FindUserUseCase`.
- An interactor is the concrete operational flow for a use case: `RegisterUserInteractor`.
- Do not group unrelated actions into a generic `UserUseCase` class.
- Controllers translate delivery input into request models and call the application boundary.
- Presenters translate response models into view-ready output.
- Gateways and repositories are ports owned by the application or domain, with infrastructure implementations outside the core.

Acceptable simplification: some codebases omit the `UseCase` suffix and rely on directory structure, e.g. `RegisterUser`. Follow the local convention if it remains unambiguous.

## Services

`Service` is overloaded. Use it only when a more precise structural noun does not fit, and qualify it by layer.

| Service type | Meaning | Examples |
|---|---|---|
| Domain Service | Pure business logic spanning domain objects | `FundsTransferService`, `RiskScoringService` |
| Application Service | Orchestrates transactions, repositories, use cases, and adapters | `RegistrationService`, `OrderFulfillmentService` |
| Infrastructure Service | Technical implementation of an external concern | `SmtpEmailService`, `S3FileStorageService` |

If the class formats, parses, validates, calculates, adapts, decorates, or persists, use that more precise word instead of `Service`.

## Distributed Workflows

Use `Saga` and `ProcessManager` for different workflow semantics.

| Construct | Naming guidance | Constraint |
|---|---|---|
| Saga | `OrderFulfillmentSaga` | Stateless choreography of local transactions and compensating actions |
| Process Manager | `OrderFulfillmentProcessManager` | Stateful orchestrator that persists workflow progress and routes next commands |
| Coordinator | `CheckoutCoordinator` | Bounded in-process coordination without claiming distributed transaction semantics |
| Orchestrator | `DeploymentOrchestrator` | Explicit ordered control across components or services |

Do not use `Saga` as a synonym for any long-running workflow. If it stores workflow state and decides the next command, call it a process manager.

## State Machines

State and event names should not blur continuous condition with instantaneous trigger.

State names can follow either convention:

- Static condition: `Idle`, `DoorOpen`, `WaitingForPayment`.
- Ongoing action: `SlidingOpen`, `ProcessingPayment`, `DialingCellphone`.

Event names should describe atomic occurrences or thresholds:

- Past tense facts: `DoorOpened`, `PaymentCaptured`, `FlightLanded`.
- Explicit thresholds: `BatteryBelowLimit`, `TenSecondsElapsed`.
- Imperative external triggers when appropriate: `BeginProcessing`.

Keep a consistent convention within a state machine. Mixing `DoorOpen` as a state with `DoorOpened` as an event is acceptable only when the distinction is deliberate and clear.

## Request Pipelines

Pipeline names should reveal where and how the component acts.

| Construct | Responsibility | Examples |
|---|---|---|
| Middleware | Cross-cutting request-response processing, often before routing or handler execution | `LoggingMiddleware`, `BodyParserMiddleware` |
| Interceptor | Wraps handler execution to transform output, measure timing, or add behavior | `ResponseMappingInterceptor`, `TimingInterceptor` |
| Guard | Authorizes or blocks execution before the handler runs | `AuthGuard`, `AdminGuard` |
| Filter | Handles or maps errors and exceptional outcomes | `HttpExceptionFilter`, `ValidationErrorFilter` |

Framework terminology may override generic naming, but the role should still be accurate.

## Physical Persistence Names

Separate logical domain names from physical storage names.

- Domain entities are singular: `Employee`, `Customer`, `Invoice`.
- Tables or collections may be plural if the project convention treats them as containers: `employees`, `customers`, `invoices`.
- Persistence records should reveal that they are not domain objects when both exist: `EmployeeRecord`, `InvoiceRow`, `PrismaUser`.

Do not force domain naming rules onto physical storage when the storage layer has a clear independent convention.
