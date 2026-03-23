# Domain Model in DDD

A domain model is a conceptual representation of core concepts, entities, and relationships within a specific domain. It serves as a shared understanding between domain experts and developers, facilitating communication and collaboration.

## Domain Modeling

Domain modeling evolves through two phases:
1. Strategic Design
2. Tactical Design

Strategic design builds the conceptual blueprint through conversations, while tactical design implements the details.

## Sample Domain Model: Library Management System

### Strategic Phase

Discovered entities:
- Book
- Author
- Member

Relationships:
- A book can have many authors
- An author can write many books
- A member can checkout many books
- A book can be borrowed by many members

Ubiquitous language terms:
- Borrow
- Return
- Reserve
- Loan
- Overdue

Potential Bounded Contexts:
- Catalog management
- Member management
- Inventory management

### Tactical Phase

Example TypeScript implementation:

```typescript
// Book (Catalog Management)
class Book extends EntityBase {
    constructor(
        private readonly title: string,
        private readonly author: Author,
        private readonly isbn: ISBN,
        private readonly publicationDate: Date
    ) {
        super();
    }

    public get getTitle(): string {
        return this.title;
    }

    public get getAuthor(): Author {
        return this.author;
    }

    public get getISBN(): ISBN {
        return this.isbn;
    }

    public get getPublicationDate(): Date {
        return this.publicationDate;
    }
}

// Loan (Loan Management)
class Loan implements IAggregateRoot {
    constructor(
        private readonly book: Book,
        private readonly member: Member,
        private readonly borrowedDate: Date,
        private returnedDate?: Date
    ) {}

    public get getBook(): Book {
        return this.book;
    }

    public get getMember(): Member {
        return this.member;
    }

    public get getBorrowedDate(): Date {
        return this.borrowedDate;
    }

    public get getReturnedDate(): Date | undefined {
        return this.returnedDate;
    }
}
```

## Learn More

- [On-Demand Webinar: Intro to Domain-Driven Design with C#](https://mailchi.mp/nimblepros/af2112un73)
- [Email Course: Intro to DDD](https://mailchi.mp/nimblepros/intro-to-ddd-email-course)