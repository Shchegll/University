#pragma once

#include <iostream>

template <typename T>
class Stack {
public:
    Stack() : topNode(nullptr), stackSize(0) {}

    ~Stack() {
        while (!isEmpty()) {
            pop();
        }
    }

    void push(const T& value) {
        Node* newNode = new Node(value);
        newNode->next = topNode;
        topNode = newNode;
        stackSize++;
    }

    T pop() {
        if (isEmpty()) {
            std::cerr << "Oshibka: stack is empty. Code ";
            return T();
        }

        T value = topNode->value;
        Node* temp = topNode;
        topNode = topNode->next;
        delete temp;
        stackSize--;
        return value;
    }

    T top() {
        if (isEmpty()) {
            std::cerr << "Oshibka: stack is empty. Code ";
            return T();
        }

        return topNode->value;
    }

    bool isEmpty() const {
        return stackSize == 0;
    }

    int size() const {
        return stackSize;
    }

private:
    struct Node {
        T value;
        Node* next;

        Node(const T& val) : value(val), next(nullptr) {}
    };

    Node* topNode;
    int stackSize;
};
