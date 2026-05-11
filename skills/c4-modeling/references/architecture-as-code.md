# Architecture As Code For C4

## Principle

Architecture diagrams are more maintainable when the source of truth is text-based, version-controlled, diffable, and reviewable. Architecture-as-code separates the architectural model from its rendered views, reducing documentation drift.

## Prefer Structurizr DSL

Structurizr DSL is the default choice for durable C4 work because it was designed for the C4 model and supports a shared model with multiple synchronized views.

Use Structurizr DSL when:

- The model will be maintained over time
- Multiple C4 views should stay synchronized
- The output belongs in source control
- The team wants reviewable architecture changes in pull requests
- You need deployment views, dynamic views, styling, or workspace-level reuse

Structurizr DSL separates:

- `model`: people, systems, containers, components, deployment nodes, and relationships
- `views`: system landscape, system context, container, component, dynamic, deployment, styles, and themes

## Structurizr DSL Skeleton

```structurizr
workspace "Example" "C4 model for Example" {
  model {
    user = person "Customer" "Places and tracks orders"

    softwareSystem = softwareSystem "Ordering Platform" "Allows customers to place orders" {
      webApp = container "Customer Web App" "Provides ordering UI" "React SPA"
      api = container "Orders API" "Handles order lifecycle" "Kotlin/Spring Boot"
      database = container "Orders Database" "Stores orders" "PostgreSQL"
    }

    paymentGateway = softwareSystem "Payment Gateway" "Processes card payments"

    user -> webApp "Places orders using" "HTTPS"
    webApp -> api "Submits orders to" "HTTPS/JSON"
    api -> database "Reads and writes orders in" "JDBC"
    api -> paymentGateway "Authorizes payments using" "HTTPS/JSON"
  }

  views {
    systemContext softwareSystem "SystemContext" {
      include *
      autoLayout lr
    }

    container softwareSystem "Containers" {
      include *
      autoLayout lr
    }
  }
}
```

## Mermaid And PlantUML

Mermaid and PlantUML are useful when diagrams must live directly inside Markdown or documentation platforms with built-in rendering.

Use Mermaid when:

- The diagram is small
- The documentation host renders Mermaid natively
- The user needs fast Markdown embedding
- Long-term synchronized model reuse is not required

Use PlantUML when:

- The team already uses PlantUML
- Existing C4-PlantUML conventions are in place
- More mature diagram rendering options are needed than Mermaid provides

Tradeoff: Mermaid and PlantUML can express C4-style diagrams, but they usually do not provide the same model/view separation as Structurizr DSL.

## File Placement

Prefer existing repository conventions. If none exist, reasonable defaults are:

- `docs/architecture/workspace.dsl`
- `docs/architecture/c4/workspace.dsl`
- `docs/architecture/context.md`
- `docs/architecture/containers.md`

Keep generated image files out of source control unless the repository already commits rendered artifacts.

## Maintenance Rules

- Treat the DSL as the source of truth.
- Review model changes in pull requests.
- Keep names aligned with deployed services, repositories, and domain language.
- Prefer one workspace per bounded system or product area unless an enterprise landscape is required.
- Link diagrams from ADRs instead of duplicating architectural rationale inside diagram files.
- Regenerate rendered diagrams after structural changes when the project commits generated output.

## Architecture-As-Code Review

Check that:

- The model has one authoritative representation of each element.
- Views include only elements needed for their purpose.
- Relationships are defined once and reused across views.
- Styles or themes do not encode unstated semantics.
- View keys and names are stable enough for documentation links.
- The DSL can be rendered by the intended tool without manual correction.
