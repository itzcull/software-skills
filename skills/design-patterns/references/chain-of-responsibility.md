# Chain of Responsibility Pattern

## Overview

The Chain of Responsibility pattern is a behavioral design pattern that allows passing requests along a chain of handlers. Each handler decides either to process the request or pass it to the next handler in the chain.

## Key Components

1. **Request**: Contains the information to be processed by the chain of handlers
2. **Abstract Handler**: Includes methods to:
   - Set the next handler in the chain
   - Process requests
3. **Handler**: Specific implementation of the abstract handler that can:
   - Handle a specific type of request
   - Pass the request to the next handler

## Benefits

- **Decoupling**: Sender of request is not aware of specific handlers
- **Reusability**: Handlers can be reused in different chains
- **Dynamic Handling**: Requests can be processed differently based on runtime context
- **Error Handling**: Centralized mechanism for handling errors and exceptions

## Common Applications

- Authentication
- Event Handling
- Workflow Processing
- Authorization
- Cross-cutting Concerns

## .NET Examples

### ASP.NET Core Middleware
Middleware handlers are configured in `Program.cs` and processed in the order they are added.

### MediatR Pipeline Behaviors
Implements Chain of Responsibility through pipelines that intercept and potentially modify requests before handling.

### ChainedTokenCredential
Allows configuring multiple token credential types to be checked in a specific order:

```typescript
interface TokenCredential {
    getToken(): Promise<string | null>;
}

class AzureCliCredential implements TokenCredential {
    public async getToken(): Promise<string | null> {
        // Implementation for Azure CLI credential
        return null;
    }
}

class ManagedIdentityCredential implements TokenCredential {
    public async getToken(): Promise<string | null> {
        // Implementation for managed identity credential
        return null;
    }
}

class ChainedTokenCredential implements TokenCredential {
    private credentials: TokenCredential[];

    constructor(...credentials: TokenCredential[]) {
        this.credentials = credentials;
    }

    public async getToken(): Promise<string | null> {
        for (const credential of this.credentials) {
            const token = await credential.getToken();
            if (token) {
                return token;
            }
        }
        return null;
    }
}

class CosmosHelper {
    private client: CosmosClient;

    constructor() {
        const credential = new ChainedTokenCredential(
            new AzureCliCredential(),
            new ManagedIdentityCredential()
        );
        
        this.client = new CosmosClient({
            accountEndpoint: this.cosmosUri,
            tokenCredential: credential
        });
    }
}
```

## When to Use

Use the Chain of Responsibility pattern when:
- You want to decouple request senders from their processors
- Multiple objects can handle a request
- The handler is not known a priori
- The set of handlers should be dynamically configurable

## Related Patterns

- [Mediator Pattern](mediator.md)
- Decorator Pattern
- Pipeline Pattern