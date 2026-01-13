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

// Helper function to send HTTP GET request with retries
// TODO: Consider using context with timeout
func sendRequest(url string) (*http.Response, error) {
	var resp *http.Response
	var err error

	attempts := 3
	sleep := 1 * time.Second
	for attempt := range attempts {
		resp, err = http.Get(url)
		if err == nil {
			break
		}
		log.Printf("Attempt %d: Error sending request to %s: %v", attempt+1, url, err)
		sleep *= 2
		time.Sleep(sleep)
	}

	if err != nil {
		return nil, err
	}

	return resp, nil
}

type RatesFetcher interface {
	Fetch() (interfaces.RatesResponse, error)
}

// Struct that represents a generic source
type GenericSource struct {
	URL string
}

// Send request to Generic source and parse response to RatesResponse
func (s *GenericSource) Fetch() (interfaces.RatesResponse, error) {
	resp, err := sendRequest(s.URL)

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

func NewGenericSource(url string) *GenericSource {
	return &GenericSource{URL: url}
}

// Struct that represents Fixer source
type FixerSource struct {
	APIKey string
}

// Send request to Fixer and parse response to RatesResponse
func (s *FixerSource) Fetch() (interfaces.RatesResponse, error) {
	query := fmt.Sprintf("access_key=%s&symbols=EUR,USD,PLN,GTQ", s.APIKey)
	url := fmt.Sprintf("https://data.fixer.io/api/latest?%s", query)

	resp, err := sendRequest(url)

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
