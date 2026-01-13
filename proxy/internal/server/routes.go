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

// RegisterRoutes sets up the HTTP routes and their corresponding handlers
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

// Handler for /health endpoint
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
		if _, err := w.Write(out); err != nil {
			log.Printf("Failed to write health response: %v", err)
		}

	}
}

// Handler for /api/rates endpoint
func (s *ServerService) GetRates() http.HandlerFunc {
	fileSource := NewFileSource(s.Config.RatesFile)
	fixerSource := NewFixerSource(s.Config.FixerAPIKey)

	// Load default rates from file.
	// This will be used if API fetching fails or if configured to use default rates.
	defaultRatesResponse, err := fileSource.Fetch()
	if err != nil || !defaultRatesResponse.Success {
		log.Println("Failed to load default rates from file")
		defaultRatesResponse = interfaces.RatesResponse{
			Rates: interfaces.Rates{
				"EUR": 1.0000,
				"USD": 1.1000,
				"PLN": 4.5000,
				"GTQ": 8.5000,
			},
		}
	}

	defaultSource := NewDefaultSource(defaultRatesResponse)

	var ratesFetcher RatesFetcher
	var ratesHandler func(RatesFetcher, *interfaces.RatesResponse) (*interfaces.RatesResponse, error)

	switch s.Config.RatesSource {
	case "file":
		log.Println("Using file as rates source (default rates)")
		ratesFetcher = defaultSource
		ratesHandler = s.handleDefaultRates
	case "fixer":
		log.Println("Using Fixer API as rates source")
		ratesFetcher = fixerSource
		ratesHandler = s.handleAPIRates
	case "external":
		log.Println("Using external URL as rates source")
		genericSource := NewGenericSource(s.Config.ExternalRatesURL)
		ratesFetcher = genericSource
		ratesHandler = s.handleAPIRates
	}

	return func(w http.ResponseWriter, r *http.Request) {
		log.Printf("Received request: %s %s\n", r.Method, r.URL.Path)

		var response *interfaces.RatesResponse
		var err error

		response, err = ratesHandler(ratesFetcher, &defaultRatesResponse)

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
		if _, err := w.Write(out); err != nil {
			log.Printf("Failed to write health response: %v", err)
		}
	}
}

// Helper function to handle API rates (both fresh and cached)
// It tries to get rates from cache first, if not found, fetches from API
// and if that fails, falls back to default rates.
func (s *ServerService) handleAPIRates(rf RatesFetcher, dr *interfaces.RatesResponse) (*interfaces.RatesResponse, error) {
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
			return dr, fmt.Errorf("failed to fetch rates from rates provider: %v", err)
		}

		// Save original EUR-based response to cache
		cachedData, err := response.Marshal()
		if err != nil {
			return &response, fmt.Errorf("failed to marshal rates for cache: %v", err)
		}
		s.Database.Set(todayKey, cachedData)
	} else {
		// Cache hit - unmarshal cached data
		err = json.Unmarshal([]byte(cached), &response)
		if err != nil {
			return &response, fmt.Errorf("failed to unmarshal cached rates: %v", err)
		}
	}

	return &response, nil
}

// Helper function to handle default rates
func (s *ServerService) handleDefaultRates(rf RatesFetcher, dr *interfaces.RatesResponse) (*interfaces.RatesResponse, error) {
	// Always return default rates
	return dr, nil
}

// Helper function to recalculate rates based on requested base currency.
// If base is "EUR", no recalculation is needed
// (this is because rates are always provided with EUR as base).
func RecalculateRates(rr *interfaces.RatesResponse, base string) (*interfaces.RatesResponse, error) {
	var convertedRates interfaces.Rates
	var err error

	if base != "EUR" {
		convertedRates, err = rates.ConvertRates(&rr.Rates, base)
		if err != nil {
			return nil, fmt.Errorf("failed to convert rates: %v", err)
		}
		rr.Rates = convertedRates
		rr.Base = base
	}

	return rr, nil
}
