#include <iostream>
#include "ShuntingYard.h"
#include "DynamicArray.h"

int main() {
    while (true) {
        std::cout << "1. List" << std::endl;
        std::cout << "2. Array" << std::endl;
        std::cout << "3. Stack" << std::endl;
        std::cout << "3. ShuntingYard" << std::endl;
        std::cout << "5. Exit" << std::endl;

        int choice;
        std::cout << "Enter ur choise: ";
        std::cin >> choice;
        std::cout << std::endl;

        switch (choice) {
        case 1: {
            DoubleLinkedList<int> list;
            list.append(1);
            list.append(2);
            list.prepend(0);
            list.insertAt(3, 1);

            list.display(); // Ожидаемый вывод: 0 3 1 2

            int removedValue = list.remove(3);
            std::cout << "Removed value: " << removedValue << std::endl; // Ожидаемый вывод: 3

            list.display(); // Ожидаемый вывод: 0 1 2
            break;
        }
        case 2: {

            //      ПРОВЕРКА ДИН. МАССИВА
            DynamicArray<int> dynamicArray;

            // Добавление элементов в массив
            dynamicArray.add(1);
            dynamicArray.add(2);
            dynamicArray.add(3);

            // Получение элементов по индексу
            std::cout << "Element at index 0: " << dynamicArray.get(0) << std::endl;
            std::cout << "Element at index 1: " << dynamicArray.get(1) << std::endl;
            std::cout << "Element at index 2: " << dynamicArray.get(2) << std::endl;

            // Изменение элемента по индексу
            dynamicArray.set(1, 4);

            // Удаление элемента
            dynamicArray.remove(0);

            std::cout << "Element at index 0: " << dynamicArray.get(0) << std::endl;
            std::cout << "Element at index 1: " << dynamicArray.get(1) << std::endl;
            std::cout << "Element at index 2: " << dynamicArray.get(2) << std::endl;

            // Вывод размера массива
            std::cout << "Array size: " << dynamicArray.size() << std::endl;
            break;
        }
        case 3: {
            //  ПРОВЕРКА СТЕКА

            Stack<int> stack;

            // Добавление элементов в стек
            stack.push(1);
            stack.push(2);
            stack.push(3);
            std::cout << "Stack size: " << stack.size() << std::endl;

            // Вывод верхнего элемента
            std::cout << "Top element: " << stack.top() << std::endl;

            while (!stack.isEmpty()) {
                std::cout << "Popped element: " << stack.pop() << std::endl;
            }

            std::cout << "Stack size: " << stack.size() << std::endl;
            std::cout << "Top element: " << stack.top() << std::endl;
            break;
        }
        case 4: {
            ReversePolishNotation rpn;

            std::string infixExpression = "25 + sin(20)";
            std::string postfixExpression = rpn.infixToPostfix(infixExpression);
            std::cout << "Before: " << postfixExpression << std::endl;

            double result = rpn.evaluatePostfix(postfixExpression);
            std::cout << "After: " << result << std::endl;
            break;
        }
        case 5: {
            return 0;
        }
        }
    }
}