package config

import (
	"fmt"
	"log"
	"os"
	"slices"
	"strings"

	"github.com/joho/godotenv"
)

const (
	DefaultProxyPort = "8012"
	DefaultRedisHost = "127.0.0.1"
	DefaultRedisPort = "6379"
	DefaultRatesFile = "rates.json"

	FixerSource    = "fixer"
	FileSource     = "file"
	ExternalSource = "external"
)

var ValidSources = []string{FixerSource, FileSource, ExternalSource}

// Config holds the configuration values for the application
type Config struct {
	ProxyPort        string
	RedisHost        string
	RedisPort        string
	RatesSource      string
	FixerAPIKey      string
	RatesFile        string
	ExternalRatesURL string
}

func isSourceValid(value string, validList []string) bool {
	return slices.Contains(validList, value)
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
	ratesSource := os.Getenv("RATES_SOURCE")
	fixerAPI := os.Getenv("FIXER_API_KEY")
	ratesFile := os.Getenv("DEFAULT_RATES_FILE")
	externalRatesURL := os.Getenv("EXTERNAL_RATES_URL")

	if proxyPort == "" {
		proxyPort = DefaultProxyPort
	}

	if redisHost == "" {
		redisHost = DefaultRedisHost
	}
	if redisPort == "" {
		redisPort = DefaultRedisPort
	}

	if !isSourceValid(ratesSource, ValidSources) {
		ratesSource = FileSource
	}

	if ratesFile == "" {
		ratesFile = DefaultRatesFile
	}

	// Validate rates file exists when using file source
	if ratesSource == FileSource {
		if _, err := os.Stat(ratesFile); err != nil {
			log.Fatalf("Configuration error: rates file '%s' does not exist or is not accessible: %v", ratesFile, err)
		}
	}

	config := &Config{
		ProxyPort:        proxyPort,
		RedisHost:        redisHost,
		RedisPort:        redisPort,
		RatesSource:      ratesSource,
		FixerAPIKey:      fixerAPI,
		RatesFile:        ratesFile,
		ExternalRatesURL: externalRatesURL,
	}

	log.Println(config.Log())

	return config
}

func (c *Config) Log() string {
	var sb strings.Builder

	length := len(c.FixerAPIKey)
	numberOfRevealedChars := 4
	numberOfAsterisks := max(length-numberOfRevealedChars, 0)

	var secretKey string
	if length > 0 {
		secretKey = strings.Repeat("*", numberOfAsterisks) + c.FixerAPIKey[numberOfAsterisks:]
	} else {
		secretKey = "(not set)"
	}

	sb.WriteString("Config:\n")
	sb.WriteString(fmt.Sprintf("  ProxyPort: %s\n", c.ProxyPort))
	sb.WriteString(fmt.Sprintf("  RedisHost: %s\n", c.RedisHost))
	sb.WriteString(fmt.Sprintf("  RedisPort: %s\n", c.RedisPort))
	sb.WriteString(fmt.Sprintf("  RatesSource: %s\n", c.RatesSource))
	sb.WriteString(fmt.Sprintf("  FixerAPIKey: %s\n", secretKey))
	sb.WriteString(fmt.Sprintf("  RatesFile: %s\n", c.RatesFile))
	sb.WriteString(fmt.Sprintf("  ExternalRatesURL: %s", c.ExternalRatesURL))
	return sb.String()
}
