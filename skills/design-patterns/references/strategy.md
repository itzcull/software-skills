# Strategy Design Pattern

## Intent

"Define a family of algorithms, encapsulate each one, and make them interchangeable. Strategy lets the algorithm vary independently from clients that use it."

## Overview

The Strategy Design Pattern allows an object to have some or all of its behavior defined through another object following a particular interface. A specific interface implementation is provided to the client when instantiated, defining the concrete behavior to be used.

## Structure

![Strategy Pattern UML](/static/969d3a2f16711b34389b844f5e9ca8a6/6f3f2/Strategy_Pattern_in_UML.png)

The pattern typically involves:
- An interface or abstract base class defining the "algorithm"
- Specific implementations of this interface
- Extraction of tightly coupled code into interface implementations

## Example

```typescript
interface Movie {
    id: number;
    title: string;
    genre: string;
}

interface IMovieRepository {
    listGenres(): string[];
    listMovies(movieGenre?: string, searchString?: string): Movie[];
}

class EfMovieRepository implements IMovieRepository {
    private readonly db = new MovieDbContext();

    public listGenres(): string[] {
        // Implementation details...
        return this.db.movies.map(m => m.genre).filter((genre, index, self) => self.indexOf(genre) === index);
    }

    public listMovies(movieGenre?: string, searchString?: string): Movie[] {
        // Implementation details...
        let movies = this.db.movies;
        
        if (movieGenre) {
            movies = movies.filter(m => m.genre === movieGenre);
        }
        
        if (searchString) {
            movies = movies.filter(m => m.title.toLowerCase().includes(searchString.toLowerCase()));
        }
        
        return movies;
    }
}

class MoviesController {
    private readonly movieRepository: IMovieRepository;

    constructor(movieRepository?: IMovieRepository) {
        this.movieRepository = movieRepository || new EfMovieRepository();
    }

    public index(movieGenre?: string, searchString?: string): { genres: string[], movies: Movie[] } {
        return {
            genres: this.movieRepository.listGenres(),
            movies: this.movieRepository.listMovies(movieGenre, searchString)
        };
    }
}
```

## Key Principles Supported

- [Single Responsibility Principle](../principles/single-responsibility.md)
- [Explicit Dependencies Principle](../principles/explicit-dependencies.md)
- [Dependency Inversion Principle](../principles/dependency-inversion.md)

## References

- [Design Patterns: Elements of Reusable Object-Oriented Software](http://amzn.to/vep3BT)
- [Design