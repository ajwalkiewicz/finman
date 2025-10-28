package internal

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"

	"proxy/pkg"
)

type RatesFetcher interface {
	FetchRates() (RatesResponse, error)
}

// Struct that represents Fixer source
type FixerSource struct {
	APIKey string
}

// Send request to Fixer and parse response ro RatesResponse
func (s *FixerSource) FetchRates() (RatesResponse, error) {
	query := fmt.Sprintf("access_key=%s&symbols=EUR,USD,PLN,GTQ", s.APIKey)
	url := fmt.Sprintf("https://data.fixer.io/api/latest?%s", query)

	r, err := http.Get(url)
	if err != nil {
		return RatesResponse{}, err
	}
	defer r.Body.Close()

	// Read file contents
	bytes, err := io.ReadAll(r.Body)
	if err != nil {
		return RatesResponse{}, err
	}

	var ratesResponse RatesResponse
	if err := json.Unmarshal(bytes, &ratesResponse); err != nil {
		return RatesResponse{}, err
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
func (s *FileSource) FetchRates() (RatesResponse, error) {
	file, err := os.Open(s.Path)
	if err != nil {
		return RatesResponse{}, fmt.Errorf("failed to open '%s' file: %w", s.Path, err)
	}

	// Something like "final" in Python
	defer file.Close()

	// Read file contents
	bytes, err := io.ReadAll(file)
	if err != nil {
		return RatesResponse{Success: false}, fmt.Errorf("failed to read '%s' file: %w", s.Path, err)
	}

	var rates pkg.Rates
	if err := json.Unmarshal(bytes, &rates); err != nil {
		return RatesResponse{Success: false}, fmt.Errorf("failed to unmarshal '%s' file: %w", s.Path, err)
	}

	return RatesResponse{
		Success: true,
		Rates:   rates,
	}, nil

}

func NewFileSource(path string) *FileSource {
	return &FileSource{Path: path}
}
