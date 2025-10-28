package pkg

import "testing"

func TestConvertRates(t *testing.T) {
	t.Run("Convert Rates to PLN", func(t *testing.T) {
		rates := Rates{
			"EUR": 1.0000,
			"USD": 1.1000,
			"PLN": 4.5000,
			"GTQ": 8.5000,
		}
		newBase := "PLN"

		got, _ := ConvertRates(&rates, newBase)
		want := Rates{
			"EUR": 0.22222222,
			"USD": 0.24444444,
			"PLN": 1.00000000,
			"GTQ": 1.88888884,
		}

		assertCorrectRates(t, got, want)
	})

	t.Run("Base currency not found in rates", func(t *testing.T) {
		rates := Rates{
			"EUR": 1.0000,
			"USD": 1.1000,
		}
		newBase := "PLN"

		_, err := ConvertRates(&rates, newBase)
		if err == nil {
			t.Errorf("expected error but got nil")
		}
	})

	t.Run("Base currency rate is zero", func(t *testing.T) {
		rates := Rates{
			"EUR": 1.0000,
			"USD": 1.1000,
			"PLN": 0.0000,
		}
		newBase := "PLN"

		_, err := ConvertRates(&rates, newBase)
		if err == nil {
			t.Errorf("expected error but got nil")
		}
	})

}

func assertCorrectRates(t testing.TB, got, want Rates) {
	t.Helper()
	for currency, wantRate := range want {
		if got[currency] != wantRate {
			t.Errorf("got %f want %f", got[currency], wantRate)
		}
	}
}
