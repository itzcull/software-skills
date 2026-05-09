# Naming Decision Process

Use this process before introducing a new name or changing an existing one. The goal is not to force every construct into a pattern. The goal is to make the name match the construct's real responsibility.

## 1. Find the Local Language

Start with nearby code and domain vocabulary:

- Inspect analogous files before naming new constructs.
- Prefer names already used by domain experts, product language, API contracts, or existing bounded contexts.
- Preserve local conventions when they are coherent and not misleading.
- Do not introduce a new suffix family if the codebase already has a precise, established one.

If the same business concept has multiple names, stop and choose the term that matches the authoritative domain language before adding more code.

## 2. Classify the Construct

Ask what the construct primarily is:

| Question | Likely category | Naming shape |
|---|---|---|
| Does it have persistent identity across time? | Entity | Singular domain noun, e.g. `User`, `Invoice` |
| Is equality based only on attributes? | Value Object | Domain noun for the described value, e.g. `EmailAddress`, `Money` |
| Is it the only mutation gateway for a consistency boundary? | Aggregate Root | Singular domain noun, often the root concept, e.g. `Order` |
| Does it represent intent to change state? | Command | Imperative verb phrase plus `Command`, e.g. `ApproveInvoiceCommand` |
| Does it request data without mutation? | Query | Data request phrase plus `Query`, e.g. `GetInvoiceDetailsQuery` |
| Does it execute exactly one command, query, event, or request? | Handler | Payload name plus `Handler`, e.g. `ApproveInvoiceCommandHandler` |
| Does it carry data across a boundary? | DTO / Result / Event | Noun phrase plus role, e.g. `InvoiceDto`, `InvoiceApprovedEvent` |
| Does it orchestrate one user-visible application action? | Use Case / Interactor | Verb plus domain noun, optionally suffixed, e.g. `RegisterUserUseCase` |
| Does it adapt an external system or interface? | Adapter / Gateway / Provider | External concern plus role, e.g. `StripePaymentGateway` |
| Does it store and retrieve aggregate roots? | Repository | Domain noun plus `Repository`, e.g. `OrderRepository` |
| Does it format, calculate, convert, parse, or validate? | Function-specific agent | Exact action noun, e.g. `DateFormatter`, `TaxCalculator` |
| Does it coordinate a multi-step workflow? | Coordinator / Orchestrator / Process Manager | Workflow noun plus explicit role, e.g. `CheckoutCoordinator` |

If no category fits, the construct may be doing too much or the domain concept has not been named yet.

## 3. Decide Active vs Passive

Names should distinguish behavior from information.

Active constructs perform work:

- Use verbs for functions and use cases: `calculateTax`, `registerUser`, `sendReceipt`.
- Use imperative intent for commands: `BookHotelRoomCommand`, not `ReservationStatusCommand`.
- Use agent nouns for single-purpose workers: `InvoiceValidator`, `CsvParser`, `CurrencyConverter`.

Passive constructs carry facts:

- Use nouns for entities and value objects: `Customer`, `Address`, `Money`.
- Use past-tense events for things that happened: `InvoiceApprovedEvent`.
- Use result or DTO suffixes for boundary payloads: `InvoiceDetailsResult`, `CustomerDto`.

Avoid naming passive data as if it performs an action. `SecurityFlawReport` is a report payload; `ReportSecurityFlawCommand` is an instruction to create or submit one.

## 4. Check the Boundary

Names should reveal architectural layer when the layer carries behavioural constraints:

- Domain layer names should usually be business nouns and verbs, not framework names.
- Application layer names may include `UseCase`, `Interactor`, `Command`, `Query`, `Handler`, `Service`, or `Coordinator` when those roles are explicit.
- Infrastructure names should reveal the external mechanism or provider: `SmtpEmailProvider`, `PostgresOrderRepository`, `RabbitMqEventBus`.
- Interface adapter names should reveal translation responsibility: `HttpOrderController`, `OrderPresenter`, `StripePaymentAdapter`.

Do not leak volatile infrastructure into domain names. `User` is a domain entity; `PrismaUserRecord` is a persistence representation.

## 5. Test the Name

Before accepting a name, ask:

- Would a reader correctly predict what this construct is allowed to do?
- Does the name exclude unrelated responsibilities?
- Can another developer tell whether this is data, behavior, orchestration, or infrastructure?
- Does the suffix imply a contract the implementation actually honours?
- Is the name stable if the implementation changes but the responsibility stays the same?

If the name needs a comment to explain what category it belongs to, rename it or split the construct.

## 6. Prefer Minimal Precision

A name should be precise enough to prevent misuse, but not a full implementation summary.

Prefer:

- `PaymentPolicy` over `PaymentConditionalBusinessRuleEvaluationLogic`
- `RetryDecorator` over `RetryWrapper`
- `OrderRepository` over `OrderDatabaseStorageManager`
- `GetActiveInvoicesQuery` over `ActiveInvoicesQueryRequestData`

Long names are acceptable when they encode real domain distinctions, but verbosity is not a substitute for a clear abstraction.
