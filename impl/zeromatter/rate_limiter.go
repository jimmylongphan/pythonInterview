package main

import (
    "context"
    "fmt"
    "sync"
    "time"
)

type Request struct {
    ClientID  string
    Path      string
    Timestamp time.Time
}

type Response struct {
    StatusCode int
    Error      error
}

type BackendClient interface {
    Call(ctx context.Context, path string) error
}

// Simple mock backend
type MockBackend struct {
    shouldFail bool
}

func (m *MockBackend) Call(ctx context.Context, path string) error {
    time.Sleep(10 * time.Millisecond) // Simulate latency
    if m.shouldFail {
        return fmt.Errorf("backend error")
    }
    return nil
}

type APIGateway struct {
    backend         BackendClient
    
    // Rate limiter: Track request counts per client
    clientRequests  map[string][]time.Time
    rateLimitCount  int           // Max requests per window
    rateLimitWindow time.Duration // Time window
    
    // Circuit breaker: Track consecutive failures
    failureCount    int
    circuitOpen     bool
    circuitOpenTime time.Time
    
    mu              sync.Mutex
}

func NewAPIGateway(backend BackendClient) *APIGateway {
    return &APIGateway{
        backend:         backend,
        clientRequests:  make(map[string][]time.Time),
        rateLimitCount:  10,              // 10 requests
        rateLimitWindow: 10 * time.Second, // per 10 seconds
        // Circuit opens after 3 consecutive failures
        // TODO: Initialize other fields as needed
    }
}

func (g *APIGateway) HandleRequest(ctx context.Context, req Request) Response {
    g.mu.Lock()
    defer g.mu.Unlock()
    
    // TODO: Implement the following:
    
    // 1. RATE LIMITING
    // - Check if client has exceeded 10 requests in the last 10 seconds
    // - Use sliding window (filter out old timestamps)
    // - Return 429 if rate limited

		// g ~ dict()
		// g["clientRequests"] ~ dict(string, datetime)

		// check if clientId is in the clientRequests 
		accepted := false
		requests, exists := g.clientRequests[req.ClientID]
		
		// check if true
		//  --- check if true
		//  ------ check if true

		// check if false
		// check if false
		// check ...
		if exists {
			// check size of array
			if len(requests) < g.rateLimitCount {
				// append a new time element
				g.clientRequests[req.ClientID] = append(g.clientRequests[req.ClientID], req.Timestamp)
				accepted = true
			} else {
				// FYI = g.rateLimitWindow = 10
				// while earliest timestamp is less than current - 10
				// pop off elements 
				// if remaining size is < 10, then ok
				// else reject
				timestamps := g.clientRequests[req.ClientID]
				for len(timestamps) > 0 && timestamps[0].Before(time.Now().Add(-g.rateLimitWindow)) {
    			timestamps = timestamps[1:]
				}

				timestamps = append(timestamps, req.Timestamp)

				if len(timestamps) < g.rateLimitCount {
					accepted = true
				} else {
					accepted = false
				}
			}
		} else {
			g.clientRequests[req.ClientID] = []time.Time{}
			g.clientRequests[req.ClientID] = append(g.clientRequests[req.ClientID], req.Timestamp)
			accepted = true
		}

		if !accepted {
			return Response{StatusCode: 429, Error: fmt.Errorf("rate limited")}
		}
    
    return Response{StatusCode: 200}
}

// ============================================================================
// TEST CODE
// ============================================================================

func main() {
    fmt.Println("=== Test Rate Limiting ===")
    testRateLimiting()
    
    fmt.Println("\n=== Test Circuit Breaker ===")
    testCircuitBreaker()
}

func testRateLimiting() {
    backend := &MockBackend{shouldFail: false}
    gateway := NewAPIGateway(backend)
    
    // Send 12 requests rapidly (should hit rate limit at 11)
    rateLimited := false
    for i := 0; i < 12; i++ {
        req := Request{
            ClientID:  "client-1",
            Path:      "/api/test",
            Timestamp: time.Now(),
        }
        resp := gateway.HandleRequest(context.Background(), req)
        fmt.Printf("Request %d: Status %d\n", i+1, resp.StatusCode)
        if resp.StatusCode == 429 {
            rateLimited = true
            break
        }
    }
    
    if rateLimited {
        fmt.Println("✓ Rate limiting works!")
    } else {
        fmt.Println("✗ Rate limiting not working - FAIL!")
        return
    }
}

func testCircuitBreaker() {
    backend := &MockBackend{shouldFail: true}
    gateway := NewAPIGateway(backend)
    
    circuitOpened := false
    for i := 0; i < 5; i++ {
        req := Request{
            ClientID:  "client-2",
            Path:      "/api/test",
            Timestamp: time.Now(),
        }
        resp := gateway.HandleRequest(context.Background(), req)
        fmt.Printf("Request %d: Status %d\n", i+1, resp.StatusCode)
        if resp.StatusCode == 503 {
            circuitOpened = true
            fmt.Printf("Circuit opened after %d requests\n", i+1)
            break
        }
    }
    
    if circuitOpened {
        fmt.Println("✓ Circuit breaker works!")
    } else {
        fmt.Println("✗ Circuit breaker not working - FAIL!")
        return
    }
    
    // Test recovery
    fmt.Println("\nWaiting 5 seconds for circuit recovery...")
    time.Sleep(5 * time.Second)
    
    backend.shouldFail = false // Fix the backend
    req := Request{
        ClientID:  "client-2",
        Path:      "/api/test",
        Timestamp: time.Now(),
    }
    resp := gateway.HandleRequest(context.Background(), req)
    if resp.StatusCode == 200 {
        fmt.Println("✓ Circuit recovered!")
    }
}