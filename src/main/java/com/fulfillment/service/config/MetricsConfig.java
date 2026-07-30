package com.fulfillment.service.config;

import io.micrometer.core.instrument.Counter;
import io.micrometer.core.instrument.MeterRegistry;
import io.micrometer.core.instrument.Timer;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class MetricsConfig {

    @Bean
    public Counter ordersFulfilledCounter(MeterRegistry registry) {
        return Counter.builder("fulfillment.orders.fulfilled.total")
                .description("Total number of successfully fulfilled orders")
                .tag("service", "resilient-fulfillment-service")
                .tag("environment", "production")
                .register(registry);
    }

    @Bean
    public Counter ordersFallbackCounter(MeterRegistry registry) {
        return Counter.builder("fulfillment.orders.fallback.total")
                .description("Total number of orders routed through fallback processing")
                .tag("service", "resilient-fulfillment-service")
                .tag("environment", "production")
                .register(registry);
    }

    @Bean
    public Timer orderProcessingTimer(MeterRegistry registry) {
        return Timer.builder("fulfillment.orders.processing.latency")
                .description("Latency distribution of order processing in milliseconds")
                .tag("service", "resilient-fulfillment-service")
                .publishPercentiles(0.5, 0.95, 0.99)
                .register(registry);
    }
}
