// Rates handling and conversion functions.

package rates

import (
	"encoding/json"
	"fmt"
	"io"
	"os"

	"proxy/internal/interfaces"
)

// Converts the rates to a new base currency.
func ConvertRates(r *interfaces.Rates, newBase string) (interfaces.Rates, error) {
	newRates := make(interfaces.Rates)

	baseRate, ok := (*r)[newBase]
	if !ok {
		return nil, fmt.Errorf("base currency not found in rates: %s", newBase)
	}

	if baseRate == 0 {
		return nil, fmt.Errorf("base currency rate is zero: %s", newBase)
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
func LoadRatesFromFile(path string) (interfaces.Rates, error) {
	// Open file
	file, err := os.Open(path)
	if err != nil {
		return nil, fmt.Errorf("failed to open '%s' file: %w", path, err)
	}
	// Ensure file is closed after function completes
	defer file.Close()

	// Read file contents
	bytes, err := io.ReadAll(file)
	if err != nil {
		return nil, fmt.Errorf("failed to read '%s' file: %w", path, err)
	}

	var rates interfaces.Rates
	if err := json.Unmarshal(bytes, &rates); err != nil {
		return nil, fmt.Errorf("failed to unmarshal '%s' file: %w", path, err)
	}

	return rates, nil
}
