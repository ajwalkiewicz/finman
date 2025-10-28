# Stage 1: Build the Go app
FROM golang:1.25 AS builder


# Set working directory
WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

# Copy application code
COPY . .

RUN CGO_ENABLED=0 GOOS=linux go build -o proxy ./cmd/api/main.go

# Stage 2: Create minimal image with Alpine for CA certificates and healthcheck support
FROM alpine:latest AS support

# Install ca-certificates for SSL/TLS connections and wget for health checks
RUN apk --no-cache add ca-certificates 

# Create a non-root user for security
RUN addgroup -S mygroup && adduser -D -u 1000 -S nonroot -G mygroup

FROM scratch AS final

# Copy CA certificates from the support stage
COPY --from=support /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt

# Copy the /etc/passwd file from the build stage to provide non-root user information
COPY --from=support /etc/passwd /etc/passwd

# Switch to non-root user
USER nonroot

# Copy application binary and files
COPY --from=builder /app/proxy /proxy
COPY --from=builder /app/rates.json /rates.json
COPY --from=builder /app/.env /.env

# Expose the port the app runs on
EXPOSE 8012

CMD ["/proxy", "server"]