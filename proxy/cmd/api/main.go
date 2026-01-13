package main

import (
	"fmt"
	"net/http"
	"os"

	"proxy/internal/config"
	"proxy/internal/server"
)

// StartServer initializes and starts the HTTP server
func StartServer() {
	config := config.Load()
	serverService := server.New(config)
	serverService.Start()
}

// HealthCheck performs a health check by sending a request to the /health
// endpoint of the running server.
// Used in Docker "healthcheck".
func HealthCheck() {
	config := config.Load()

	url := fmt.Sprintf("http://127.0.0.1:%s/health", config.ProxyPort)
	if _, err := http.Get(url); err != nil {
		fmt.Printf("Health check failed: %v", err)
		os.Exit(2)
	}
}

func main() {
	progName := os.Args[0]
	usageMessage := fmt.Sprintf("Usage: %s <command>\nCommands:\n  server   Start the API server\n  check    Perform a health check\n", progName)

	if len(os.Args) < 2 {
		message := fmt.Sprintf("Expected 'server' or 'check' subcommands\n%s", usageMessage)
		fmt.Println(message)
		os.Exit(1)
	}

	command := os.Args[1]

	switch command {
	case "server":
		StartServer()
	case "check":
		HealthCheck()
	default:
		message := fmt.Sprintf("Unrecognized command: %q\n%s", command, usageMessage)
		fmt.Println(message)
		os.Exit(1)
	}
}
