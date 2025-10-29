package server

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"

	"proxy/internal/database"
	"proxy/internal/interfaces"
	"proxy/pkg/rates"

	"github.com/rs/cors"
)

func (s *ServerService) RegisterRoutes() http.Handler {
	// Create new mux and register handlers
	mux := http.NewServeMux()

	// Register routes with middleware
	mux.HandleFunc(
		"/health",
		Chain(
			s.GetHealth(),
			Method("GET"),
			Logging(),
		),
	)
	mux.HandleFunc(
		"/api/rates",
		Chain(
			s.GetRates(),
			Method("GET"),
			Validator(ValidateBaseCurrency),
			Logging(),
		),
	)

	// Set up CORS middleware
	newHandler := cors.New(cors.Options{
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

	return newHandler.Handler(mux)
}

func (s *ServerService) GetHealth() http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		log.Printf("Received request: %s %s\n", r.Method, r.URL.Path)

		// Get health status from database
		hr := s.Database.Health()

		// Marshal the health check response
		out, err := hr.Marshal()
		if err != nil {
			http.Error(w, "Failed to marshal health response", http.StatusInternalServerError)
			return
		}

		w.Header().Set("Content-Type", "application/json")
		w.Write(out)
	}
}

func (s *ServerService) GetRates() http.HandlerFunc {
	FileSource := NewFileSource(s.Config.RatesFile)
	FixerSource := NewFixerSource(s.Config.FixerAPIKey)

	// Load default rates from file.
	// This will be used if API fetching fails or if configured to use default rates.
	DefaultRatesResponse, err := FileSource.Fetch()
	if err != nil || !DefaultRatesResponse.Success {
		log.Println("Failed to load default rates from file")
		DefaultRatesResponse = interfaces.RatesResponse{
			Rates: interfaces.Rates{
				"EUR": 1.0000,
				"USD": 1.1000,
				"PLN": 4.5000,
				"GTQ": 8.5000,
			},
		}
	}

	DefaultSource := NewDefaultSource(DefaultRatesResponse)

	var RatesSource RatesFetcher
	var RatesHandler func(RatesFetcher, interfaces.RatesResponse) (interfaces.RatesResponse, error)

	if s.Config.UseDefaultRates {
		log.Println("Using default rates as rates source")
		RatesSource = DefaultSource
		RatesHandler = s.handleDefaultRates
	} else {
		log.Println("Using Fixer API as rates source")
		RatesSource = FixerSource
		RatesHandler = s.handleAPIRates
	}

	return func(w http.ResponseWriter, r *http.Request) {
		log.Printf("Received request: %s %s\n", r.Method, r.URL.Path)

		var response interfaces.RatesResponse
		var err error

		response, err = RatesHandler(RatesSource, DefaultRatesResponse)

		if err != nil {
			log.Printf("Error handling rates request: %v", err)
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		// Recalculate rates if base currency is not EUR
		base := r.URL.Query().Get("base")

		response, err = RecalculateRates(response, base)
		if err != nil {
			log.Printf("Error recalculating rates: %v", err)
			http.Error(w, "Failed to recalculate rates", http.StatusInternalServerError)
			return
		}

		// Marshaling - means converting the bytes that can be sent over the network
		out, err := response.Marshal()
		if err != nil {
			log.Printf("Error marshalling rates response: %v", err)
			http.Error(w, "Failed to marshal rates response", http.StatusInternalServerError)
			return
		}

		w.Header().Set("Content-Type", "application/json")
		w.Write(out)
	}
}

// Helper function to handle API rates (both fresh and cached)
// It tries to get rates from cache first, if not found, fetches from API
// and if that fails, falls back to default rates.
func (s *ServerService) handleAPIRates(rf RatesFetcher, dr interfaces.RatesResponse) (interfaces.RatesResponse, error) {
	todayKey := database.GetCacheKey()

	// Check cache first
	cached, err := s.Database.Get(todayKey)
	log.Printf("Get from Redis: %q, err=%v", cached, err)

	var response interfaces.RatesResponse

	if err != nil {
		// Cache miss - fetch from API
		log.Println("Data not found in cache")
		response, err = rf.Fetch()
		if err != nil {
			log.Printf("Error fetching rates from API: %v", err)
			// Fallback to default rates if API fetch fails
			return dr, fmt.Errorf("failed to fetch rates from Fixer API: %v", err)
		}

		// Save original EUR-based response to cache
		cachedData, err := response.Marshal()
		if err != nil {
			return response, fmt.Errorf("failed to marshal rates for cache: %v", err)
		}
		s.Database.Set(todayKey, cachedData)
	} else {
		// Cache hit - unmarshal cached data
		err = json.Unmarshal([]byte(cached), &response)
		if err != nil {
			return response, fmt.Errorf("failed to unmarshal cached rates: %v", err)
		}
	}

	return response, nil
}

func (s *ServerService) handleDefaultRates(rf RatesFetcher, dr interfaces.RatesResponse) (interfaces.RatesResponse, error) {
	// Always return default rates
	return dr, nil
}

// Helper function to recalculate rates based on requested base currency.
func RecalculateRates(rr interfaces.RatesResponse, base string) (interfaces.RatesResponse, error) {
	var convertedRates interfaces.Rates
	var err error

	if base != "EUR" {
		convertedRates, err = rates.ConvertRates(&rr.Rates, base)
		if err != nil {
			return interfaces.RatesResponse{}, fmt.Errorf("failed to convert rates: %v", err)
		}
		rr.Rates = convertedRates
		rr.Base = base
	}

	return rr, nil
}
