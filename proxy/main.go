package main

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/redis/go-redis/v9"
	"github.com/rs/cors"
)

// StartServer initializes and starts the HTTP server
func StartServer() {
	var rc *redis.Client
	var err error

	config := LoadConfig()

	// Try to connect to Redis with retries
	attempts := 3
	sleep := 2 * time.Second

	for range attempts {
		rc, err = getRedisClient(config)
		if err == nil {
			break
		}
		time.Sleep(sleep)
	}

	if err != nil {
		log.Fatalf("Failed to connect to Redis after %d attempts: %v", attempts, err)
	}

	defer rc.Close()

	// Create new mux and register handlers
	mux := http.NewServeMux()
	mux.HandleFunc("/health", Chain(getHealth(rc), Method("GET"), Logging()))
	mux.HandleFunc(
		"/api/rates",
		Chain(
			getRates(config, rc),
			Method("GET"),
			Validator(ValidateBaseCurrency),
			Logging(),
		),
	)

	// Set up CORS middleware
	c := cors.New(cors.Options{
		AllowedOrigins: []string{
			"http://127.0.0.1:3000",
			"http://localhost:3000",
			"http://finman.walkiewicz.io",
			"https://finman.walkiewicz.io",
		},
		AllowCredentials: true,
		// Enable Debugging for testing, consider disabling in production
		Debug: false,
	})
	handler := c.Handler(mux)

	// Create the HTTP server
	server := &http.Server{
		Addr:    ":8012",
		Handler: handler,
	}

	// Start the server in a goroutine
	go func() {
		log.Printf("Starting server on http://0.0.0.0%s", server.Addr)

		if err := server.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			log.Fatalf("Could not listen on %s: %v\n", server.Addr, err)
		}

		log.Println("Stopped serving new connections.")
	}()

	// Wait for interrupt signal to gracefully shutdown the server with
	sigChan := make(chan os.Signal, 1)
	signal.Notify(sigChan, syscall.SIGINT, syscall.SIGTERM)
	<-sigChan

	shutdownCtx, shutdownRelease := context.WithTimeout(context.Background(), 10*time.Second)
	defer shutdownRelease()

	if err := server.Shutdown(shutdownCtx); err != nil {
		log.Fatalf("HTTP shutdown error: %v", err)
	}

	log.Println("Graceful shutdown complete.")
}

// HealthCheck performs a health check by sending a request to the /health endpoint
// of the running server.
// Used in Docker healthcheck.
func HealthCheck() {
	url := "http://127.0.0.1:8012/health"
	if _, err := http.Get(url); err != nil {
		fmt.Printf("Health check failed: %v", err)
		os.Exit(2)
	}
}

func main() {
	if len(os.Args) < 2 {
		fmt.Println("expected 'server' or 'check' subcommands")
		os.Exit(1)
	}

	switch os.Args[1] {
	case "server":
		StartServer()
	case "check":
		HealthCheck()
	default:
		fmt.Println("expected 'server' or 'check' subcommands")
		os.Exit(1)
	}
}
