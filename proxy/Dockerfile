# Stage 1: Build the Go app
FROM golang:1.25 AS builder


# Set working directory
WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

# Copy application code
COPY . .

RUN CGO_ENABLED=0 GOOS=linux go build -o proxy .

# Stage 2: Create minimal image with Alpine for CA certificates and healthcheck support
FROM alpine:latest

# Install ca-certificates for SSL/TLS connections and wget for healthchecks
RUN apk --no-cache add ca-certificates wget

# Copy the /etc/passwd file from the build stage to provide non-root user information
COPY --from=builder /etc/passwd /etc/passwd

# Copy application binary and files
COPY --from=builder /app/proxy /proxy
COPY --from=builder /app/rates.json /rates.json
COPY --from=builder /app/data/.env /.env

# Create a non-root user for security
RUN addgroup -S mygroup && adduser -D -u 1000 -S nonroot -G mygroup

USER nonroot

# Expose the port the app runs on
EXPOSE 8012

CMD ["/proxy"]