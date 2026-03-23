---
title: Rate Limiting Algorithms
description: Understanding different rate limiting algorithms including Token Bucket, Leaky Bucket, Fixed Window, and Sliding Window approaches with implementation examples
source: https://blog.algomaster.io/p/rate-limiting-algorithms-explained-with-code
tags: [rate-limiting, algorithms, api-design, throttling, token-bucket, leaky-bucket, sliding-window, traffic-control]
category: key-concepts
---

# Rate Limiting Algorithms

## Definition

> Rate limiting is a technique used to control the rate of requests sent or received by a network interface controller and is used to prevent abuse and ensure fair usage of resources.

Rate limiting is essential for protecting systems from abuse, ensuring fair resource allocation, and maintaining system stability under high load. Different algorithms offer various trade-offs between accuracy, memory usage, and implementation complexity.

## Why Rate Limiting is Important

### System Protection
- **Prevent DDoS attacks**: Limit malicious traffic before it overwhelms servers
- **Resource conservation**: Protect CPU, memory, and bandwidth from overuse
- **Database protection**: Prevent query overload and connection exhaustion

### Fair Usage
- **Equal access**: Ensure all users get fair share of resources
- **Prevent monopolization**: Stop single users from consuming all capacity
- **Service quality**: Maintain response times for all users

### Business Requirements
- **API monetization**: Enforce usage tiers and pricing plans
- **SLA compliance**: Meet guaranteed service levels
- **Cost control**: Manage infrastructure costs by controlling usage

## Rate Limiting Algorithms

### 1. Token Bucket Algorithm

**Concept**: A bucket holds tokens that are added at a fixed rate. Each request consumes a token. When tokens are available, requests are allowed; when the bucket is empty, requests are rejected or delayed.

#### How It Works

1. **Bucket Initialization**: Create bucket with maximum capacity and initial token count
2. **Token Refill**: Add tokens at a constant rate (refill rate)
3. **Request Processing**: Each request consumes one token
4. **Decision Logic**: Allow request if tokens available, otherwise reject

#### Implementation

```python
import time
import threading
from typing import Optional

class TokenBucket:
    def __init__(self, capacity: int, refill_rate: float):
        """
        Initialize Token Bucket
        
        Args:
            capacity: Maximum number of tokens in bucket
            refill_rate: Tokens added per second
        """
        self.capacity = capacity
        self.tokens = capacity
        self.refill_rate = refill_rate
        self.last_refill = time.time()
        self.lock = threading.Lock()
    
    def _refill(self):
        """Add tokens based on elapsed time"""
        now = time.time()
        elapsed = now - self.last_refill
        tokens_to_add = elapsed * self.refill_rate
        
        self.tokens = min(self.capacity, self.tokens + tokens_to_add)
        self.last_refill = now
    
    def consume(self, tokens: int = 1) -> bool:
        """
        Try to consume tokens from bucket
        
        Args:
            tokens: Number of tokens to consume
            
        Returns:
            True if tokens consumed successfully, False otherwise
        """
        with self.lock:
            self._refill()
            
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False
    
    def peek(self) -> float:
        """Get current token count without consuming"""
        with self.lock:
            self._refill()
            return self.tokens

# Usage example
bucket = TokenBucket(capacity=10, refill_rate=1.0)  # 10 tokens max, 1 token/second

def handle_request(request_id: str) -> str:
    if bucket.consume():
        return f"Request {request_id} processed"
    else:
        return f"Request {request_id} rate limited"

# Simulate requests
for i in range(15):
    print(handle_request(f"req_{i}"))
    time.sleep(0.1)
```

#### Advanced Token Bucket with Different Token Costs

```python
class WeightedTokenBucket(TokenBucket):
    def __init__(self, capacity: int, refill_rate: float, request_costs: dict):
        super().__init__(capacity, refill_rate)
        self.request_costs = request_costs
    
    def handle_request(self, request_type: str) -> bool:
        """Handle request with type-specific token cost"""
        cost = self.request_costs.get(request_type, 1)
        return self.consume(cost)

# Example: Different API endpoints have different costs
api_bucket = WeightedTokenBucket(
    capacity=100,
    refill_rate=10.0,
    request_costs={
        'GET': 1,
        'POST': 2,
        'DELETE': 3,
        'BULK_OPERATION': 10
    }
)

# Heavy operations consume more tokens
print(api_bucket.handle_request('GET'))        # Consumes 1 token
print(api_bucket.handle_request('BULK_OPERATION'))  # Consumes 10 tokens
```

#### Pros and Cons

**Pros:**
- Simple to implement and understand
- Allows burst traffic up to bucket capacity
- Self-regulating (bucket refills automatically)
- Good for APIs that need to handle occasional spikes

**Cons:**
- Memory usage scales with number of users
- Doesn't guarantee perfectly smooth rate
- Burst allowance might not be desirable for all use cases

### 2. Leaky Bucket Algorithm

**Concept**: Requests enter a bucket that has a small hole at the bottom. The bucket processes requests at a constant rate. If the bucket is full, new requests overflow and are discarded.

#### How It Works

1. **Bucket Setup**: Create bucket with fixed capacity
2. **Request Queuing**: Incoming requests are added to bucket queue
3. **Constant Processing**: Process requests at fixed rate regardless of arrival rate
4. **Overflow Handling**: Reject requests when bucket is full

#### Implementation

```python
import time
import threading
from collections import deque
from typing import Any, Optional, Callable

class LeakyBucket:
    def __init__(self, capacity: int, leak_rate: float):
        """
        Initialize Leaky Bucket
        
        Args:
            capacity: Maximum requests bucket can hold
            leak_rate: Requests processed per second
        """
        self.capacity = capacity
        self.leak_rate = leak_rate
        self.queue = deque()
        self.last_leak = time.time()
        self.lock = threading.Lock()
        self.processing = False
    
    def add_request(self, request: Any) -> bool:
        """
        Add request to bucket
        
        Args:
            request: Request object to process
            
        Returns:
            True if request added, False if bucket is full
        """
        with self.lock:
            if len(self.queue) >= self.capacity:
                return False  # Bucket overflow
            
            self.queue.append(request)
            
            # Start processing if not already running
            if not self.processing:
                self._start_processing()
            
            return True
    
    def _start_processing(self):
        """Start processing requests at leak rate"""
        self.processing = True
        threading.Thread(target=self._process_requests, daemon=True).start()
    
    def _process_requests(self):
        """Process requests at constant rate"""
        while True:
            with self.lock:
                if not self.queue:
                    self.processing = False
                    break
                
                # Calculate how many requests to process
                now = time.time()
                elapsed = now - self.last_leak
                requests_to_process = int(elapsed * self.leak_rate)
                
                if requests_to_process > 0:
                    # Process requests
                    for _ in range(min(requests_to_process, len(self.queue))):
                        request = self.queue.popleft()
                        self._handle_request(request)
                    
                    self.last_leak = now
            
            # Sleep to maintain leak rate
            time.sleep(1.0 / self.leak_rate)
    
    def _handle_request(self, request):
        """Override this method to define request processing logic"""
        print(f"Processing request: {request}")

# Usage example
class APILeakyBucket(LeakyBucket):
    def _handle_request(self, request):
        """Process API request"""
        request_id, endpoint = request
        print(f"Processing API request {request_id} to {endpoint}")
        # Simulate processing time
        time.sleep(0.1)

# Create bucket that processes 5 requests per second
api_bucket = APILeakyBucket(capacity=20, leak_rate=5.0)

# Simulate burst of requests
requests = [(f"req_{i}", "/api/users") for i in range(25)]

accepted = 0
rejected = 0

for request in requests:
    if api_bucket.add_request(request):
        accepted += 1
    else:
        rejected += 1

print(f"Accepted: {accepted}, Rejected: {rejected}")
```

#### Leaky Bucket with Backpressure

```python
class BackpressureLeakyBucket(LeakyBucket):
    def __init__(self, capacity: int, leak_rate: float, backpressure_callback: Callable):
        super().__init__(capacity, leak_rate)
        self.backpressure_callback = backpressure_callback
    
    def add_request(self, request: Any) -> bool:
        """Add request with backpressure signaling"""
        added = super().add_request(request)
        
        if not added:
            # Signal backpressure to upstream
            self.backpressure_callback(request)
        
        return added

def handle_backpressure(request):
    """Handle rejected requests"""
    print(f"Request {request} rejected - signaling upstream to slow down")

# Bucket with backpressure handling
bp_bucket = BackpressureLeakyBucket(
    capacity=10,
    leak_rate=2.0,
    backpressure_callback=handle_backpressure
)
```

#### Pros and Cons

**Pros:**
- Provides smooth, constant output rate
- Good for protecting downstream systems
- Prevents sudden traffic spikes from reaching backend
- Natural backpressure mechanism

**Cons:**
- More complex implementation than token bucket
- Can introduce latency for bursty traffic
- Fixed processing rate may underutilize capacity during low traffic

### 3. Fixed Window Counter Algorithm

**Concept**: Divide time into fixed windows and count requests in each window. Reset the counter at the beginning of each new window.

#### How It Works

1. **Window Definition**: Define fixed time windows (e.g., 1 minute)
2. **Request Counting**: Count requests within current window
3. **Limit Enforcement**: Reject requests if window limit exceeded
4. **Window Reset**: Reset counter at window boundary

#### Implementation

```python
import time
import threading
from collections import defaultdict

class FixedWindowCounter:
    def __init__(self, window_size: int, max_requests: int):
        """
        Initialize Fixed Window Counter
        
        Args:
            window_size: Window size in seconds
            max_requests: Maximum requests per window
        """
        self.window_size = window_size
        self.max_requests = max_requests
        self.counters = defaultdict(int)  # window_start -> count
        self.lock = threading.Lock()
    
    def _get_current_window(self) -> int:
        """Get current window start time"""
        return int(time.time() // self.window_size) * self.window_size
    
    def _cleanup_old_windows(self, current_window: int):
        """Remove old window data to prevent memory leaks"""
        cutoff = current_window - self.window_size
        old_windows = [w for w in self.counters.keys() if w < cutoff]
        for window in old_windows:
            del self.counters[window]
    
    def is_allowed(self, identifier: str = "default") -> bool:
        """
        Check if request is allowed
        
        Args:
            identifier: User/IP identifier for per-user limiting
            
        Returns:
            True if request allowed, False otherwise
        """
        with self.lock:
            current_window = self._get_current_window()
            window_key = f"{identifier}:{current_window}"
            
            # Cleanup old windows
            self._cleanup_old_windows(current_window)
            
            # Check if limit exceeded
            if self.counters[window_key] >= self.max_requests:
                return False
            
            # Increment counter
            self.counters[window_key] += 1
            return True
    
    def get_remaining_requests(self, identifier: str = "default") -> int:
        """Get remaining requests for current window"""
        with self.lock:
            current_window = self._get_current_window()
            window_key = f"{identifier}:{current_window}"
            used = self.counters.get(window_key, 0)
            return max(0, self.max_requests - used)
    
    def get_reset_time(self) -> int:
        """Get timestamp when current window resets"""
        current_window = self._get_current_window()
        return current_window + self.window_size

# Usage example
rate_limiter = FixedWindowCounter(window_size=60, max_requests=100)  # 100 requests per minute

def handle_api_request(user_id: str, endpoint: str) -> dict:
    """Handle API request with rate limiting"""
    if rate_limiter.is_allowed(user_id):
        remaining = rate_limiter.get_remaining_requests(user_id)
        reset_time = rate_limiter.get_reset_time()
        
        return {
            'status': 'success',
            'data': f'Response for {endpoint}',
            'rate_limit': {
                'remaining': remaining,
                'reset': reset_time
            }
        }
    else:
        reset_time = rate_limiter.get_reset_time()
        return {
            'status': 'rate_limited',
            'error': 'Rate limit exceeded',
            'rate_limit': {
                'remaining': 0,
                'reset': reset_time
            }
        }

# Simulate API requests
for i in range(105):
    response = handle_api_request("user123", "/api/data")
    if response['status'] == 'rate_limited':
        print(f"Request {i}: Rate limited, reset at {response['rate_limit']['reset']}")
        break
    else:
        print(f"Request {i}: Success, {response['rate_limit']['remaining']} remaining")
```

#### Pros and Cons

**Pros:**
- Simple to understand and implement
- Memory efficient
- Clear rate limit semantics
- Good performance characteristics

**Cons:**
- **Window boundary issue**: Can allow double the rate at window boundaries
- Not as smooth as other algorithms
- Potential for abuse near window transitions

### 4. Sliding Window Log Algorithm

**Concept**: Maintain a log of request timestamps and remove entries older than the window size. Allow requests if the count of recent requests is below the limit.

#### How It Works

1. **Timestamp Logging**: Record timestamp for each request
2. **Window Sliding**: Remove timestamps older than window size
3. **Count Checking**: Count remaining timestamps
4. **Decision Making**: Allow if count is below limit

#### Implementation

```python
import time
import threading
from collections import defaultdict, deque
from typing import List

class SlidingWindowLog:
    def __init__(self, window_size: int, max_requests: int):
        """
        Initialize Sliding Window Log
        
        Args:
            window_size: Window size in seconds
            max_requests: Maximum requests per window
        """
        self.window_size = window_size
        self.max_requests = max_requests
        self.request_logs = defaultdict(deque)  # identifier -> deque of timestamps
        self.lock = threading.Lock()
    
    def _clean_old_requests(self, log: deque, current_time: float):
        """Remove requests older than window size"""
        cutoff_time = current_time - self.window_size
        
        while log and log[0] <= cutoff_time:
            log.popleft()
    
    def is_allowed(self, identifier: str = "default") -> bool:
        """
        Check if request is allowed
        
        Args:
            identifier: User/IP identifier
            
        Returns:
            True if request allowed, False otherwise
        """
        with self.lock:
            current_time = time.time()
            log = self.request_logs[identifier]
            
            # Clean old requests
            self._clean_old_requests(log, current_time)
            
            # Check if limit would be exceeded
            if len(log) >= self.max_requests:
                return False
            
            # Add current request timestamp
            log.append(current_time)
            return True
    
    def get_request_count(self, identifier: str = "default") -> int:
        """Get current request count in window"""
        with self.lock:
            current_time = time.time()
            log = self.request_logs[identifier]
            
            # Clean old requests
            self._clean_old_requests(log, current_time)
            
            return len(log)
    
    def get_oldest_request_time(self, identifier: str = "default") -> float:
        """Get timestamp of oldest request in current window"""
        with self.lock:
            current_time = time.time()
            log = self.request_logs[identifier]
            
            # Clean old requests
            self._clean_old_requests(log, current_time)
            
            return log[0] if log else current_time

# Usage example with detailed analytics
class AnalyticsRateLimiter(SlidingWindowLog):
    def __init__(self, window_size: int, max_requests: int):
        super().__init__(window_size, max_requests)
        self.rejected_requests = defaultdict(int)
        self.total_requests = defaultdict(int)
    
    def is_allowed(self, identifier: str = "default") -> bool:
        """Track analytics while rate limiting"""
        self.total_requests[identifier] += 1
        
        allowed = super().is_allowed(identifier)
        
        if not allowed:
            self.rejected_requests[identifier] += 1
        
        return allowed
    
    def get_analytics(self, identifier: str = "default") -> dict:
        """Get rate limiting analytics"""
        total = self.total_requests[identifier]
        rejected = self.rejected_requests[identifier]
        current_count = self.get_request_count(identifier)
        
        return {
            'total_requests': total,
            'rejected_requests': rejected,
            'success_rate': (total - rejected) / total if total > 0 else 0,
            'current_window_count': current_count,
            'remaining_requests': self.max_requests - current_count
        }

# Create rate limiter: 10 requests per 60 seconds
analytics_limiter = AnalyticsRateLimiter(window_size=60, max_requests=10)

# Simulate requests with analytics
user_id = "user456"
for i in range(15):
    allowed = analytics_limiter.is_allowed(user_id)
    analytics = analytics_limiter.get_analytics(user_id)
    
    print(f"Request {i}: {'Allowed' if allowed else 'Blocked'}")
    print(f"  Analytics: {analytics}")
    
    time.sleep(1)  # Space out requests
```

#### Memory-Optimized Sliding Window Log

```python
import bisect

class MemoryOptimizedSlidingWindowLog:
    def __init__(self, window_size: int, max_requests: int, cleanup_interval: int = 100):
        """
        Memory-optimized version with periodic cleanup
        
        Args:
            window_size: Window size in seconds
            max_requests: Maximum requests per window
            cleanup_interval: Requests between cleanup operations
        """
        self.window_size = window_size
        self.max_requests = max_requests
        self.cleanup_interval = cleanup_interval
        self.request_logs = defaultdict(list)  # Using list instead of deque
        self.request_counts = defaultdict(int)
        self.lock = threading.Lock()
    
    def _cleanup_if_needed(self, identifier: str):
        """Periodic cleanup to manage memory"""
        if self.request_counts[identifier] % self.cleanup_interval == 0:
            current_time = time.time()
            cutoff_time = current_time - self.window_size
            
            # Use binary search to find cutoff point
            log = self.request_logs[identifier]
            cutoff_index = bisect.bisect_right(log, cutoff_time)
            
            # Remove old entries
            if cutoff_index > 0:
                self.request_logs[identifier] = log[cutoff_index:]
    
    def is_allowed(self, identifier: str = "default") -> bool:
        """Optimized request checking"""
        with self.lock:
            current_time = time.time()
            cutoff_time = current_time - self.window_size
            
            # Count recent requests using binary search
            log = self.request_logs[identifier]
            cutoff_index = bisect.bisect_right(log, cutoff_time)
            recent_requests = len(log) - cutoff_index
            
            if recent_requests >= self.max_requests:
                return False
            
            # Add new request (list is kept sorted)
            bisect.insort(log, current_time)
            self.request_counts[identifier] += 1
            
            # Periodic cleanup
            self._cleanup_if_needed(identifier)
            
            return True
```

#### Pros and Cons

**Pros:**
- Very accurate rate limiting
- No edge cases at window boundaries
- Provides detailed request history
- Smooth rate limiting behavior

**Cons:**
- High memory usage for high-traffic applications
- Performance overhead for timestamp management
- Requires efficient data structure for timestamp storage

### 5. Sliding Window Counter Algorithm

**Concept**: Combines fixed window counter with sliding window concepts. Uses weighted averages of current and previous windows to estimate the rate.

#### How It Works

1. **Window Tracking**: Track current and previous window counters
2. **Weight Calculation**: Calculate how much of previous window to include
3. **Weighted Sum**: Compute weighted sum of windows
4. **Decision Logic**: Allow request if weighted sum is below limit

#### Implementation

```python
import time
import threading
from collections import defaultdict

class SlidingWindowCounter:
    def __init__(self, window_size: int, max_requests: int):
        """
        Initialize Sliding Window Counter
        
        Args:
            window_size: Window size in seconds
            max_requests: Maximum requests per window
        """
        self.window_size = window_size
        self.max_requests = max_requests
        self.current_window = defaultdict(int)
        self.previous_window = defaultdict(int)
        self.window_start_time = defaultdict(int)
        self.lock = threading.Lock()
    
    def _get_window_start(self, current_time: float) -> int:
        """Get current window start time"""
        return int(current_time // self.window_size) * self.window_size
    
    def _update_windows(self, identifier: str, current_time: float):
        """Update window counters if necessary"""
        window_start = self._get_window_start(current_time)
        
        if identifier not in self.window_start_time:
            self.window_start_time[identifier] = window_start
            return
        
        # Check if we need to slide the window
        if window_start > self.window_start_time[identifier]:
            # Move current to previous
            self.previous_window[identifier] = self.current_window[identifier]
            self.current_window[identifier] = 0
            self.window_start_time[identifier] = window_start
    
    def _calculate_weighted_count(self, identifier: str, current_time: float) -> float:
        """Calculate weighted request count across windows"""
        window_start = self.window_start_time[identifier]
        
        # How far into current window are we? (0.0 to 1.0)
        window_progress = (current_time - window_start) / self.window_size
        
        # Weight for previous window (decreases as we progress through current window)
        previous_weight = 1.0 - window_progress
        
        # Weighted sum
        weighted_count = (
            self.current_window[identifier] +
            self.previous_window[identifier] * previous_weight
        )
        
        return weighted_count
    
    def is_allowed(self, identifier: str = "default") -> bool:
        """
        Check if request is allowed using sliding window counter
        
        Args:
            identifier: User/IP identifier
            
        Returns:
            True if request allowed, False otherwise
        """
        with self.lock:
            current_time = time.time()
            
            # Update windows if necessary
            self._update_windows(identifier, current_time)
            
            # Calculate weighted count
            weighted_count = self._calculate_weighted_count(identifier, current_time)
            
            # Check if request would exceed limit
            if weighted_count >= self.max_requests:
                return False
            
            # Increment current window counter
            self.current_window[identifier] += 1
            return True
    
    def get_current_usage(self, identifier: str = "default") -> dict:
        """Get detailed usage information"""
        with self.lock:
            current_time = time.time()
            self._update_windows(identifier, current_time)
            
            weighted_count = self._calculate_weighted_count(identifier, current_time)
            window_progress = (current_time - self.window_start_time[identifier]) / self.window_size
            
            return {
                'weighted_count': weighted_count,
                'current_window_count': self.current_window[identifier],
                'previous_window_count': self.previous_window[identifier],
                'window_progress': window_progress,
                'remaining_requests': max(0, self.max_requests - weighted_count)
            }

# Usage example with monitoring
class MonitoredSlidingWindowCounter(SlidingWindowCounter):
    def __init__(self, window_size: int, max_requests: int):
        super().__init__(window_size, max_requests)
        self.total_requests = defaultdict(int)
        self.blocked_requests = defaultdict(int)
    
    def is_allowed(self, identifier: str = "default") -> bool:
        """Track statistics while rate limiting"""
        self.total_requests[identifier] += 1
        
        allowed = super().is_allowed(identifier)
        
        if not allowed:
            self.blocked_requests[identifier] += 1
        
        return allowed
    
    def get_statistics(self, identifier: str = "default") -> dict:
        """Get comprehensive statistics"""
        usage = self.get_current_usage(identifier)
        total = self.total_requests[identifier]
        blocked = self.blocked_requests[identifier]
        
        return {
            **usage,
            'total_requests': total,
            'blocked_requests': blocked,
            'success_rate': (total - blocked) / total if total > 0 else 1.0,
            'block_rate': blocked / total if total > 0 else 0.0
        }

# Create monitored rate limiter: 50 requests per 60 seconds
monitored_limiter = MonitoredSlidingWindowCounter(window_size=60, max_requests=50)

# Simulate traffic pattern
import random

user_id = "user789"
for i in range(100):
    allowed = monitored_limiter.is_allowed(user_id)
    stats = monitored_limiter.get_statistics(user_id)
    
    if i % 10 == 0:  # Print stats every 10 requests
        print(f"Request {i}: {'✓' if allowed else '✗'}")
        print(f"  Weighted count: {stats['weighted_count']:.2f}")
        print(f"  Window progress: {stats['window_progress']:.2f}")
        print(f"  Success rate: {stats['success_rate']:.2f}")
        print(f"  Remaining: {stats['remaining_requests']:.2f}")
        print()
    
    # Simulate variable request timing
    time.sleep(random.uniform(0.1, 2.0))
```

#### Pros and Cons

**Pros:**
- More accurate than fixed window counter
- More memory efficient than sliding window log
- Smoother rate limiting than fixed windows
- Good balance of accuracy and performance

**Cons:**
- More complex implementation than simple algorithms
- Still has some approximation (not perfectly accurate)
- Requires careful handling of window transitions

## Distributed Rate Limiting

For distributed systems, rate limiting becomes more complex as you need to coordinate limits across multiple servers.

### Redis-Based Distributed Rate Limiting

```python
import redis
import time
import threading

class DistributedRateLimiter:
    def __init__(self, redis_client: redis.Redis, window_size: int, max_requests: int):
        """
        Distributed rate limiter using Redis
        
        Args:
            redis_client: Redis client instance
            window_size: Window size in seconds
            max_requests: Maximum requests per window
        """
        self.redis = redis_client
        self.window_size = window_size
        self.max_requests = max_requests
    
    def is_allowed_fixed_window(self, identifier: str) -> bool:
        """Fixed window distributed rate limiting"""
        current_window = int(time.time() // self.window_size) * self.window_size
        key = f"rate_limit:{identifier}:{current_window}"
        
        # Use Redis pipeline for atomic operations
        pipe = self.redis.pipeline()
        pipe.incr(key)
        pipe.expire(key, self.window_size)
        results = pipe.execute()
        
        current_count = results[0]
        return current_count <= self.max_requests
    
    def is_allowed_sliding_window_log(self, identifier: str) -> bool:
        """Sliding window log using Redis sorted sets"""
        current_time = time.time()
        cutoff_time = current_time - self.window_size
        key = f"rate_limit_log:{identifier}"
        
        # Use Redis pipeline for atomic operations
        pipe = self.redis.pipeline()
        
        # Remove old entries
        pipe.zremrangebyscore(key, 0, cutoff_time)
        
        # Count current entries
        pipe.zcard(key)
        
        # Add current request if under limit
        # We'll check count and conditionally add
        results = pipe.execute()
        current_count = results[1]
        
        if current_count < self.max_requests:
            # Add current timestamp
            self.redis.zadd(key, {str(current_time): current_time})
            self.redis.expire(key, self.window_size)
            return True
        
        return False
    
    def is_allowed_token_bucket(self, identifier: str, refill_rate: float, capacity: int) -> bool:
        """Distributed token bucket using Redis"""
        key = f"token_bucket:{identifier}"
        current_time = time.time()
        
        # Lua script for atomic token bucket operations
        lua_script = """
        local key = KEYS[1]
        local capacity = tonumber(ARGV[1])
        local refill_rate = tonumber(ARGV[2])
        local current_time = tonumber(ARGV[3])
        local tokens_requested = tonumber(ARGV[4])
        
        local bucket = redis.call('HMGET', key, 'tokens', 'last_refill')
        local tokens = tonumber(bucket[1]) or capacity
        local last_refill = tonumber(bucket[2]) or current_time
        
        -- Refill tokens
        local elapsed = current_time - last_refill
        local tokens_to_add = elapsed * refill_rate
        tokens = math.min(capacity, tokens + tokens_to_add)
        
        -- Check if enough tokens
        if tokens >= tokens_requested then
            tokens = tokens - tokens_requested
            redis.call('HMSET', key, 'tokens', tokens, 'last_refill', current_time)
            redis.call('EXPIRE', key, 3600)  -- 1 hour expiry
            return 1
        else
            redis.call('HMSET', key, 'tokens', tokens, 'last_refill', current_time)
            redis.call('EXPIRE', key, 3600)
            return 0
        end
        """
        
        result = self.redis.eval(
            lua_script, 
            1, 
            key, 
            capacity, 
            refill_rate, 
            current_time, 
            1  # tokens requested
        )
        
        return bool(result)

# Usage with Redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)
distributed_limiter = DistributedRateLimiter(
    redis_client=redis_client,
    window_size=60,
    max_requests=100
)

# Test different algorithms
user_id = "distributed_user"

# Fixed window
allowed_fixed = distributed_limiter.is_allowed_fixed_window(user_id)
print(f"Fixed window: {'Allowed' if allowed_fixed else 'Blocked'}")

# Sliding window log
allowed_sliding = distributed_limiter.is_allowed_sliding_window_log(user_id)
print(f"Sliding window log: {'Allowed' if allowed_sliding else 'Blocked'}")

# Token bucket
allowed_token = distributed_limiter.is_allowed_token_bucket(user_id, refill_rate=1.0, capacity=10)
print(f"Token bucket: {'Allowed' if allowed_token else 'Blocked'}")
```

## Choosing the Right Algorithm

### Decision Matrix

| Algorithm | Accuracy | Memory Usage | Complexity | Burst Handling | Use Case |
|-----------|----------|--------------|------------|----------------|----------|
| Token Bucket | Good | Low | Low | Excellent | APIs with burst tolerance |
| Leaky Bucket | Excellent | Medium | Medium | Poor | Protecting downstream systems |
| Fixed Window | Fair | Low | Low | Poor | Simple rate limiting |
| Sliding Window Log | Excellent | High | Medium | Good | Precise rate limiting |
| Sliding Window Counter | Good | Low | Medium | Good | Balanced approach |

### Recommendations

**For High-Traffic APIs**
```python
# Use sliding window counter for balance of accuracy and performance
rate_limiter = SlidingWindowCounter(window_size=60, max_requests=1000)
```

**For Protecting Databases**
```python
# Use leaky bucket to ensure smooth, constant rate
db_protector = LeakyBucket(capacity=50, leak_rate=10.0)
```

**For User-Facing Features**
```python
# Use token bucket to allow occasional bursts
user_limiter = TokenBucket(capacity=20, refill_rate=2.0)
```

**For Compliance/Billing**
```python
# Use sliding window log for precise tracking
billing_limiter = SlidingWindowLog(window_size=3600, max_requests=1000)
```

## Advanced Topics

### Adaptive Rate Limiting

```python
class AdaptiveRateLimiter:
    def __init__(self, base_limit: int, window_size: int):
        self.base_limit = base_limit
        self.window_size = window_size
        self.current_limit = base_limit
        self.limiter = SlidingWindowCounter(window_size, base_limit)
        self.error_rate = 0.0
        self.last_adjustment = time.time()
    
    def update_error_rate(self, error_rate: float):
        """Update system error rate to adjust limits"""
        self.error_rate = error_rate
        
        # Adjust limit based on error rate
        if error_rate > 0.05:  # 5% error rate threshold
            # Reduce limit by 20%
            self.current_limit = int(self.current_limit * 0.8)
        elif error_rate < 0.01:  # 1% error rate threshold
            # Increase limit by 10%
            self.current_limit = min(self.base_limit, int(self.current_limit * 1.1))
        
        # Update limiter with new limit
        self.limiter.max_requests = self.current_limit
    
    def is_allowed(self, identifier: str) -> bool:
        return self.limiter.is_allowed(identifier)
```

### Rate Limiting with Priority Classes

```python
class PriorityRateLimiter:
    def __init__(self, limits: dict):
        """
        Rate limiter with priority classes
        
        Args:
            limits: Dict mapping priority -> (window_size, max_requests)
        """
        self.limiters = {}
        for priority, (window_size, max_requests) in limits.items():
            self.limiters[priority] = SlidingWindowCounter(window_size, max_requests)
    
    def is_allowed(self, identifier: str, priority: str = "normal") -> bool:
        """Check if request is allowed for given priority"""
        if priority not in self.limiters:
            priority = "normal"
        
        return self.limiters[priority].is_allowed(identifier)

# Usage
priority_limiter = PriorityRateLimiter({
    "premium": (60, 1000),    # 1000 requests per minute
    "normal": (60, 100),      # 100 requests per minute
    "free": (60, 10)          # 10 requests per minute
})
```

Rate limiting is crucial for building robust, scalable systems. Choose the algorithm that best fits your specific requirements for accuracy, performance, and complexity. Consider using distributed approaches for multi-server deployments and implement appropriate monitoring and alerting to ensure your rate limiting is working effectively.