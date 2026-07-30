# Multi-stage Dockerfile for Resilient Fulfillment Microservice

# Stage 1: Build JAR using Maven
FROM maven:3.9.6-eclipse-temurin-17 AS builder
WORKDIR /app
COPY pom.xml .
COPY src ./src
RUN mvn clean package -DskipTests

# Stage 2: Minimal Linux Runtime Image
FROM eclipse-temurin:17-jre
WORKDIR /opt/fulfillment-service

# Create non-root system user for security
RUN groupadd -r fulfillment && useradd -r -g fulfillment fulfillment

# Copy built artifact from builder stage
COPY --from=builder /app/target/resilient-fulfillment-service-1.0.0-SNAPSHOT.jar app.jar

# Create log directory and set ownership
RUN mkdir -p /var/log/fulfillment-service && chown -R fulfillment:fulfillment /opt/fulfillment-service /var/log/fulfillment-service

USER fulfillment

EXPOSE 8080

ENTRYPOINT ["java", "-Xms256m", "-Xmx512m", "-XX:+UseG1GC", "-jar", "app.jar"]
