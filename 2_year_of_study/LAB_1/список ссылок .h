#pragma once

#include <iostream>

template <typename T>
class DoubleLinkedList {
public:
    DoubleLinkedList() : head(nullptr), tail(nullptr), length(0) {}

    ~DoubleLinkedList() {
        while (head) {
            Node* temp = head;
            head = head->next;
            delete temp;
        }
    }

    int getLength() const {
        return length;
    }

    void insertAt(const T& item, int index) {
        if (index < 0 || index > length) {
            std::cerr << "Oshibka: invalid index" << std::endl;
            return;
        }

        Node* newNode = new Node(item);

        if (index <= length / 2) {
            if (index == 0) {
                newNode->next = head;
                if (head) head->prev = newNode;
                head = newNode;
                if (!tail) tail = head;
            }
            else {
                Node* curr = head;
                for (int i = 0; i < index; i++) {
                    curr = curr->next;
                }
                newNode->next = curr;
                newNode->prev = curr->prev;
                curr->prev->next = newNode;
                curr->prev = newNode;
            }
        }
        else {
            if (index == length) {
                newNode->prev = tail;
                tail->next = newNode;
                tail = newNode;
            }
            else {
                Node* curr = tail;
                for (int i = length - 1; i > index; i--) {
                    curr = curr->prev;
                }
                newNode->next = curr;
                newNode->prev = curr->prev;
                curr->prev->next = newNode;
                curr->prev = newNode;
            }
        }

        length++;
    }

    T remove(const T& item) {
        Node* curr = head;
        while (curr) {
            if (curr->data == item) {
                if (curr == head) {
                    head = curr->next;
                    if (head) head->prev = nullptr;
                }
                else {
                    curr->prev->next = curr->next;
                }
                if (curr == tail) {
                    tail = curr->prev;
                    if (tail) tail->next = nullptr;
                }
                else {
                    curr->next->prev = curr->prev;
                }
                T value = curr->data;
                delete curr;
                length--;
                return value;
            }
            curr = curr->next;
        }
        return T();
    }

    T removeAt(int index) {
        if (index < 0 || index >= length) {
            std::cerr << "Oshibka: invalid index. Code ";
            return -1;
        }

        if (index == 0) {
            T value = removeFirst();
            return value;
        }
        else if (index == length - 1) {
            T value = removeLast();
            return value;
        }

        if (index <= length / 2) {
            Node* curr = head;
            for (int i = 0; i < index; i++) {
                curr = curr->next;
            }
            curr->prev->next = curr->next;
            curr->next->prev = curr->prev;
            T value = curr->data;
            delete curr;
            length--;
            return value;
        }
        else {
            Node* curr = tail;
            for (int i = length - 1; i > index; i--) {
                curr = curr->prev;
            }
            curr->prev->next = curr->next;
            curr->next->prev = curr->prev;
            T value = curr->data;
            delete curr;
            length--;
            return value;
        }
    }

    void append(const T& item) {
        insertAt(item, length);
    }

    void prepend(const T& item) {
        insertAt(item, 0);
    }

    T get(int index) const {
        if (index < 0 || index >= length) {
            std::cerr << "Oshibka: invalid index. Code ";
            return T();
        }

        if (index < length / 2) {
            Node* curr = head;
            for (int i = 0; i < index; i++) {
                curr = curr->next;
            }
            return curr->data;
        }
        else {
            Node* curr = tail;
            for (int i = length - 1; i > index; i--) {
                curr = curr->prev;
            }
            return curr->data;
        }
    }

    void display() const {
        Node* curr = head;
        while (curr) {
            std::cout << curr->data << " ";
            curr = curr->next;
        }
        std::cout << std::endl;
    }

    T removeFirst() {
        if (length == 0) {
            std::cerr << "Oshibka: list is empty. Code ";
            return -1;
        }
        Node* front = head;
        T value = front->data;
        head = head->next;
        if (head) {
            head->prev = nullptr;
        }
        delete front;
        length--;
        return value;
    }

    T removeLast() {
        if (length == 0) {
            std::cerr << "Oshibka: list is empty. Code ";
            return -1;
        }
        Node* back = tail;
        T value = back->data;
        tail = tail->prev;
        if (tail) {
            tail->next = nullptr;
        }
        delete back;
        length--;
        return value;
    }


private:
    struct Node {
        T data;
        Node* prev;
        Node* next;
        Node(const T& item) : data(item), prev(nullptr), next(nullptr) {}
    };

    Node* head;
    Node* tail;
    int length;
};
