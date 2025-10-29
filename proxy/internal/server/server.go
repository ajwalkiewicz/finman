package server

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"proxy/internal/config"
	"proxy/internal/database"
)

type ServerService struct {
	Database   *database.DBService
	HttpServer *http.Server
	Config     *config.Config
}

func New(c *config.Config) *ServerService {
	dbService, err := database.New(c.RedisHost, c.RedisPort)

	if err != nil {
		log.Fatalf("Could not initialize database service: %v", err)
	}

	serverService := &ServerService{
		Database: dbService,
		Config:   c,
	}

	httpServer := &http.Server{
		Addr:         fmt.Sprintf(":%s", c.ProxyPort),
		Handler:      serverService.RegisterRoutes(),
		IdleTimeout:  time.Minute,
		ReadTimeout:  10 * time.Second,
		WriteTimeout: 30 * time.Second,
	}

	serverService.HttpServer = httpServer

	log.Printf("Server initialized on port %q", c.ProxyPort)

	return serverService
}

// Start runs the HTTP server and handles graceful shutdown on interrupt signals.
func (s *ServerService) Start() {
	// Start the server in a goroutine
	go func() {
		log.Printf("Starting server on http://0.0.0.0:%s", s.Config.ProxyPort)

		if err := s.HttpServer.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			log.Fatalf("Could not listen on %s: %v\n", s.Config.ProxyPort, err)
		}

		log.Println("Stopped serving new connections.")
	}()

	// Wait for interrupt signal to gracefully shutdown the server with
	sigChan := make(chan os.Signal, 1)
	signal.Notify(sigChan, syscall.SIGINT, syscall.SIGTERM)
	<-sigChan

	if err := s.Close(); err != nil {
		log.Fatalf("HTTP shutdown error: %v", err)
	}

	log.Println("Graceful shutdown complete.")
}

func (s *ServerService) Close() error {
	log.Printf("Stopping server on http://localhost:%s", s.Config.ProxyPort)

	dbErr := s.Database.Close()
	if dbErr != nil {
		log.Printf("Error closing database connection: %v", dbErr)
	}

	serverErr := s.HttpServer.Close()
	if serverErr != nil {
		log.Printf("Error closing server connection: %v", serverErr)
	}

	if dbErr != nil || serverErr != nil {
		return fmt.Errorf("errors during closing: dbErr=%v, serverErr=%v", dbErr, serverErr)
	}

	return nil
}

// Shutdown gracefully shuts down the server and database connections.
// In docker setup shutdown is tricky, because it can return error if
// database close itself before server shutdown is called.
// In such context, better use Close() method.
func (s *ServerService) Shutdown(ctx context.Context) error {
	log.Printf("Shutting down server on http://localhost:%d", s.Config.ProxyPort)

	dbErr := s.Database.Shutdown(ctx)
	if dbErr != nil {
		log.Printf("Error shutting down database connection: %v", dbErr)
	}

	serverErr := s.HttpServer.Shutdown(ctx)
	if serverErr != nil {
		log.Printf("Error shutting down server connection: %v", serverErr)
	}

	if dbErr != nil || serverErr != nil {
		return fmt.Errorf("errors during shutdown: dbErr=%v, serverErr=%v", dbErr, serverErr)
	}

	return nil
}
