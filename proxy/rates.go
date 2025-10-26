// Rates handling and conversion functions.

package main

import (
	"encoding/json"
	"fmt"
	"io"
	"os"
)

type Rates map[string]float32

// Converts the rates to a new base currency.
func ConvertRates(r *Rates, newBase string) (Rates, error) {
	newRates := make(Rates)

	baseRate, ok := (*r)[newBase]
	if !ok {
		return nil, fmt.Errorf("base currency not found in rates: %s", newBase)
	}

	for currency, rate := range *r {
		newRates[currency] = rate / baseRate
	}
	newRates[newBase] = 1.0

	return newRates, nil
}

// Loads exchange rates from a JSON file.
// The file should contain a JSON object mapping currency codes to their rates.
// Example file content:
// {"EUR": 1.0000, "USD": 1.1000, "PLN": 4.5000, "GTQ": 8.5000}
func LoadRatesFromFile(path string) (Rates, error) {
	// Open file
	file, err := os.Open(path)
	if err != nil {
		return nil, fmt.Errorf("failed to open '%s' file: %w", path, err)
	}
	// Something like "final" in Python
	defer file.Close()

	// Read file contents
	bytes, err := io.ReadAll(file)
	if err != nil {
		return nil, fmt.Errorf("failed to read '%s' file: %w", path, err)
	}

	var rates Rates
	if err := json.Unmarshal(bytes, &rates); err != nil {
		return nil, fmt.Errorf("failed to unmarshal '%s' file: %w", path, err)
	}

	return rates, nil
}
