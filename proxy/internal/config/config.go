package config

import (
	"log"
	"os"
	"strings"

	"github.com/joho/godotenv"
)

const (
	DefaultProxyPort = "8012"
	DefaultRedisHost = "127.0.0.1"
	DefaultRedisPort = "6379"
	DefaultRatesFile = "rates.json"
)

// Config holds the configuration values for the application
type Config struct {
	ProxyPort       string
	RedisHost       string
	RedisPort       string
	FixerAPIKey     string
	RatesFile       string
	UseDefaultRates bool
}

// Load loads configuration from environment variables or .env file
func Load() *Config {
	err := godotenv.Load()
	if err != nil {
		log.Printf("No .env file found or error loading it: %v", err)
	}

	proxyPort := os.Getenv("PROXY_PORT")
	redisHost := os.Getenv("REDIS_HOST")
	redisPort := os.Getenv("REDIS_PORT")
	fixerAPI := os.Getenv("FIXER_API_KEY")
	ratesFile := os.Getenv("DEFAULT_RATES_FILE")

	if proxyPort == "" {
		proxyPort = DefaultProxyPort
	}

	if redisHost == "" {
		redisHost = DefaultRedisHost
	}
	if redisPort == "" {
		redisPort = DefaultRedisPort
	}

	var useDefaultRates bool
	if fixerAPI == "" {
		useDefaultRates = true
	} else {
		useDefaultRates = false
	}

	if ratesFile == "" {
		ratesFile = DefaultRatesFile
	}

	config := &Config{
		ProxyPort:       proxyPort,
		RedisHost:       redisHost,
		RedisPort:       redisPort,
		FixerAPIKey:     fixerAPI,
		RatesFile:       ratesFile,
		UseDefaultRates: useDefaultRates,
	}

	log.Printf("Loaded config")

	length := len(config.FixerAPIKey)
	numberOfRevealedChars := 4
	numberOfAsterisks := max(length-numberOfRevealedChars, 0)

	if length > 0 {
		log.Printf("Fixer API Key: %s", strings.Repeat("*", numberOfAsterisks)+config.FixerAPIKey[numberOfAsterisks:])
	} else {
		log.Printf("No Fixer API Key provided, using default rates from rates.json")
	}

	log.Printf("Redis Host: %s", config.RedisHost)
	log.Printf("Redis Port: %s", config.RedisPort)

	return config
}
