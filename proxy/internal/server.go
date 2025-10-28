package internal

import (
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"log"
	"net/http"
	"time"

	"proxy/pkg"

	"github.com/redis/go-redis/v9"
)

const (
	CacheKeyPrefix string        = "exchange_rates"
	CacheDuration  time.Duration = 24 * 60 * 60 * time.Second // 24 hours
)

var supportedCurrencies = map[string]bool{
	"USD": true,
	"EUR": true,
	"PLN": true,
	"GTQ": true,
}

type Marshaler interface {
	Marshal() ([]byte, error)
}

type HealthResponse struct {
	Status         string `json:"status"`
	Timestamp      int64  `json:"timestamp"`
	RedisConnected bool   `json:"redisConnected"`
}

// Marshal method for HealthResponse
func (r *HealthResponse) Marshal() ([]byte, error) {
	out, err := json.Marshal(r)
	if err != nil {
		return nil, fmt.Errorf("failed to marshal health response: %v", err)
	}

	log.Printf("Response: %+v", r)
	return out, nil
}

type RatesResponse struct {
	Success   bool      `json:"success"`
	Timestamp int64     `json:"timestamp"`
	Date      string    `json:"date"` // Format: YYYY-MM-DD
	Base      string    `json:"base"`
	Rates     pkg.Rates `json:"rates"`
}

// Marshal method for RatesResponse
func (r *RatesResponse) Marshal() ([]byte, error) {
	out, err := json.Marshal(r)
	if err != nil {
		return nil, fmt.Errorf("failed to marshal rates response: %v", err)
	}

	log.Printf("Response: %+v", r)
	return out, nil
}

func getTodayCacheKey() string {
	today := time.Now().Format("2006-01-02")
	cacheKey := fmt.Sprintf("%s_%s", CacheKeyPrefix, today)
	log.Printf("Todays cache key: %s", cacheKey)
	return cacheKey
}

func GetRedisClient(redisHost, redisPort string) (*redis.Client, error) {
	log.Println("Connecting to Redis...")

	client := redis.NewClient(&redis.Options{
		Addr:     fmt.Sprintf("%s:%s", redisHost, redisPort),
		Password: "", // No password set
		DB:       0,  // Use default DB
		Protocol: 2,  // Connection protocol
	})

	ctx := context.Background()

	redisStatus := client.Ping(ctx).Err() == nil

	if !redisStatus {
		log.Printf("Cannot connect to redis at %s:%s", redisHost, redisPort)
		return nil, errors.New("failed to connect to Redis")
	}

	log.Println("Connected to Redis")
	return client, nil
}

func GetHealth(rc *redis.Client) http.HandlerFunc {
	ctx := context.Background()

	return func(w http.ResponseWriter, r *http.Request) {
		log.Printf("Received request: %s %s\n", r.Method, r.URL.Path)

		// Get health status
		redisStatus := rc.Ping(ctx).Err() == nil

		h := HealthResponse{
			Status:         "ok",
			Timestamp:      time.Now().Unix(),
			RedisConnected: redisStatus,
		}

		// Marshal the health check response
		out, err := h.Marshal()
		if err != nil {
			http.Error(w, "Failed to marshal health response", http.StatusInternalServerError)
			return
		}

		w.Header().Set("Content-Type", "application/json")
		w.Write(out)
	}
}

// Helper function to validate base currency parameter
func ValidateBaseCurrency(r *http.Request) error {
	if !r.URL.Query().Has("base") {
		return errors.New("missing 'base' query parameter")
	}

	base := r.URL.Query().Get("base")
	if base == "" {
		return fmt.Errorf("'base' query parameter cannot be empty")
	}

	if len(base) != 3 {
		return fmt.Errorf("'base' query parameter must be a 3-letter currency code")
	}

	if !supportedCurrencies[base] {
		return fmt.Errorf("unsupported 'base' currency: %s", base)
	}

	return nil
}

// Helper function to create a response with proper base currency conversion
func createRatesResponse(rates pkg.Rates, base string) (RatesResponse, error) {
	convertedRates := rates
	var err error

	if base != "EUR" {
		convertedRates, err = pkg.ConvertRates(&rates, base)
		if err != nil {
			return RatesResponse{}, fmt.Errorf("failed to convert rates: %v", err)
		}
	}

	return RatesResponse{
		Success:   true,
		Timestamp: time.Now().Unix(),
		Date:      time.Now().Format("2006-01-02"),
		Base:      base,
		Rates:     convertedRates,
	}, nil
}

// Helper function to handle default rates
func handleDefaultRates(defaultRates pkg.Rates, base string) (RatesResponse, error) {
	log.Println("Using default rates")

	response, err := createRatesResponse(defaultRates, base)
	if err != nil {
		return RatesResponse{}, err
	}

	return response, nil
}

// Helper function to handle API rates (both fresh and cached)
func handleAPIRates(rc *redis.Client, ctx context.Context, fixerAPIKey, base string) (RatesResponse, error) {
	todayKey := getTodayCacheKey()

	// Check cache first
	cached, err := rc.Get(ctx, todayKey).Result()
	log.Printf("Get from Redis: %s, err=%s", cached, err)

	var response RatesResponse

	if err != nil {
		// Cache miss - fetch from API
		log.Println("Data not found in cache")
		fixerSource := NewFixerSource(fixerAPIKey)
		response, err = fixerSource.FetchRates()
		if err != nil {
			return RatesResponse{}, fmt.Errorf("failed to fetch rates from Fixer API: %v", err)
		}

		// Save original EUR-based response to cache
		cachedData, err := response.Marshal()
		if err != nil {
			return RatesResponse{}, fmt.Errorf("failed to marshal rates for cache: %v", err)
		}
		rc.SetEx(ctx, todayKey, cachedData, CacheDuration)
	} else {
		// Cache hit - unmarshal cached data
		err = json.Unmarshal([]byte(cached), &response)
		if err != nil {
			return RatesResponse{}, fmt.Errorf("failed to unmarshal cached rates: %v", err)
		}
	}

	// Convert to requested base currency and create final response
	finalResponse, err := createRatesResponse(response.Rates, base)
	if err != nil {
		return RatesResponse{}, err
	}

	return finalResponse, nil
}

func GetRates(rc *redis.Client, c *Config) http.HandlerFunc {
	var defaultRates pkg.Rates
	useDefaultRates := false
	ctx := context.Background()

	if c.FixerAPIKey == "" {
		var err error
		useDefaultRates = true
		defaultRates, err = pkg.LoadRatesFromFile(c.DefaultRatesFile)
		if err != nil {
			log.Println("Error loading default rates:", err)
			panic("Cannot load default rates from rates.json")
		}
	}

	return func(w http.ResponseWriter, r *http.Request) {
		log.Printf("Received request: %s %s\n", r.Method, r.URL.Path)

		w.Header().Set("Content-Type", "application/json")
		base := r.URL.Query().Get("base")
		var response RatesResponse
		var err error

		// Handle request based on configuration
		if useDefaultRates {
			response, err = handleDefaultRates(defaultRates, base)
		} else {
			log.Println("Checking for data in cache...")
			response, err = handleAPIRates(rc, ctx, c.FixerAPIKey, base)
		}

		if err != nil {
			log.Printf("Error handling rates request: %v", err)
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		out, err := response.Marshal()
		if err != nil {
			log.Printf("Error marshalling rates response: %v", err)
			http.Error(w, "Failed to marshal rates response", http.StatusInternalServerError)
			return
		}

		w.Write(out)
	}
}
