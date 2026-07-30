package com.fulfillment.service.controller;

import com.fulfillment.service.dto.OrderRequest;
import com.fulfillment.service.dto.OrderResponse;
import com.fulfillment.service.service.FulfillmentService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/v1/orders")
@RequiredArgsConstructor
@Slf4j
public class OrderController {

    private final FulfillmentService fulfillmentService;

    @PostMapping
    public ResponseEntity<OrderResponse> createOrder(@RequestBody OrderRequest request) {
        log.info("Received POST /api/v1/orders for customer={}", request.getCustomerEmail());
        OrderResponse response = fulfillmentService.processOrder(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }

    @GetMapping
    public ResponseEntity<List<OrderResponse>> getAllOrders() {
        return ResponseEntity.ok(fulfillmentService.getAllOrders());
    }

    @GetMapping("/{orderNumber}")
    public ResponseEntity<OrderResponse> getOrderByNumber(@PathVariable String orderNumber) {
        return ResponseEntity.ok(fulfillmentService.getOrderByNumber(orderNumber));
    }

    @GetMapping("/health")
    public ResponseEntity<Map<String, String>> healthCheck() {
        return ResponseEntity.ok(Map.of(
                "status", "UP",
                "service", "ResilientFulfillmentService",
                "timestamp", java.time.LocalDateTime.now().toString()
        ));
    }
}
