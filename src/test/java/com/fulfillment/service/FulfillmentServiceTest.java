package com.fulfillment.service;

import com.fulfillment.service.dto.OrderRequest;
import com.fulfillment.service.dto.OrderResponse;
import com.fulfillment.service.model.OrderStatus;
import com.fulfillment.service.service.FulfillmentService;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import java.math.BigDecimal;

import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest
class FulfillmentServiceTest {

    @Autowired
    private FulfillmentService fulfillmentService;

    @Test
    @DisplayName("Should successfully process normal order and persist to SQL database")
    void testProcessOrderSuccess() {
        OrderRequest request = new OrderRequest("PROD-TEST-1", 3, new BigDecimal("25.00"), "test@example.com");

        OrderResponse response = fulfillmentService.processOrder(request);

        assertNotNull(response);
        assertNotNull(response.getId());
        assertEquals("PROD-TEST-1", response.getProductId());
        assertEquals(3, response.getQuantity());
        assertEquals(new BigDecimal("75.00"), response.getTotalPrice());
        assertEquals(OrderStatus.FULFILLED, response.getStatus());
    }

    @Test
    @DisplayName("Should trigger Resilience4j fallback when downstream inventory service fails")
    void testProcessOrderDownstreamFailure() {
        OrderRequest request = new OrderRequest("PROD-FAIL", 1, new BigDecimal("100.00"), "fallback@example.com");

        OrderResponse response = fulfillmentService.processOrder(request);

        assertNotNull(response);
        assertEquals(OrderStatus.FALLBACK_PROCESSING, response.getStatus());
        assertTrue(response.getMessage().contains("fallback"));
    }
}
