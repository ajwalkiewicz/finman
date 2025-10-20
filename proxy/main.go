package main

import (
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"strings"
	"time"

	"github.com/joho/godotenv"
	"github.com/redis/go-redis/v9"
	"github.com/rs/cors"
)

type Rates map[string]float32

var supportedCurrencies = map[string]bool{
	"USD": true,
	"EUR": true,
	"PLN": true,
	"GTQ": true,
}

const (
	CACHE_KEY_PREFIX string        = "exchange_rates"
	CACHE_DURATION   time.Duration = 24 * 60 * 60 * time.Second // 24 hours
)

type Config struct {
	RedisHost   string
	RedisPort   string
	FixerAPIKey string
}

type HealthResponse struct {
	Status         string `json:"status"`
	Timestamp      int64  `json:"timestamp"`
	RedisConnected bool   `json:"redisConnected"`
}

type RatesResponse struct {
	Success   bool   `json:"success"`
	Timestamp int64  `json:"timestamp"`
	Date      string `json:"date"` // Format: YYYY-MM-DD
	Base      string `json:"base"`
	Rates     Rates  `json:"rates"`
}

func convertRates(r *Rates, newBase string) Rates {
	newRates := make(Rates)

	if baseRate, ok := (*r)[newBase]; ok {
		for currency, rate := range *r {
			newRates[currency] = rate / baseRate
		}
	}

	return newRates
}

func loadConfig() *Config {
	err := godotenv.Load()
	if err != nil {
		log.Printf("No .env file found or error loading it: %v", err)
	}

	redisHost := os.Getenv("REDIS_HOST")
	redisPort := os.Getenv("REDIS_PORT")
	fixerAPI := os.Getenv("FIXER_API_KEY")

	if redisHost == "" {
		redisHost = "127.0.0.1"
	}
	if redisPort == "" {
		redisPort = "6379"
	}

	config := &Config{
		RedisHost:   redisHost,
		RedisPort:   redisPort,
		FixerAPIKey: fixerAPI,
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

func loadRatesFromFile() Rates {
	log.Println("Loading default rates from rates.json file")
	// Open file
	file, err := os.Open("rates.json")
	if err != nil {
		log.Fatal(err)
	}
	// Something like "final" in Python
	defer file.Close()

	// Read file contents
	bytes, err := io.ReadAll(file)
	if err != nil {
		log.Fatal(err)
	}

	var rates Rates
	if err := json.Unmarshal(bytes, &rates); err != nil {
		log.Fatal(err)
	}

	return rates
}

func fetchFromFixer(apiKey string) (RatesResponse, error) {
	log.Println("Fetching data from Fixer API")

	url := fmt.Sprintf(
		"https://data.fixer.io/api/latest?access_key=%s&symbols=EUR,USD,PLN,GTQ",
		apiKey,
	)

	r, err := http.Get(url)
	if err != nil {
		log.Println("Error fetching data from Fixer API:", err)
		return RatesResponse{}, err
	}
	defer r.Body.Close()

	// Read file contents
	bytes, err := io.ReadAll(r.Body)
	if err != nil {
		log.Println("Error reading response body from Fixer API:", err)
		return RatesResponse{}, err
	}

	var ratesResponse RatesResponse
	if err := json.Unmarshal(bytes, &ratesResponse); err != nil {
		log.Println("Error unmarshalling response body from Fixer API:", err)
		return RatesResponse{}, err
	}

	log.Printf("Fetched data: %v", ratesResponse)

	return ratesResponse, nil
}

func getTodayCacheKey() string {
	today := time.Now().Format("2006-01-02")
	cacheKey := fmt.Sprintf("%s_%s", CACHE_KEY_PREFIX, today)
	log.Printf("Todays cache key: %s", cacheKey)
	return cacheKey
}

func getRedisClient(c *Config) (*redis.Client, error) {
	log.Println("Connecting to Redis...")

	client := redis.NewClient(&redis.Options{
		Addr:     fmt.Sprintf("%s:%s", c.RedisHost, c.RedisPort),
		Password: "", // No password set
		DB:       0,  // Use default DB
		Protocol: 2,  // Connection protocol
	})

	ctx := context.Background()

	redisStatus := client.Ping(ctx).Err() == nil

	if !redisStatus {
		log.Printf("Cannot connect to redis at %s:%s", c.RedisHost, c.RedisPort)
		return nil, errors.New("failed to connect to Redis")
	}

	log.Println("Connected to Redis")
	return client, nil
}

func getHealth(rc *redis.Client) http.HandlerFunc {
	ctx := context.Background()

	return func(w http.ResponseWriter, r *http.Request) {
		log.Printf("Received request: %s %s\n", r.Method, r.URL.Path)

		// Get health status
		redisStatus := rc.Ping(ctx).Err() == nil

		h := &HealthResponse{
			Status:         "ok",
			Timestamp:      time.Now().Unix(),
			RedisConnected: redisStatus,
		}

		// Marshal the health check response
		out, err := json.Marshal(h)
		if err != nil {
			http.Error(w, "Failed to marshal health response", http.StatusInternalServerError)
			return
		}

		w.Header().Set("Content-Type", "application/json")
		w.Write(out)
	}
}

func getRates(c *Config, rc *redis.Client) http.HandlerFunc {
	useDefaultRates := false
	defaultRates := Rates{}

	ctx := context.Background()

	if c.FixerAPIKey == "" {
		useDefaultRates = true
		defaultRates = loadRatesFromFile()
	}

	return func(w http.ResponseWriter, r *http.Request) {
		// Get exchange rates
		log.Printf("Received request: %s %s\n", r.Method, r.URL.Path)

		if !r.URL.Query().Has("base") {
			http.Error(w, "Missing 'base' query parameter", http.StatusBadRequest)
			return
		}

		base := r.URL.Query().Get("base")

		if base == "" {
			http.Error(w, "'base' query parameter cannot be empty", http.StatusBadRequest)
			return
		}

		if len(base) != 3 {
			http.Error(w, "'base' query parameter must be a 3-letter currency code", http.StatusBadRequest)
			return
		}

		if !supportedCurrencies[base] {
			http.Error(w, fmt.Sprintf("Unsupported 'base' currency: %s", base), http.StatusBadRequest)
			return
		}

		w.Header().Set("Content-Type", "application/json")

		if useDefaultRates {
			log.Println("Using default rates")

			resp := RatesResponse{
				Success:   true,
				Timestamp: time.Now().Unix(),
				Date:      time.Now().Format("2006-01-02"),
				Base:      base,
				Rates:     convertRates(&defaultRates, base),
			}

			// Marshal the rates response
			out, err := json.Marshal(resp)
			if err != nil {
				http.Error(w, "Failed to marshal rates response", http.StatusInternalServerError)
				return
			}
			w.Write(out)
			return
		}

		log.Println("Checking for data in cache...")

		todayKey := getTodayCacheKey()

		// Check cache first
		cached, err := rc.Get(ctx, todayKey).Result()
		log.Printf("Get from Redis: %s, err=%s", cached, err)

		if err != nil {
			log.Println("Data not found in cache")
			resp, err := fetchFromFixer(c.FixerAPIKey)
			if err != nil {
				http.Error(w, "Failed to fetch rates from Fixer API", http.StatusInternalServerError)
				return
			}

			if base != "EUR" {
				resp.Base = base
				resp.Rates = convertRates(&resp.Rates, base)
			}

			out, err := json.Marshal(resp)
			if err != nil {
				http.Error(w, "Failed to marshal rates response", http.StatusInternalServerError)
				return
			}
			rc.SetEx(ctx, todayKey, out, CACHE_DURATION)
			w.Write(out)
		} else {
			var result RatesResponse

			err := json.Unmarshal([]byte(cached), &result)
			if err != nil {
				http.Error(w, "Failed to unmarshal rates response", http.StatusInternalServerError)
				return
			}

			if base != "EUR" {
				result.Base = base
				result.Rates = convertRates(&result.Rates, base)
			}

			log.Printf("Response: %+v", result)

			out, err := json.Marshal(result)
			if err != nil {
				http.Error(w, "Failed to marshal rates response", http.StatusInternalServerError)
				return
			}
			w.Write(out)
		}
	}
}

func main() {
	var rc *redis.Client
	var err error

	config := loadConfig()

	rc, err = getRedisClient(config)
	if err != nil {
		log.Fatalf("Failed to connect to Redis: %v", err)
	}
	defer rc.Close()

	mux := http.NewServeMux()
	mux.HandleFunc("/health", getHealth(rc))
	mux.HandleFunc("/api/rates", getRates(config, rc))

	// Set up CORS middleware
	c := cors.New(cors.Options{
		AllowedOrigins: []string{
			"http://127.0.0.1:3000",
			"http://finman.walkiewicz.io",
			"https://finman.walkiewicz.io",
		},
		AllowCredentials: true,
		// Enable Debugging for testing, consider disabling in production
		Debug: false,
	})
	handler := c.Handler(mux)

	log.Println("Starting server on http://0.0.0.0:8012")
	err = http.ListenAndServe(":8012", handler)
	if err != nil {
		log.Fatalf("Failed to start server: %v", err)
	}
}
