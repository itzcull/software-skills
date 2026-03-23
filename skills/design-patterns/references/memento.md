# Memento Pattern

## Overview

The Memento pattern is a behavioral design pattern that allows capturing and externalizing an object's internal state without violating [encapsulation](../principles/encapsulation.md), enabling state restoration later.

## Intent

"Capture and externalize an object's internal state so that the object can be restored to this state later, without violating encapsulation."

## Key Characteristics

- Also known as the "Token pattern"
- Part of the Gang of Four design patterns
- Enables undo/redo functionality
- Preserves object state without breaking encapsulation

## When to Use

The Memento pattern is best suited for scenarios such as:
- Implementing undo/redo in editor applications
- Rolling back objects to previous states
- Providing state restoration without compromising encapsulation

## Structure

The pattern involves three primary classes:

1. **Memento**: Stores the internal state
   - Holds `state`
   - Provides `GetState()` and `SetState()` methods

2. **Originator**: The object whose state needs preservation
   - Contains the current `state`
   - Creates mementos via `CreateMemento()`
   - Restores state using `SetMemento()`

3. **Caretaker**: Manages and tracks mementos
   - Keeps a list of mementos
   - Does not directly manipulate memento contents

## Sample Code (TypeScript)

```typescript
class Originator {
    private _state: string = '';
    
    public get state(): string {
        return this._state;
    }
    
    public set state(value: string) {
        this._state = value;
        console.log(`State set to: ${this._state}`);
    }

    public createMemento(): Memento {
        return new Memento(this._state);
    }

    public setMemento(memento: Memento): void {
        this._state = memento.state;
        console.log(`State restored to: ${this._state}`);
    }
}

class Memento {
    public readonly state: string;
    
    constructor(state: string) {
        this.state = state;
    }
}

class Caretaker {
    private mementos: Memento[] = [];
    
    public addMemento(memento: Memento): void {
        this.mementos.push(memento);
    }
    
    public getMemento(index: number): Memento {
        return this.mementos[index];
    }
}
```