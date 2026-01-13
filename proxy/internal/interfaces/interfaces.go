package interfaces

import (
	"encoding/json"
	"fmt"
	"log"
)

type Rates map[string]float64

type Service interface {
	Health() HealthResponse
	Close() error
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
func (hr *HealthResponse) Marshal() ([]byte, error) {
	out, err := json.Marshal(hr)
	if err != nil {
		return nil, fmt.Errorf("failed to marshal health response: %v", err)
	}

	log.Printf("Response: %+v", hr)
	return out, nil
}

type RatesResponse struct {
	Success   bool   `json:"success"`
	Timestamp int64  `json:"timestamp"`
	Date      string `json:"date"` // Format: YYYY-MM-DD
	Base      string `json:"base"`
	Rates     Rates  `json:"rates"`
}

// Marshal method for RatesResponse
func (rr *RatesResponse) Marshal() ([]byte, error) {
	out, err := json.Marshal(rr)
	if err != nil {
		return nil, fmt.Errorf("failed to marshal rates response: %v", err)
	}

	log.Printf("Response: %+v", rr)
	return out, nil
}
