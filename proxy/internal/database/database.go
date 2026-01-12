package database

import (
	"context"
	"fmt"
	"log"
	"time"

	"proxy/internal/interfaces"

	"github.com/redis/go-redis/v9"
)

const (
	CacheKeyPrefix string        = "exchange_rates"
	CacheDuration  time.Duration = 24 * 60 * 60 * time.Second // 24 hours
)

type DBService struct {
	Service *redis.Client
}

// New initializes a new Redis client and returns a Service interface.
func New(redisHost, redisPort string) (*DBService, error) {
	log.Println("Connecting to Redis...")

	client := redis.NewClient(&redis.Options{
		Addr:     fmt.Sprintf("%s:%s", redisHost, redisPort),
		Password: "", // No password set
		DB:       0,  // Use default DB
		Protocol: 2,  // Connection protocol
	})

	ctx := context.Background()

	attempts := 3
	baseSleep := 2 * time.Second
	var redisStatus bool

	for attempt := 0; attempt < attempts; attempt++ {
		redisStatus = client.Ping(ctx).Err() == nil

		if redisStatus {
			break
		}

		// Apply exponential backoff between retries to reduce load on Redis.
		if attempt < attempts-1 {
			sleep := baseSleep * time.Duration(1<<attempt)
			log.Printf("[Attempt %d/%d] Redis connection failed, retrying in %s...", attempt+1, attempts, sleep)
			time.Sleep(sleep)
		}
	}

	if !redisStatus {
		return nil, fmt.Errorf("could not connect to Redis after %d attempts", attempts)
	}

	log.Println("Connected to Redis")

	s := &DBService{Service: client}

	return s, nil
}

// Health returns the health status and statistics of the Redis server.
func (s *DBService) Health() interfaces.HealthResponse {
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second) // Default is now 5s
	defer cancel()

	redisStatus := s.Service.Ping(ctx).Err() == nil

	return interfaces.HealthResponse{
		Status:         "ok",
		Timestamp:      time.Now().Unix(),
		RedisConnected: redisStatus,
	}
}

// Close closes the Redis client connection.
func (s *DBService) Close() error {
	return s.Service.Close()
}

// Shutdown gracefully shuts down the Redis client connection.
func (s *DBService) Shutdown(ctx context.Context) error {
	cmd := s.Service.Shutdown(ctx)
	return cmd.Err()
}

// Get retrieves a value from Redis by key.
func (s *DBService) Get(key string) (string, error) {
	ctx, release := context.WithTimeout(context.Background(), 1*time.Second)
	defer release()

	return s.Service.Get(ctx, key).Result()
}

// Set stores a value in Redis with the specified key.
func (s *DBService) Set(key string, value any) error {
	ctx, release := context.WithTimeout(context.Background(), 1*time.Second)
	defer release()

	return s.Service.SetEx(ctx, key, value, CacheDuration).Err()
}

// GetCacheKey generates the cache key for today's date.
func GetCacheKey() string {
	today := time.Now().Format("2006-01-02")
	cacheKey := fmt.Sprintf("%s_%s", CacheKeyPrefix, today)
	return cacheKey
}
