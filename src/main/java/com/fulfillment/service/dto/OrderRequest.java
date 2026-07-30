package com.fulfillment.service.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.math.BigDecimal;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class OrderRequest {
    private String productId;
    private Integer quantity;
    private BigDecimal pricePerUnit;
    private String customerEmail;
}
