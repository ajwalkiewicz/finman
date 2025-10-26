// proxy/config.go

package main

import (
	"log"
	"os"
	"strings"

	"github.com/joho/godotenv"
)

// Config holds the configuration values for the application
type Config struct {
	RedisHost        string
	RedisPort        string
	FixerAPIKey      string
	DefaultRatesFile string
}

// LoadConfig loads configuration from environment variables or .env file
func LoadConfig() *Config {
	err := godotenv.Load()
	if err != nil {
		log.Printf("No .env file found or error loading it: %v", err)
	}

	redisHost := os.Getenv("REDIS_HOST")
	redisPort := os.Getenv("REDIS_PORT")
	fixerAPI := os.Getenv("FIXER_API_KEY")
	defaultRatesFile := os.Getenv("DEFAULT_RATES_FILE")

	if redisHost == "" {
		redisHost = "127.0.0.1"
	}
	if redisPort == "" {
		redisPort = "6379"
	}

	if defaultRatesFile == "" {
		defaultRatesFile = "rates.json"
	}

	config := &Config{
		RedisHost:        redisHost,
		RedisPort:        redisPort,
		FixerAPIKey:      fixerAPI,
		DefaultRatesFile: defaultRatesFile,
	}

	log.Printf("Loaded config")

	length := len(config.FixerAPIKey)
	numberOfRevealedChars := 4
	numberOfAsterisks := length - numberOfRevealedChars

	if length > 0 {
		log.Printf("Fixer API Key: %s", strings.Repeat("*", numberOfAsterisks)+config.FixerAPIKey[numberOfAsterisks:])
	} else {
		log.Printf("No Fixer API Key provided, using default rates from rates.json")
	}

	log.Printf("Redis Host: %s", config.RedisHost)
	log.Printf("Redis Port: %s", config.RedisPort)

	return config
}
