package com.example.entity;


import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.ToString;
import org.springframework.stereotype.Component;

@Data
public class User {
    private String name;
    private String sex;
    private int id;

    public User() {
    }

    public User(String name, int age) {
        this.name = name;
        this.id = age;
    }

}
