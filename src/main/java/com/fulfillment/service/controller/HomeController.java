package com.fulfillment.service.controller;

import org.springframework.core.io.ClassPathResource;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ResponseBody;

import java.io.InputStream;
import java.nio.charset.StandardCharsets;

@Controller
public class HomeController {

    @GetMapping(value = "/", produces = MediaType.TEXT_HTML_VALUE)
    @ResponseBody
    public ResponseEntity<String> index() {
        try {
            ClassPathResource resource = new ClassPathResource("static/index.html");
            InputStream inputStream = resource.getInputStream();
            String htmlContent = new String(inputStream.readAllBytes(), StandardCharsets.UTF_8);
            return ResponseEntity.ok(htmlContent);
        } catch (Exception e) {
            return ResponseEntity.status(500).body("<html><body><h1>Error loading Dashboard</h1><p>" + e.getMessage() + "</p></body></html>");
        }
    }
}
