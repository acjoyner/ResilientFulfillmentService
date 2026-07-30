package com.fulfillment.service.repository;

import com.fulfillment.service.model.ProductCache;
import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ProductRedisRepository extends CrudRepository<ProductCache, String> {
}
