package com.fulfillment.service.model;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.data.annotation.Id;
import org.springframework.data.redis.core.RedisHash;

import java.io.Serializable;
import java.math.BigDecimal;

@Data
@NoArgsConstructor
@AllArgsConstructor
@RedisHash(value = "ProductCache", timeToLive = 600) // TTL 10 minutes
public class ProductCache implements Serializable {

    @Id
    private String id;
    private String name;
    private BigDecimal price;
    private Integer availableStock;
}
