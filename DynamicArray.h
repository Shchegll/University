#pragma once

#include <iostream>

template <typename T>
class DynamicArray {
public:
    DynamicArray() {
        capacity = 10;
        data = new T[capacity];
        currSize = 0;
    }

    ~DynamicArray() {
        delete[] data;
    }

    void resize() {
        int newCapacity = capacity * 2;
        T* newData = new T[newCapacity];
        for (int i = 0; i < currSize; i++) {
            newData[i] = data[i];
        }
        delete[] data;
        data = newData;
        capacity = newCapacity;
    }

    void add(const T& value) {
        if (currSize >= capacity) {
            resize();
        }
        data[currSize++] = value;
    }

    void set(int index, const T& value) {
        if (index < 0 || index >= currSize) {
            std::cerr << "Oshibka: invalid index" << std::endl;
        }
        data[index] = value;
    }

    T get(int index) {
        if (index < 0 || index >= currSize) {
            std::cerr << "Oshibka: invalid index. Code ";
            return -1;
        }
        return data[index];
    }

    void remove(int index) {
        if (index < 0 || index >= currSize) {
            std::cerr << "Oshibka: invalid index" << std::endl;
            return;
        }

        for (int i = index; i < currSize - 1; i++) {
            data[i] = data[i + 1];
        }
        currSize--;
    }

    int size() {
        return currSize;
    }

private:
    T* data;
    int capacity;
    int currSize;
};
