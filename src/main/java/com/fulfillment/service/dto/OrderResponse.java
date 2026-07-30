package com.fulfillment.service.dto;

import com.fulfillment.service.model.OrderStatus;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;
import java.time.LocalDateTime;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class OrderResponse {
    private Long id;
    private String orderNumber;
    private String productId;
    private Integer quantity;
    private BigDecimal totalPrice;
    private OrderStatus status;
    private String message;
    private LocalDateTime createdAt;
}
