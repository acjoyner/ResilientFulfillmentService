package com.fulfillment.service.service;

import io.github.resilience4j.bulkhead.annotation.Bulkhead;
import io.github.resilience4j.circuitbreaker.annotation.CircuitBreaker;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.util.Random;

@Service
@Slf4j
public class InventoryClientService {

    private final Random random = new Random();

    /**
     * Checks inventory allocation for an order.
     * Decorated with Resilience4j CircuitBreaker & Bulkhead annotations.
     */
    @CircuitBreaker(name = "inventoryServiceCB", fallbackMethod = "inventoryFallback")
    @Bulkhead(name = "inventoryServiceBH", fallbackMethod = "inventoryBulkheadFallback")
    public boolean verifyAndReserveInventory(String productId, int quantity) {
        log.info("Attempting downstream inventory check for productId={}, quantity={}", productId, quantity);

        // Simulate external network latency & potential failure
        if ("PROD-FAIL".equalsIgnoreCase(productId)) {
            log.error("Simulated downstream Inventory Service Failure for productId={}", productId);
            throw new RuntimeException("Inventory service connection timeout!");
        }

        if ("PROD-SLOW".equalsIgnoreCase(productId)) {
            try {
                log.warn("Simulated latency spike in Inventory Service for productId={}", productId);
                Thread.sleep(3000);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }

        log.info("Inventory successfully verified and reserved for productId={}", productId);
        return true;
    }

    // Circuit Breaker Fallback
    public boolean inventoryFallback(String productId, int quantity, Throwable t) {
        log.warn("[CIRCUIT BREAKER FALLBACK] Inventory Service call failed or circuit trip OPEN. Cause: {}. ProductId={}", 
                 t.getMessage(), productId);
        return false;
    }

    // Bulkhead Fallback (triggers when max concurrent calls exceeded)
    public boolean inventoryBulkheadFallback(String productId, int quantity, Throwable t) {
        log.warn("[BULKHEAD FALLBACK] Concurrent capacity limit reached for Inventory Service! ProductId={}", productId);
        return false;
    }
}
