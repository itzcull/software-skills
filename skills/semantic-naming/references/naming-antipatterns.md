# Naming Antipatterns

Vague names are usually design feedback. They often mean the construct has unclear boundaries, too many responsibilities, or a missing domain concept.

## Manager

`Manager` usually means "does miscellaneous things related to this noun." It invites unrelated behavior and often grows into a god object.

Avoid:

```text
UserManager
ConnectionManager
PaymentManager
```

Prefer a name that states the actual responsibility:

| If it actually... | Prefer |
|---|---|
| Creates objects | `Factory`, `Builder` |
| Coordinates a workflow | `Coordinator`, `Orchestrator` |
| Tracks long-running workflow state | `ProcessManager` |
| Stores and retrieves aggregates | `Repository` |
| Controls access to another object | `Proxy` |
| Owns lifecycle of pooled resources | `Pool`, `Registry`, `Cache` |
| Executes one payload | `Handler` |
| Applies a domain decision | `Policy`, `Specification` |

Narrow exception: `Manager` may be acceptable where the term is a framework or domain-standard role, or for a small localized UI/resource lifecycle object such as `FontManager`. Even then, prefer a more precise name when available.

## Helper and Util

`Helper` and `Util` usually collect stateless procedures that did not find a proper home. They make code harder to discover and easier to couple globally.

Avoid:

```text
DateUtil
StringHelper
PaymentHelper
```

Prefer:

| If it actually... | Prefer |
|---|---|
| Formats values | `Formatter` |
| Parses text or bytes | `Parser` |
| Converts representations | `Converter` |
| Calculates derived values | `Calculator` |
| Validates inputs | `Validator` |
| Generates identifiers or values | `Generator` |
| Encodes or decodes values | `Encoder`, `Decoder`, `Codec` |
| Normalizes values | `Normalizer` |

If the operation belongs to a domain concept, move the behavior there rather than creating a utility class.

## Logic and Process

`Logic` and `Process` are usually tautologies. Most code contains logic and participates in a process.

Avoid:

```text
UserLogic
PaymentProcess
OrderProcessingLogic
```

Prefer names that identify the domain action or architectural role:

```text
RegisterUserUseCase
CapturePaymentCommandHandler
OrderFulfillmentProcessManager
PaymentPolicy
```

Use `ProcessManager` only for a stateful workflow orchestrator. Do not use `Process` as a generic suffix for any multi-step method.

## Processor

`Processor` is often too broad. It can be acceptable for a component that consumes a stream or queue of work items, but it should not hide the type of work being done.

Avoid:

```text
DataProcessor
UserProcessor
MessageProcessor
```

Prefer:

| If it actually... | Prefer |
|---|---|
| Handles one command or event | `Handler` |
| Executes scheduled work | `Job`, `Worker` |
| Parses input | `Parser` |
| Transforms data | `Transformer`, `Mapper`, `Converter` |
| Runs a pipeline step | `PipelineStep`, or a domain-specific step name |
| Consumes messages continuously | `Consumer` |

`InvoiceBatchProcessor` can be acceptable if it explicitly consumes invoice batches and the surrounding code uses processor terminology consistently.

## Data and Info

`Data` and `Info` can be appropriate for passive carriers, but they are often too vague.

Avoid:

```text
UserData
ConnectionInfo
ResultData
```

Prefer:

| If it crosses a boundary | Prefer |
|---|---|
| API request | `Request`, `RequestDto` |
| API response | `Response`, `ResponseDto` |
| Query result | `Result`, `QueryResult` |
| Persistence shape | `Record`, `Row`, `Document` |
| Domain value | A Value Object name such as `EmailAddress` |

`Info` is acceptable only when the main distinction is explicitly "information about X, not behavior for X" and there is no more precise carrier role.

## Wrapper

`Wrapper` describes structure but not purpose. Most wrappers are actually established structural patterns.

Avoid:

```text
HttpClientWrapper
RetryWrapper
UserWrapper
```

Prefer:

| If it actually... | Prefer |
|---|---|
| Adapts an interface | `Adapter` |
| Adds behavior around another object | `Decorator` |
| Simplifies a subsystem | `Facade` |
| Controls access | `Proxy` |
| Owns framework integration | `Gateway`, `Provider`, `Client` |

Use `Wrapper` only when the project has no stronger semantic distinction and the construct truly does nothing beyond wrapping a primitive or foreign object.

## Type-Encoding Names

Do not encode obvious language types when the semantic role is what matters.

Avoid:

```text
userArray
nameString
invoiceObject
callbackFunction
```

Prefer:

```text
users
displayName
invoice
onInvoiceApproved
```

Type names are useful when they distinguish domain representations, such as `InvoiceRow`, `InvoiceDto`, and `Invoice`.

## Misleading Verb-Noun Order

Use word order to distinguish action from result.

| Active action | Passive artifact |
|---|---|
| `ReportSecurityFlawCommand` | `SecurityFlawReport` |
| `ApproveInvoiceCommand` | `InvoiceApproval` |
| `RegisterUserUseCase` | `UserRegistrationResult` |

If a construct performs work, lead with the action. If it stores or describes the result of work, lead with the domain object.

## Eponymous and Whimsical Names

Names based on people, jokes, animals, or project lore are hard for new readers to interpret.

Avoid names like `ZuseMethod`, `Pig`, or `Flink` for internal concepts when a descriptive term exists.

Prefer names that reveal the underlying idea, such as `BreadthFirstSearch`, `StreamProcessor`, or `FalsePositive`.

Public product or library names may have branding reasons to be memorable, but internal constructs should optimize for comprehension.
