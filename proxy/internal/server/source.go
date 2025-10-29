package server

import (
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"time"

	"proxy/internal/interfaces"
)

type RatesFetcher interface {
	Fetch() (interfaces.RatesResponse, error)
}

// Struct that represents Fixer source
type FixerSource struct {
	APIKey string
}

// Send request to Fixer and parse response ro RatesResponse
func (s *FixerSource) Fetch() (interfaces.RatesResponse, error) {
	query := fmt.Sprintf("access_key=%s&symbols=EUR,USD,PLN,GTQ", s.APIKey)
	url := fmt.Sprintf("https://data.fixer.io/api/latest?%s", query)

	var resp *http.Response
	var err error

	attempts := 3
	sleep := 2 * time.Second
	for attempt := range attempts {
		resp, err = http.Get(url)
		if err == nil {
			break
		}
		log.Printf("Attempt %d: Error fetching rates from Fixer: %v", attempt+1, err)
		time.Sleep(sleep)
	}

	if err != nil {
		return interfaces.RatesResponse{}, err
	}

	defer resp.Body.Close()

	// Read response body
	bytes, err := io.ReadAll(resp.Body)
	if err != nil {
		return interfaces.RatesResponse{}, err
	}

	var ratesResponse interfaces.RatesResponse
	if err := json.Unmarshal(bytes, &ratesResponse); err != nil {
		return interfaces.RatesResponse{}, err
	}

	return ratesResponse, nil
}

func NewFixerSource(apiKey string) *FixerSource {
	return &FixerSource{APIKey: apiKey}
}

type FileSource struct {
	Path string
}

// Loads exchange rates from a JSON file.
// The file should contain a JSON object mapping currency codes to their rates.
// Example file content:
// {"EUR": 1.0000, "USD": 1.1000, "PLN": 4.5000, "GTQ": 8.5000}
func (s *FileSource) Fetch() (interfaces.RatesResponse, error) {
	file, err := os.Open(s.Path)
	if err != nil {
		return interfaces.RatesResponse{}, fmt.Errorf("failed to open '%s' file: %w", s.Path, err)
	}

	// Something like "final" in Python
	defer file.Close()

	// Read file contents
	bytes, err := io.ReadAll(file)
	if err != nil {
		return interfaces.RatesResponse{Success: false}, fmt.Errorf("failed to read '%s' file: %w", s.Path, err)
	}

	var rates interfaces.Rates
	if err := json.Unmarshal(bytes, &rates); err != nil {
		return interfaces.RatesResponse{Success: false}, fmt.Errorf("failed to unmarshal '%s' file: %w", s.Path, err)
	}

	return interfaces.RatesResponse{
		Success: true,
		Rates:   rates,
	}, nil

}

func NewFileSource(path string) *FileSource {
	return &FileSource{Path: path}
}

type DefaultSource struct {
	RatesResponse interfaces.RatesResponse
}

func (s *DefaultSource) Fetch() (interfaces.RatesResponse, error) {
	return s.RatesResponse, nil
}

func NewDefaultSource(ratesResponse interfaces.RatesResponse) *DefaultSource {
	return &DefaultSource{RatesResponse: ratesResponse}
}
