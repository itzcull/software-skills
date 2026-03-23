---
title: "Circuit Breaker Pattern for Microservices"
description: "Comprehensive guide to implementing circuit breaker patterns for fault tolerance and resilience in distributed systems"
category: "Building Blocks"
tags: ["circuit-breaker", "microservices", "fault-tolerance", "resilience", "design-patterns"]
difficulty: "intermediate"
last_updated: "2025-07-27"
---

# Circuit Breaker Pattern for Microservices

The Circuit Breaker pattern is a crucial design pattern for building resilient microservices. It prevents cascading failures by monitoring for failures and temporarily blocking calls to failing services, allowing them time to recover while protecting the overall system stability.

## What is the Circuit Breaker Pattern?

The Circuit Breaker pattern works like an electrical circuit breaker in your home. When it detects a problem (like too many failures), it "trips" and stops the flow of requests to a failing service, preventing further damage to the system.

### Electrical Circuit Breaker Analogy

```
Normal Operation:
Power Source ──[CLOSED]──► Electrical Device
              Circuit Breaker

Fault Detected:
Power Source ──[OPEN]───X  Electrical Device
              Circuit Breaker
              (Protecting from overload)
```

### Software Circuit Breaker

```
Normal Operation:
Client ──[CLOSED]──► Service
       Circuit Breaker

Service Failing:
Client ──[OPEN]───X  Service (Failing)
       Circuit Breaker
       (Returns fallback response)
```

## Circuit Breaker States

The circuit breaker operates in three distinct states, forming a state machine:

### 1. Closed State (Normal Operation)

All requests pass through to the downstream service. The circuit breaker monitors for failures.

```python
import time
import asyncio
from enum import Enum
from typing import Callable, Any, Optional
from dataclasses import dataclass

class CircuitBreakerState(Enum):
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"

@dataclass
class CircuitBreakerConfig:
    failure_threshold: int = 5          # Number of failures before opening
    success_threshold: int = 3          # Successes needed to close from half-open
    timeout: float = 60.0              # Time to wait before trying half-open
    expected_exception: type = Exception

class CircuitBreaker:
    def __init__(self, config: CircuitBreakerConfig):
        self.config = config
        self.state = CircuitBreakerState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = None
        self.state_change_listeners = []
        
    def add_state_change_listener(self, listener: Callable):
        """Add listener for state changes"""
        self.state_change_listeners.append(listener)
    
    def _notify_state_change(self, old_state: CircuitBreakerState, new_state: CircuitBreakerState):
        """Notify listeners of state changes"""
        for listener in self.state_change_listeners:
            try:
                listener(old_state, new_state, self)
            except Exception as e:
                print(f"State change listener error: {e}")
    
    async def call(self, func: Callable, *args, **kwargs) -> Any:
        """Execute function through circuit breaker"""
        if self.state == CircuitBreakerState.OPEN:
            if self._should_attempt_reset():
                self._move_to_half_open()
            else:
                raise CircuitOpenException("Circuit breaker is OPEN")
        
        try:
            # Execute the function
            result = await self._execute_function(func, *args, **kwargs)
            self._on_success()
            return result
            
        except self.config.expected_exception as e:
            self._on_failure()
            raise e
    
    async def _execute_function(self, func: Callable, *args, **kwargs) -> Any:
        """Execute function, handling both sync and async"""
        if asyncio.iscoroutinefunction(func):
            return await func(*args, **kwargs)
        else:
            return func(*args, **kwargs)
    
    def _should_attempt_reset(self) -> bool:
        """Check if enough time has passed to attempt reset"""
        if self.last_failure_time is None:
            return True
        
        return time.time() - self.last_failure_time >= self.config.timeout
    
    def _on_success(self):
        """Handle successful call"""
        if self.state == CircuitBreakerState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= self.config.success_threshold:
                self._move_to_closed()
        elif self.state == CircuitBreakerState.CLOSED:
            self.failure_count = 0  # Reset failure count on success
    
    def _on_failure(self):
        """Handle failed call"""
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.state == CircuitBreakerState.CLOSED:
            if self.failure_count >= self.config.failure_threshold:
                self._move_to_open()
        elif self.state == CircuitBreakerState.HALF_OPEN:
            self._move_to_open()
    
    def _move_to_open(self):
        """Move to OPEN state"""
        old_state = self.state
        self.state = CircuitBreakerState.OPEN
        self.success_count = 0
        self._notify_state_change(old_state, self.state)
        print(f"Circuit breaker moved to OPEN state after {self.failure_count} failures")
    
    def _move_to_half_open(self):
        """Move to HALF_OPEN state"""
        old_state = self.state
        self.state = CircuitBreakerState.HALF_OPEN
        self.success_count = 0
        self._notify_state_change(old_state, self.state)
        print("Circuit breaker moved to HALF_OPEN state")
    
    def _move_to_closed(self):
        """Move to CLOSED state"""
        old_state = self.state
        self.state = CircuitBreakerState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self._notify_state_change(old_state, self.state)
        print("Circuit breaker moved to CLOSED state")

class CircuitOpenException(Exception):
    """Exception raised when circuit breaker is open"""
    pass
```

### 2. Open State (Failure Protection)

All requests are immediately rejected without calling the downstream service. A fallback response is typically provided.

```python
class CircuitBreakerWithFallback(CircuitBreaker):
    def __init__(self, config: CircuitBreakerConfig, fallback_func: Callable = None):
        super().__init__(config)
        self.fallback_func = fallback_func
        self.metrics = CircuitBreakerMetrics()
    
    async def call(self, func: Callable, *args, **kwargs) -> Any:
        """Execute function with fallback support"""
        try:
            return await super().call(func, *args, **kwargs)
        except CircuitOpenException:
            self.metrics.record_fallback_execution()
            
            if self.fallback_func:
                try:
                    return await self._execute_function(self.fallback_func, *args, **kwargs)
                except Exception as e:
                    self.metrics.record_fallback_failure()
                    raise FallbackFailedException(f"Both primary and fallback failed: {e}")
            else:
                raise ServiceUnavailableException("Service unavailable and no fallback provided")

class FallbackFailedException(Exception):
    pass

class ServiceUnavailableException(Exception):
    pass
```

### 3. Half-Open State (Testing Recovery)

A limited number of requests are allowed through to test if the downstream service has recovered.

```python
class HalfOpenCircuitBreaker(CircuitBreaker):
    def __init__(self, config: CircuitBreakerConfig):
        super().__init__(config)
        self.half_open_max_calls = 3  # Limit concurrent calls in half-open state
        self.half_open_current_calls = 0
        self.half_open_lock = asyncio.Lock()
    
    async def call(self, func: Callable, *args, **kwargs) -> Any:
        """Execute with half-open state limiting"""
        if self.state == CircuitBreakerState.HALF_OPEN:
            async with self.half_open_lock:
                if self.half_open_current_calls >= self.half_open_max_calls:
                    raise CircuitOpenException("Half-open call limit reached")
                
                self.half_open_current_calls += 1
        
        try:
            result = await super().call(func, *args, **kwargs)
            return result
        finally:
            if self.state == CircuitBreakerState.HALF_OPEN:
                async with self.half_open_lock:
                    self.half_open_current_calls -= 1
```

## Advanced Circuit Breaker Implementations

### 1. Time Window-Based Circuit Breaker

Uses sliding time windows to calculate failure rates instead of simple counters.

```python
from collections import deque
import threading

class TimeWindowCircuitBreaker:
    def __init__(self, 
                 failure_rate_threshold: float = 0.5,  # 50% failure rate
                 window_size: int = 60,                # 60 seconds
                 minimum_requests: int = 10,           # Min requests in window
                 open_timeout: int = 60):              # Time before half-open
        self.failure_rate_threshold = failure_rate_threshold
        self.window_size = window_size
        self.minimum_requests = minimum_requests
        self.open_timeout = open_timeout
        
        self.state = CircuitBreakerState.CLOSED
        self.request_log = deque()  # Store (timestamp, success) tuples
        self.last_failure_time = None
        self.lock = threading.Lock()
    
    def _clean_old_requests(self):
        """Remove requests outside the time window"""
        current_time = time.time()
        cutoff_time = current_time - self.window_size
        
        while self.request_log and self.request_log[0][0] < cutoff_time:
            self.request_log.popleft()
    
    def _calculate_failure_rate(self) -> float:
        """Calculate current failure rate"""
        if not self.request_log:
            return 0.0
        
        total_requests = len(self.request_log)
        failed_requests = sum(1 for _, success in self.request_log if not success)
        
        return failed_requests / total_requests if total_requests > 0 else 0.0
    
    async def call(self, func: Callable, *args, **kwargs) -> Any:
        """Execute function with time window analysis"""
        with self.lock:
            self._clean_old_requests()
            
            # Check if circuit should open
            if self.state == CircuitBreakerState.CLOSED:
                if (len(self.request_log) >= self.minimum_requests and
                    self._calculate_failure_rate() >= self.failure_rate_threshold):
                    self.state = CircuitBreakerState.OPEN
                    self.last_failure_time = time.time()
                    print(f"Circuit opened - failure rate: {self._calculate_failure_rate():.2%}")
            
            # Check if circuit should move to half-open
            elif self.state == CircuitBreakerState.OPEN:
                if (self.last_failure_time and 
                    time.time() - self.last_failure_time >= self.open_timeout):
                    self.state = CircuitBreakerState.HALF_OPEN
                    print("Circuit moved to half-open")
        
        # Handle requests based on current state
        if self.state == CircuitBreakerState.OPEN:
            raise CircuitOpenException("Circuit breaker is open")
        
        # Execute the function
        start_time = time.time()
        try:
            result = await self._execute_function(func, *args, **kwargs)
            
            # Record success
            with self.lock:
                self.request_log.append((start_time, True))
                if self.state == CircuitBreakerState.HALF_OPEN:
                    self.state = CircuitBreakerState.CLOSED
                    print("Circuit closed after successful half-open test")
            
            return result
            
        except Exception as e:
            # Record failure
            with self.lock:
                self.request_log.append((start_time, False))
                if self.state == CircuitBreakerState.HALF_OPEN:
                    self.state = CircuitBreakerState.OPEN
                    self.last_failure_time = time.time()
                    print("Circuit reopened after half-open failure")
            
            raise e
```

### 2. Adaptive Circuit Breaker

Dynamically adjusts thresholds based on system behavior and patterns.

```python
class AdaptiveCircuitBreaker:
    def __init__(self, initial_threshold: float = 0.5):
        self.failure_rate_threshold = initial_threshold
        self.min_threshold = 0.1
        self.max_threshold = 0.9
        self.adaptation_factor = 0.1
        
        self.recent_patterns = deque(maxlen=100)  # Store recent behavior
        self.base_circuit_breaker = TimeWindowCircuitBreaker(
            failure_rate_threshold=self.failure_rate_threshold
        )
    
    def _analyze_patterns(self):
        """Analyze recent patterns to adjust threshold"""
        if len(self.recent_patterns) < 20:
            return
        
        # Count recovery attempts and success rates
        recovery_attempts = sum(1 for pattern in self.recent_patterns if pattern['recovery_attempt'])
        successful_recoveries = sum(1 for pattern in self.recent_patterns 
                                  if pattern['recovery_attempt'] and pattern['success'])
        
        if recovery_attempts > 0:
            recovery_rate = successful_recoveries / recovery_attempts
            
            # Adjust threshold based on recovery patterns
            if recovery_rate > 0.8:  # High recovery rate
                # Increase threshold (be more tolerant of failures)
                self.failure_rate_threshold = min(
                    self.max_threshold,
                    self.failure_rate_threshold + self.adaptation_factor
                )
            elif recovery_rate < 0.2:  # Low recovery rate
                # Decrease threshold (be less tolerant of failures)
                self.failure_rate_threshold = max(
                    self.min_threshold,
                    self.failure_rate_threshold - self.adaptation_factor
                )
        
        # Update base circuit breaker
        self.base_circuit_breaker.failure_rate_threshold = self.failure_rate_threshold
    
    async def call(self, func: Callable, *args, **kwargs) -> Any:
        """Execute with adaptive behavior"""
        is_recovery_attempt = self.base_circuit_breaker.state == CircuitBreakerState.HALF_OPEN
        
        try:
            result = await self.base_circuit_breaker.call(func, *args, **kwargs)
            
            # Record successful pattern
            if is_recovery_attempt:
                self.recent_patterns.append({
                    'timestamp': time.time(),
                    'recovery_attempt': True,
                    'success': True
                })
            
            self._analyze_patterns()
            return result
            
        except Exception as e:
            # Record failure pattern
            if is_recovery_attempt:
                self.recent_patterns.append({
                    'timestamp': time.time(),
                    'recovery_attempt': True,
                    'success': False
                })
            
            self._analyze_patterns()
            raise e
```

## Metrics and Monitoring

### 1. Circuit Breaker Metrics Collection

```python
from dataclasses import dataclass
from typing import Dict
import json

@dataclass
class CircuitBreakerMetrics:
    successful_calls: int = 0
    failed_calls: int = 0
    fallback_executions: int = 0
    fallback_failures: int = 0
    state_changes: int = 0
    total_open_time: float = 0.0
    last_state_change: float = 0.0
    
    def record_success(self):
        self.successful_calls += 1
    
    def record_failure(self):
        self.failed_calls += 1
    
    def record_fallback_execution(self):
        self.fallback_executions += 1
    
    def record_fallback_failure(self):
        self.fallback_failures += 1
    
    def record_state_change(self, old_state: CircuitBreakerState, new_state: CircuitBreakerState):
        current_time = time.time()
        
        # Track time spent in OPEN state
        if old_state == CircuitBreakerState.OPEN and self.last_state_change > 0:
            self.total_open_time += current_time - self.last_state_change
        
        self.state_changes += 1
        self.last_state_change = current_time
    
    def get_failure_rate(self) -> float:
        total_calls = self.successful_calls + self.failed_calls
        return self.failed_calls / total_calls if total_calls > 0 else 0.0
    
    def get_fallback_success_rate(self) -> float:
        total_fallbacks = self.fallback_executions
        successful_fallbacks = total_fallbacks - self.fallback_failures
        return successful_fallbacks / total_fallbacks if total_fallbacks > 0 else 0.0
    
    def export_metrics(self) -> Dict:
        return {
            'successful_calls': self.successful_calls,
            'failed_calls': self.failed_calls,
            'failure_rate': self.get_failure_rate(),
            'fallback_executions': self.fallback_executions,
            'fallback_success_rate': self.get_fallback_success_rate(),
            'state_changes': self.state_changes,
            'total_open_time_seconds': self.total_open_time,
            'timestamp': time.time()
        }

class MetricsCollectingCircuitBreaker(CircuitBreaker):
    def __init__(self, config: CircuitBreakerConfig, name: str = "default"):
        super().__init__(config)
        self.name = name
        self.metrics = CircuitBreakerMetrics()
        
        # Register for state changes
        self.add_state_change_listener(self.metrics.record_state_change)
    
    async def call(self, func: Callable, *args, **kwargs) -> Any:
        """Execute with metrics collection"""
        try:
            result = await super().call(func, *args, **kwargs)
            self.metrics.record_success()
            return result
        except Exception as e:
            if isinstance(e, CircuitOpenException):
                # Don't count circuit open as a failure - it's protection
                pass
            else:
                self.metrics.record_failure()
            raise e
    
    def get_health_status(self) -> Dict:
        """Get current health status"""
        return {
            'name': self.name,
            'state': self.state.value,
            'failure_count': self.failure_count,
            'metrics': self.metrics.export_metrics(),
            'healthy': self.state != CircuitBreakerState.OPEN
        }
```

### 2. Dashboard and Alerting

```python
class CircuitBreakerDashboard:
    def __init__(self):
        self.circuit_breakers: Dict[str, MetricsCollectingCircuitBreaker] = {}
        self.alert_thresholds = {
            'failure_rate': 0.2,
            'open_state_duration': 300,  # 5 minutes
            'frequent_state_changes': 10  # per hour
        }
    
    def register_circuit_breaker(self, name: str, circuit_breaker: MetricsCollectingCircuitBreaker):
        """Register a circuit breaker for monitoring"""
        self.circuit_breakers[name] = circuit_breaker
    
    def get_dashboard_data(self) -> Dict:
        """Get data for dashboard display"""
        dashboard_data = {
            'timestamp': time.time(),
            'circuit_breakers': {},
            'overall_health': self._calculate_overall_health()
        }
        
        for name, cb in self.circuit_breakers.items():
            dashboard_data['circuit_breakers'][name] = cb.get_health_status()
        
        return dashboard_data
    
    def _calculate_overall_health(self) -> Dict:
        """Calculate overall system health"""
        total_cbs = len(self.circuit_breakers)
        open_cbs = sum(1 for cb in self.circuit_breakers.values() 
                      if cb.state == CircuitBreakerState.OPEN)
        
        return {
            'total_circuit_breakers': total_cbs,
            'open_circuit_breakers': open_cbs,
            'health_percentage': ((total_cbs - open_cbs) / total_cbs * 100) if total_cbs > 0 else 100
        }
    
    def check_alerts(self) -> List[Dict]:
        """Check for alert conditions"""
        alerts = []
        
        for name, cb in self.circuit_breakers.items():
            metrics = cb.metrics
            
            # High failure rate alert
            if metrics.get_failure_rate() > self.alert_thresholds['failure_rate']:
                alerts.append({
                    'type': 'high_failure_rate',
                    'circuit_breaker': name,
                    'value': metrics.get_failure_rate(),
                    'threshold': self.alert_thresholds['failure_rate'],
                    'severity': 'warning'
                })
            
            # Circuit open too long
            if (cb.state == CircuitBreakerState.OPEN and 
                cb.last_failure_time and
                time.time() - cb.last_failure_time > self.alert_thresholds['open_state_duration']):
                alerts.append({
                    'type': 'circuit_open_too_long',
                    'circuit_breaker': name,
                    'duration': time.time() - cb.last_failure_time,
                    'threshold': self.alert_thresholds['open_state_duration'],
                    'severity': 'critical'
                })
        
        return alerts
```

## Integration Patterns

### 1. HTTP Client with Circuit Breaker

```python
import aiohttp
from typing import Optional

class ResilientHttpClient:
    def __init__(self, base_url: str, circuit_breaker_config: CircuitBreakerConfig):
        self.base_url = base_url.rstrip('/')
        self.circuit_breaker = CircuitBreakerWithFallback(
            config=circuit_breaker_config,
            fallback_func=self._fallback_response
        )
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=10)
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def get(self, path: str, **kwargs) -> Dict:
        """Make GET request through circuit breaker"""
        return await self.circuit_breaker.call(self._make_request, 'GET', path, **kwargs)
    
    async def post(self, path: str, **kwargs) -> Dict:
        """Make POST request through circuit breaker"""
        return await self.circuit_breaker.call(self._make_request, 'POST', path, **kwargs)
    
    async def _make_request(self, method: str, path: str, **kwargs) -> Dict:
        """Make HTTP request"""
        url = f"{self.base_url}{path}"
        
        async with self.session.request(method, url, **kwargs) as response:
            if response.status >= 500:
                raise aiohttp.ClientResponseError(
                    request_info=response.request_info,
                    history=response.history,
                    status=response.status
                )
            
            return await response.json()
    
    async def _fallback_response(self, method: str, path: str, **kwargs) -> Dict:
        """Fallback response when circuit is open"""
        return {
            'error': 'Service temporarily unavailable',
            'fallback': True,
            'path': path,
            'method': method
        }

# Usage example
async def example_usage():
    config = CircuitBreakerConfig(
        failure_threshold=3,
        timeout=30.0,
        expected_exception=aiohttp.ClientError
    )
    
    async with ResilientHttpClient('https://api.example.com', config) as client:
        try:
            response = await client.get('/users/123')
            print(f"Response: {response}")
        except Exception as e:
            print(f"Request failed: {e}")
```

### 2. Database Connection Circuit Breaker

```python
import asyncpg
from typing import Optional

class ResilientDatabaseClient:
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.circuit_breaker = CircuitBreakerWithFallback(
            config=CircuitBreakerConfig(
                failure_threshold=5,
                timeout=60.0,
                expected_exception=(asyncpg.PostgresError, ConnectionError)
            ),
            fallback_func=self._database_fallback
        )
        self.connection_pool: Optional[asyncpg.Pool] = None
    
    async def initialize(self):
        """Initialize connection pool"""
        self.connection_pool = await asyncpg.create_pool(
            self.connection_string,
            min_size=5,
            max_size=20
        )
    
    async def execute_query(self, query: str, *args) -> List[Dict]:
        """Execute query through circuit breaker"""
        return await self.circuit_breaker.call(self._execute_db_query, query, *args)
    
    async def _execute_db_query(self, query: str, *args) -> List[Dict]:
        """Execute database query"""
        async with self.connection_pool.acquire() as connection:
            rows = await connection.fetch(query, *args)
            return [dict(row) for row in rows]
    
    async def _database_fallback(self, query: str, *args) -> List[Dict]:
        """Fallback when database is unavailable"""
        # Could return cached data, empty result, or default values
        print(f"Database unavailable, returning fallback for query: {query}")
        return []

# Usage with automatic retry and backoff
class RetryableCircuitBreaker(CircuitBreaker):
    def __init__(self, config: CircuitBreakerConfig, max_retries: int = 3):
        super().__init__(config)
        self.max_retries = max_retries
    
    async def call_with_retry(self, func: Callable, *args, **kwargs) -> Any:
        """Execute with exponential backoff retry"""
        last_exception = None
        
        for attempt in range(self.max_retries + 1):
            try:
                return await self.call(func, *args, **kwargs)
            except CircuitOpenException:
                # Don't retry if circuit is open
                raise
            except Exception as e:
                last_exception = e
                
                if attempt < self.max_retries:
                    # Exponential backoff
                    delay = (2 ** attempt) * 0.1  # 0.1, 0.2, 0.4 seconds
                    await asyncio.sleep(delay)
                    print(f"Retry attempt {attempt + 1} after {delay}s delay")
        
        raise last_exception
```

### 3. Microservice Communication

```python
class MicroserviceClient:
    def __init__(self, service_name: str, service_url: str):
        self.service_name = service_name
        self.service_url = service_url
        
        # Different circuit breakers for different operations
        self.circuit_breakers = {
            'read': CircuitBreakerWithFallback(
                config=CircuitBreakerConfig(failure_threshold=5, timeout=30.0),
                fallback_func=self._read_fallback
            ),
            'write': CircuitBreakerWithFallback(
                config=CircuitBreakerConfig(failure_threshold=3, timeout=60.0),
                fallback_func=self._write_fallback
            ),
            'critical': CircuitBreakerWithFallback(
                config=CircuitBreakerConfig(failure_threshold=1, timeout=120.0),
                fallback_func=self._critical_fallback
            )
        }
    
    async def get_user(self, user_id: str) -> Dict:
        """Get user data (read operation)"""
        return await self.circuit_breakers['read'].call(
            self._api_call, 'GET', f'/users/{user_id}'
        )
    
    async def update_user(self, user_id: str, data: Dict) -> Dict:
        """Update user data (write operation)"""
        return await self.circuit_breakers['write'].call(
            self._api_call, 'PUT', f'/users/{user_id}', json=data
        )
    
    async def process_payment(self, payment_data: Dict) -> Dict:
        """Process payment (critical operation)"""
        return await self.circuit_breakers['critical'].call(
            self._api_call, 'POST', '/payments', json=payment_data
        )
    
    async def _api_call(self, method: str, path: str, **kwargs) -> Dict:
        """Make API call to microservice"""
        async with aiohttp.ClientSession() as session:
            url = f"{self.service_url}{path}"
            async with session.request(method, url, **kwargs) as response:
                if response.status >= 400:
                    raise aiohttp.ClientResponseError(
                        request_info=response.request_info,
                        history=response.history,
                        status=response.status
                    )
                return await response.json()
    
    async def _read_fallback(self, method: str, path: str, **kwargs) -> Dict:
        """Fallback for read operations - return cached or default data"""
        # Could integrate with cache here
        return {'error': 'Data temporarily unavailable', 'cached': True}
    
    async def _write_fallback(self, method: str, path: str, **kwargs) -> Dict:
        """Fallback for write operations - queue for later processing"""
        # Could queue operation for later retry
        return {'error': 'Write operation queued for retry', 'queued': True}
    
    async def _critical_fallback(self, method: str, path: str, **kwargs) -> Dict:
        """Fallback for critical operations - fail fast"""
        raise ServiceUnavailableException("Critical service unavailable")
```

## Testing Circuit Breakers

### 1. Unit Testing

```python
import pytest
from unittest.mock import AsyncMock

class TestCircuitBreaker:
    @pytest.fixture
    def circuit_breaker(self):
        config = CircuitBreakerConfig(
            failure_threshold=3,
            success_threshold=2,
            timeout=1.0
        )
        return CircuitBreaker(config)
    
    @pytest.mark.asyncio
    async def test_closed_state_allows_calls(self, circuit_breaker):
        """Test that calls pass through in closed state"""
        mock_func = AsyncMock(return_value="success")
        
        result = await circuit_breaker.call(mock_func)
        
        assert result == "success"
        assert circuit_breaker.state == CircuitBreakerState.CLOSED
        mock_func.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_opens_after_threshold_failures(self, circuit_breaker):
        """Test circuit opens after failure threshold"""
        mock_func = AsyncMock(side_effect=Exception("Service error"))
        
        # Trigger failures up to threshold
        for _ in range(3):
            with pytest.raises(Exception):
                await circuit_breaker.call(mock_func)
        
        assert circuit_breaker.state == CircuitBreakerState.OPEN
    
    @pytest.mark.asyncio
    async def test_open_state_rejects_calls(self, circuit_breaker):
        """Test circuit rejects calls when open"""
        # Force circuit to open state
        circuit_breaker.state = CircuitBreakerState.OPEN
        mock_func = AsyncMock()
        
        with pytest.raises(CircuitOpenException):
            await circuit_breaker.call(mock_func)
        
        mock_func.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_half_open_transition(self, circuit_breaker):
        """Test transition to half-open after timeout"""
        # Force circuit to open state with old failure time
        circuit_breaker.state = CircuitBreakerState.OPEN
        circuit_breaker.last_failure_time = time.time() - 2.0  # 2 seconds ago
        
        mock_func = AsyncMock(return_value="success")
        
        result = await circuit_breaker.call(mock_func)
        
        assert result == "success"
        assert circuit_breaker.state == CircuitBreakerState.HALF_OPEN
    
    @pytest.mark.asyncio
    async def test_recovery_to_closed(self, circuit_breaker):
        """Test recovery from half-open to closed"""
        circuit_breaker.state = CircuitBreakerState.HALF_OPEN
        mock_func = AsyncMock(return_value="success")
        
        # Make enough successful calls to close circuit
        for _ in range(2):  # success_threshold = 2
            await circuit_breaker.call(mock_func)
        
        assert circuit_breaker.state == CircuitBreakerState.CLOSED
```

### 2. Chaos Engineering Tests

```python
class ChaosTestingCircuitBreaker:
    def __init__(self, circuit_breaker: CircuitBreaker):
        self.circuit_breaker = circuit_breaker
        self.chaos_scenarios = []
    
    def add_chaos_scenario(self, name: str, failure_rate: float, duration: float):
        """Add a chaos testing scenario"""
        self.chaos_scenarios.append({
            'name': name,
            'failure_rate': failure_rate,
            'duration': duration
        })
    
    async def run_chaos_test(self, service_func: Callable, call_rate: float = 1.0):
        """Run chaos test scenarios"""
        results = {}
        
        for scenario in self.chaos_scenarios:
            print(f"Running chaos scenario: {scenario['name']}")
            
            # Create chaotic service function
            chaotic_func = self._create_chaotic_function(
                service_func, 
                scenario['failure_rate']
            )
            
            # Run test for specified duration
            scenario_results = await self._run_scenario(
                chaotic_func, 
                scenario['duration'], 
                call_rate
            )
            
            results[scenario['name']] = scenario_results
        
        return results
    
    def _create_chaotic_function(self, original_func: Callable, failure_rate: float):
        """Create a function that fails at specified rate"""
        async def chaotic_func(*args, **kwargs):
            if random.random() < failure_rate:
                raise Exception(f"Chaos-induced failure (rate: {failure_rate})")
            return await original_func(*args, **kwargs)
        
        return chaotic_func
    
    async def _run_scenario(self, func: Callable, duration: float, call_rate: float):
        """Run test scenario for specified duration"""
        start_time = time.time()
        results = {
            'total_calls': 0,
            'successful_calls': 0,
            'failed_calls': 0,
            'circuit_open_calls': 0,
            'state_changes': []
        }
        
        # Monitor state changes
        def state_change_listener(old_state, new_state, cb):
            results['state_changes'].append({
                'timestamp': time.time() - start_time,
                'old_state': old_state.value,
                'new_state': new_state.value
            })
        
        self.circuit_breaker.add_state_change_listener(state_change_listener)
        
        # Run calls for specified duration
        while time.time() - start_time < duration:
            results['total_calls'] += 1
            
            try:
                await self.circuit_breaker.call(func)
                results['successful_calls'] += 1
            except CircuitOpenException:
                results['circuit_open_calls'] += 1
            except Exception:
                results['failed_calls'] += 1
            
            await asyncio.sleep(1.0 / call_rate)
        
        return results

# Example chaos test
async def example_chaos_test():
    # Create a mock service
    async def mock_service():
        await asyncio.sleep(0.1)  # Simulate processing time
        return "success"
    
    # Setup circuit breaker
    config = CircuitBreakerConfig(failure_threshold=5, timeout=10.0)
    circuit_breaker = CircuitBreaker(config)
    
    # Create chaos tester
    chaos_tester = ChaosTestingCircuitBreaker(circuit_breaker)
    chaos_tester.add_chaos_scenario("light_failure", 0.1, 30.0)      # 10% failure for 30s
    chaos_tester.add_chaos_scenario("heavy_failure", 0.5, 30.0)      # 50% failure for 30s
    chaos_tester.add_chaos_scenario("total_failure", 1.0, 15.0)      # 100% failure for 15s
    
    # Run chaos tests
    results = await chaos_tester.run_chaos_test(mock_service, call_rate=2.0)
    
    for scenario, result in results.items():
        print(f"\nScenario: {scenario}")
        print(f"Total calls: {result['total_calls']}")
        print(f"Success rate: {result['successful_calls'] / result['total_calls']:.2%}")
        print(f"Circuit protections: {result['circuit_open_calls']}")
        print(f"State changes: {len(result['state_changes'])}")
```

## Best Practices and Common Pitfalls

### 1. Configuration Best Practices

```python
class CircuitBreakerBestPractices:
    @staticmethod
    def calculate_recommended_config(
        service_sla: float,           # Expected service SLA (e.g., 0.99 for 99%)
        avg_response_time: float,     # Average response time in seconds
        request_rate: float,          # Requests per second
        recovery_time: float          # Expected recovery time in seconds
    ) -> CircuitBreakerConfig:
        """Calculate recommended circuit breaker configuration"""
        
        # Failure threshold based on SLA
        expected_failure_rate = 1 - service_sla
        requests_per_timeout = request_rate * (recovery_time / 2)  # Half recovery time
        failure_threshold = max(3, int(requests_per_timeout * expected_failure_rate * 2))
        
        # Timeout based on recovery time
        timeout = max(recovery_time, 30.0)  # Minimum 30 seconds
        
        # Success threshold for half-open state
        success_threshold = max(2, int(failure_threshold / 3))
        
        return CircuitBreakerConfig(
            failure_threshold=failure_threshold,
            success_threshold=success_threshold,
            timeout=timeout
        )
    
    @staticmethod
    def validate_configuration(config: CircuitBreakerConfig) -> List[str]:
        """Validate circuit breaker configuration"""
        warnings = []
        
        if config.failure_threshold < 3:
            warnings.append("Failure threshold too low - may cause frequent trips")
        
        if config.failure_threshold > 20:
            warnings.append("Failure threshold too high - may not protect effectively")
        
        if config.timeout < 10:
            warnings.append("Timeout too short - service may not have time to recover")
        
        if config.timeout > 300:
            warnings.append("Timeout too long - may delay recovery detection")
        
        if config.success_threshold >= config.failure_threshold:
            warnings.append("Success threshold should be less than failure threshold")
        
        return warnings
```

### 2. Common Pitfalls and Solutions

```python
class CircuitBreakerPitfalls:
    """Examples of common pitfalls and their solutions"""
    
    def pitfall_shared_circuit_breaker(self):
        """
        PITFALL: Using single circuit breaker for multiple operations
        This can cause fast operations to be blocked by slow ones
        """
        # BAD: Single circuit breaker for all operations
        bad_circuit_breaker = CircuitBreaker(CircuitBreakerConfig())
        
        async def fast_operation():
            return await bad_circuit_breaker.call(self.quick_api_call)
        
        async def slow_operation():
            return await bad_circuit_breaker.call(self.slow_api_call)
        
        # GOOD: Separate circuit breakers for different operations
        fast_cb = CircuitBreaker(CircuitBreakerConfig(failure_threshold=5, timeout=30))
        slow_cb = CircuitBreaker(CircuitBreakerConfig(failure_threshold=3, timeout=120))
        
        async def fast_operation_fixed():
            return await fast_cb.call(self.quick_api_call)
        
        async def slow_operation_fixed():
            return await slow_cb.call(self.slow_api_call)
    
    def pitfall_no_fallback_strategy(self):
        """
        PITFALL: No fallback when circuit is open
        Users get errors instead of degraded experience
        """
        # BAD: No fallback handling
        async def bad_user_profile_service(user_id: str):
            cb = CircuitBreaker(CircuitBreakerConfig())
            return await cb.call(self.get_user_profile, user_id)  # Throws exception when open
        
        # GOOD: Fallback to cached or default data
        async def good_user_profile_service(user_id: str):
            cb = CircuitBreakerWithFallback(
                config=CircuitBreakerConfig(),
                fallback_func=lambda uid: {'id': uid, 'name': 'Guest', 'cached': True}
            )
            return await cb.call(self.get_user_profile, user_id)
    
    def pitfall_ignoring_circuit_breaker_state(self):
        """
        PITFALL: Not monitoring circuit breaker state
        No visibility into system health
        """
        # BAD: No monitoring
        cb = CircuitBreaker(CircuitBreakerConfig())
        
        # GOOD: Monitor and alert on state changes
        monitored_cb = MetricsCollectingCircuitBreaker(
            config=CircuitBreakerConfig(),
            name="user_service"
        )
        
        def state_change_handler(old_state, new_state, circuit_breaker):
            if new_state == CircuitBreakerState.OPEN:
                self.send_alert(f"Circuit breaker {circuit_breaker.name} opened")
        
        monitored_cb.add_state_change_listener(state_change_handler)
    
    def pitfall_wrong_exception_handling(self):
        """
        PITFALL: Treating all exceptions as failures
        Some exceptions shouldn't trip the circuit breaker
        """
        # BAD: All exceptions count as failures
        bad_config = CircuitBreakerConfig(expected_exception=Exception)
        
        # GOOD: Only specific exceptions count as failures
        good_config = CircuitBreakerConfig(
            expected_exception=(aiohttp.ClientError, TimeoutError)
        )
        
        # Authentication errors shouldn't trip circuit breaker
        class SelectiveCircuitBreaker(CircuitBreaker):
            async def call(self, func: Callable, *args, **kwargs) -> Any:
                try:
                    return await super().call(func, *args, **kwargs)
                except (AuthenticationError, ValidationError):
                    # Don't count these as circuit breaker failures
                    raise
```

### 3. Monitoring and Observability Best Practices

```python
class CircuitBreakerObservability:
    def __init__(self):
        self.metrics_exporters = []
        self.alert_channels = []
    
    def setup_monitoring(self, circuit_breakers: Dict[str, CircuitBreaker]):
        """Setup comprehensive monitoring for circuit breakers"""
        
        # Export metrics to monitoring systems
        for name, cb in circuit_breakers.items():
            self.setup_metrics_export(name, cb)
            self.setup_health_checks(name, cb)
            self.setup_alerting(name, cb)
    
    def setup_metrics_export(self, name: str, cb: CircuitBreaker):
        """Export metrics to monitoring systems (Prometheus, etc.)"""
        def export_metrics():
            if hasattr(cb, 'metrics'):
                metrics = cb.metrics.export_metrics()
                
                # Export to Prometheus-style metrics
                self.export_counter(f'circuit_breaker_calls_total', metrics['successful_calls'], {'name': name, 'result': 'success'})
                self.export_counter(f'circuit_breaker_calls_total', metrics['failed_calls'], {'name': name, 'result': 'failure'})
                self.export_gauge(f'circuit_breaker_state', self._state_to_number(cb.state), {'name': name})
                self.export_gauge(f'circuit_breaker_failure_rate', metrics['failure_rate'], {'name': name})
        
        # Schedule regular metrics export
        asyncio.create_task(self.periodic_export(export_metrics, interval=10.0))
    
    def _state_to_number(self, state: CircuitBreakerState) -> int:
        """Convert state to numeric value for metrics"""
        return {
            CircuitBreakerState.CLOSED: 0,
            CircuitBreakerState.HALF_OPEN: 1,
            CircuitBreakerState.OPEN: 2
        }[state]
    
    async def periodic_export(self, export_func: Callable, interval: float):
        """Periodically export metrics"""
        while True:
            try:
                export_func()
            except Exception as e:
                print(f"Metrics export failed: {e}")
            await asyncio.sleep(interval)
```

## Conclusion

The Circuit Breaker pattern is essential for building resilient microservices architectures. Key takeaways include:

### Design Principles

1. **Fail Fast**: Don't wait for timeouts when a service is known to be down
2. **Provide Fallbacks**: Always have a plan for when services are unavailable
3. **Monitor and Alert**: Visibility into circuit breaker state is crucial
4. **Separate Concerns**: Use different circuit breakers for different operations
5. **Graceful Degradation**: Degrade functionality rather than failing completely

### Implementation Guidelines

1. **Start Simple**: Begin with basic timeout-based circuit breakers
2. **Add Sophistication**: Enhance with time windows and adaptive behavior
3. **Monitor Everything**: Implement comprehensive metrics and alerting
4. **Test Thoroughly**: Use chaos engineering to validate behavior
5. **Document Behavior**: Ensure team understands circuit breaker behavior

### Configuration Considerations

- **Failure Threshold**: Balance between protection and sensitivity
- **Timeout Duration**: Allow sufficient time for service recovery
- **Success Threshold**: Require enough successes to confirm recovery
- **Fallback Strategy**: Always have a plan for circuit open state

### Common Use Cases

- **HTTP API Calls**: Protect against external service failures
- **Database Connections**: Handle database unavailability gracefully
- **Message Queue Operations**: Protect against broker failures
- **Cache Operations**: Handle cache service outages
- **Third-party Integrations**: Protect against partner service issues

The Circuit Breaker pattern, when properly implemented and monitored, provides a robust foundation for building fault-tolerant distributed systems that can handle failures gracefully and recover automatically.