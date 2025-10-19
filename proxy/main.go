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
	"time"

	"github.com/joho/godotenv"
	"github.com/redis/go-redis/v9"
)

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

type Rates struct {
	Eur float32 `json:"EUR"`
	Usd float32 `json:"USD"`
	Pln float32 `json:"PLN"`
	Gtq float32 `json:"GTQ"`
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

	r := &Config{
		RedisHost:   redisHost,
		RedisPort:   redisPort,
		FixerAPIKey: fixerAPI,
	}

	log.Printf("Config loaded: %+v", r)

	return r
}

func loadDefaultRates() Rates {
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

func fetchFromFixer(apiKey string) RatesResponse {
	log.Println("Fetching data from Fixer API")

	url := fmt.Sprintf(
		"https://data.fixer.io/api/latest?access_key=%s&symbols=EUR,USD,PLN,GTQ",
		apiKey,
	)

	r, err := http.Get(url)
	if err != nil {
		panic(err)
	}
	defer r.Body.Close()

	// Read file contents
	bytes, err := io.ReadAll(r.Body)
	if err != nil {
		log.Fatal(err)
	}

	var ratesResponse RatesResponse
	if err := json.Unmarshal(bytes, &ratesResponse); err != nil {
		log.Fatal(err)
	}

	log.Printf("Fetched data: %v", ratesResponse)

	return ratesResponse
}

func getTodayCacheKey() string {
	today := time.Now().Format("2006-01-02")
	cacheKey := fmt.Sprintf("%s_%s", CACHE_KEY_PREFIX, today)
	log.Printf("Todays cache key: %s", cacheKey)
	return cacheKey
}

func getRedisClient(c *Config) *redis.Client {
	log.Println("Connecting to Redis...")

	client := redis.NewClient(&redis.Options{
		Addr:     fmt.Sprintf("%s:%s", c.RedisHost, c.RedisPort),
		Password: "", // No password set
		DB:       0,  // Use default DB
		Protocol: 2,  // Connection protocol
	})

	ctx := context.Background()

	redisStatus := client.Ping(ctx).String() == "ping: PONG"

	if !redisStatus {
		log.Fatalln("Cannot connect to redis")
		panic(errors.New("Failed to connect to Redis"))
	}

	log.Println("Connected to Redis")
	return client
}

func getHealth(rc *redis.Client) http.HandlerFunc {
	ctx := context.Background()
	// Ping the Redis server, which should respond with PONG

	return func(w http.ResponseWriter, r *http.Request) {
		log.Printf("Received request: %s %s\n", r.Method, r.URL.Path)

		// Get health status
		redisStatus := rc.Ping(ctx).String() == "ping: PONG"

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
		io.Writer.Write(w, out)
	}
}

func getRates(c *Config, rc *redis.Client) http.HandlerFunc {
	useDefaultRates := false
	defaultRates := Rates{}

	ctx := context.Background()

	if c.FixerAPIKey == "" {
		useDefaultRates = true
		defaultRates = loadDefaultRates()
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
				Rates:     defaultRates,
			}

			// Marshal the rates response
			out, err := json.Marshal(resp)
			if err != nil {
				http.Error(w, "Failed to marshal rates response", http.StatusInternalServerError)
				return
			}
			io.Writer.Write(w, out)
			return
		}

		log.Println("Checking for data in cache...")

		todayKey := getTodayCacheKey()

		// Check cache first
		val, err := rc.Get(ctx, todayKey).Result()
		log.Printf("Get from Redis: %s, err=%s", val, err)

		if err != nil {
			log.Println("Data not found in cache")
			resp := fetchFromFixer(c.FixerAPIKey)
			out, err := json.Marshal(resp)
			if err != nil {
				http.Error(w, "Failed to marshal rates response", http.StatusInternalServerError)
				return
			}
			rc.SetEx(ctx, todayKey, out, CACHE_DURATION)
			io.Writer.Write(w, out)
		} else {
			var result map[string]interface{}
			err := json.Unmarshal([]byte(val), &result)
			if err != nil {
				http.Error(w, "Failed to marshal rates response", http.StatusInternalServerError)
				return
			}
			out, _ := json.Marshal(result)
			io.Writer.Write(w, out)
		}
	}
}

func main() {
	config := loadConfig()

	rc := getRedisClient(config)
	defer rc.Close()

	http.HandleFunc("/health", getHealth(rc))
	http.HandleFunc("/api/rates", getRates(config, rc))

	log.Println("Starting server on http://0.0.0.0:8080")
	err := http.ListenAndServe(":8080", nil)
	if err != nil {
		log.Fatalf("Failed to start server: %v", err)
	}
}
