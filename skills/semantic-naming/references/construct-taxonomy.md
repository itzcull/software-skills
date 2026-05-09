# Construct Taxonomy

Use this table as a naming reference. A suffix is appropriate only when the construct satisfies the semantic responsibility described here.

| Archetype | Context | Semantic responsibility | Naming examples |
|---|---|---|---|
| Entity | Domain-Driven Design | Object with persistent identity and lifecycle; encapsulates domain state and invariants | `User`, `Job`, `Invoice` |
| Value Object | Domain-Driven Design | Immutable descriptor with equality by attributes, not identity | `EmailAddress`, `Money`, `MessageText` |
| Aggregate Root | Domain-Driven Design | Entity that protects a consistency boundary and controls access to child entities | `Order`, `Account`, `Job` |
| Specification | DDD / Design Patterns | Composable predicate or named rule for whether something satisfies a condition | `ActiveUserSpecification`, `EligibleForDiscountSpec` |
| Policy | Domain / Application | Context-dependent rule or strategy for deciding what action should be taken | `RefundPolicy`, `PasswordRotationPolicy` |
| Factory | Creational Pattern | Encapsulates object creation when construction has meaningful rules or variation | `InvoiceFactory`, `PokemonFactory` |
| Builder | Creational Pattern | Assembles a complex object through multiple explicit configuration steps | `ReportBuilder`, `HttpRequestBuilder` |
| Command | CQRS / Application | Passive payload expressing imperative intent to mutate state | `ApproveInvoiceCommand`, `BookHotelRoomCommand` |
| Query | CQRS / Application | Passive payload requesting data without side effects | `GetInvoiceDetailsQuery`, `ActiveInvoicesQuery` |
| Handler | CQRS / Messaging | Executes one command, query, event, or request type | `ApproveInvoiceCommandHandler`, `InvoiceApprovedEventHandler` |
| Result | Application / Query | Passive payload returned from a use case or query | `InvoiceDetailsResult`, `RegistrationResult` |
| DTO | Boundary / Transport | Passive data shape crossing process, API, persistence, or UI boundaries | `InvoiceDto`, `CreateUserRequestDto` |
| Event | Domain / Integration | Immutable fact that something already happened | `InvoiceApprovedEvent`, `PaymentCaptured` |
| UseCase | Clean Architecture | Single application capability or user goal | `RegisterUserUseCase`, `SendPaymentUseCase` |
| Interactor | Clean Architecture | Concrete implementation of a use case's operational flow | `RegisterUserInteractor`, `SendPaymentInteractor` |
| Domain Service | DDD | Pure domain operation spanning multiple entities or value objects | `FundsTransferService`, `PricingCalculator` |
| Application Service | Application Layer | Orchestrates use cases, transactions, repositories, and adapters | `UserRegistrationService`, `OrderFulfillmentService` |
| Infrastructure Service | Infrastructure | Implements technical integration with external systems | `SmtpEmailProvider`, `AmazonS3FileStorage` |
| Repository | DDD / Persistence Port | Stores and retrieves aggregate roots using domain-oriented collection semantics | `OrderRepository`, `UserRepository` |
| Gateway | Ports and Adapters | Application-owned abstraction over an external system or capability | `PaymentGateway`, `FraudCheckGateway` |
| Adapter | Ports and Adapters / Structural Pattern | Translates one interface or protocol into another | `StripePaymentAdapter`, `LegacyCustomerAdapter` |
| Controller | Interface Adapter | Converts incoming delivery mechanism input into application requests | `OrdersController`, `RegisterUserController` |
| Presenter | Interface Adapter | Formats application response data for a view or delivery mechanism | `InvoicePresenter`, `UserProfilePresenter` |
| Saga | Distributed Workflow | Stateless choreography of local transactions with compensating actions | `OrderFulfillmentSaga` |
| Process Manager | Distributed Workflow | Stateful orchestrator that tracks and routes a long-running workflow | `OrderFulfillmentProcessManager` |
| Coordinator | Application Flow | Coordinates a bounded workflow without owning core domain rules | `CheckoutCoordinator`, `ImportCoordinator` |
| Orchestrator | Application / Infrastructure Flow | Directs ordered calls across components or services | `DeploymentOrchestrator`, `PaymentOrchestrator` |
| Middleware | Request Pipeline | Runs early in request-response flow for cross-cutting request processing | `LoggingMiddleware`, `BodyParserMiddleware` |
| Interceptor | Request Pipeline | Wraps handler execution to transform output, measure execution, or add behavior | `LoggingInterceptor`, `ResponseMappingInterceptor` |
| Guard | Request Pipeline | Allows or blocks access before execution | `AuthGuard`, `RoleGuard` |
| Decorator | Structural Pattern | Adds behavior around another object without changing its interface | `RetryDecorator`, `CachingDecorator` |
| Facade | Structural Pattern | Simplifies access to a complex subsystem | `BillingFacade`, `SearchFacade` |
| Proxy | Structural Pattern | Controls access to another object | `RemoteUserProxy`, `LazyImageProxy` |
| Formatter | Transformation | Converts a value into a display or textual representation | `DateFormatter`, `CurrencyFormatter` |
| Calculator | Domain / Utility Function Object | Computes a derived value from inputs without owning workflow | `TaxCalculator`, `PricingCalculator` |
| Converter | Transformation | Converts between equivalent representations | `CurrencyConverter`, `MarkdownToHtmlConverter` |
| Parser | Boundary / Transformation | Turns untrusted text or bytes into structured data | `CsvParser`, `JwtParser` |
| Validator | Boundary / Domain Rule | Checks whether input satisfies a rule, often returning errors | `PasswordValidator`, `SchemaValidator` |

## Suffix Contracts

Only use a suffix when the code keeps the contract implied by the suffix:

- `Command` expresses mutation intent and should not perform reads for display.
- `Query` reads and must not mutate state.
- `Handler` should handle one payload type or request shape.
- `Repository` should expose domain persistence semantics, not arbitrary database operations.
- `Service` must be qualified by layer and responsibility; otherwise prefer a more specific noun.
- `Adapter`, `Decorator`, `Facade`, and `Proxy` should match their structural pattern, not just wrap code casually.

## Naming by Capability

Use capability suffixes deliberately:

- `-able` names a capability or property of an object: `Serializable`, `Sortable`.
- `-er` and `-or` name an active agent: `Reader`, `Writer`, `Validator`, `Executor`.
- `-ary` often implies a collection or place: `Dictionary`, `Directory`.

Avoid capability names when the construct is really a domain concept. `InvoiceApprover` may be useful as a role object, but an application action is usually clearer as `ApproveInvoiceUseCase` or `ApproveInvoiceCommandHandler`.
