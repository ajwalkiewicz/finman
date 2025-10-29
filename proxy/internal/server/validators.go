package server

import (
	"errors"
	"fmt"
	"net/http"
)

var supportedCurrencies = map[string]bool{
	"USD": true,
	"EUR": true,
	"PLN": true,
	"GTQ": true,
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
