# REPR Design Pattern

## Overview

The REPR (Request-Endpoint-Response) Design Pattern is a simplified approach to web API endpoint design that focuses on three key components:

- Request
- Endpoint
- Response

### Key Characteristics

- Simplifies the traditional MVC pattern
- More focused on API development
- Eliminates unnecessary components like Views and bloated Controllers
- Provides a clean, focused approach to defining API endpoints

## Core Concept

"The REPR pattern defines web API endpoints as having three components: a Request, an Endpoint, and a Response."

### Differences from MVC

- No View component
- No multi-action Controllers
- Endpoints are designed as individual classes
- Each endpoint has a single `Handle` method

## Structure

An REPR endpoint typically consists of:
- An optional Request type
- An Endpoint class with a `Handle` method
- An optional Response type

## Flexibility

- Not strictly a REST pattern
- Can be used for RESTful or RPC-style endpoints
- Allows flexibility in implementing business logic

## Example Scenario

For a `Customer` resource, you might have:
- `GetCustomerRequest`
- `GetCustomerEndpoint`
- `GetCustomerResponse`

## When to Use

- API-focused applications
- When you want to simplify endpoint design
- To reduce complexity in web service architecture

## References

- [Ardalis.ApiEndpoints NuGet Package](https://www.nuget.org/packages/Ardalis.ApiEndpoints/)
- [MVC Controllers are Dinosaurs article](https://ardalis.com/mvc-controllers-are-dinosaurs-embrace-api-endpoints/)

## Related Tools

- [MediatR](https://github.com/jbogard/MediatR)
- [AutoMapper](https://automapper.org/)
- [FastEndpoints](https://fast-endpoints.com/)