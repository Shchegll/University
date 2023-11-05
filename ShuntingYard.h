#include "DoubleLinkedList.h"
#include "Stack.h"
#include <string>
#include <iostream>

class ReversePolishNotation {
public:
    ReversePolishNotation() {}

    std::string infixToPostfix(const std::string& infixExpression) {
        std::string postfix;
        operatorStack = Stack<std::string>();
        DoubleLinkedList<std::string> tokens = tokenize(infixExpression);

        for (size_t i = 0; i < tokens.getLength(); i++) {
            std::string token = tokens.get(i);
            if (isdigit(token[0])) {
                postfix += token + " ";
            }
            else if (isOperator(token)) {
                while (!operatorStack.isEmpty() && getOperatorPriority(token) <= getOperatorPriority(operatorStack.top())) {
                    postfix += operatorStack.pop();
                    postfix += " ";
                }
                operatorStack.push(token); // Добавляем полное имя функции или оператор
            }
            else if (token == "(") {
                operatorStack.push("(");
            }
            else if (token == ")") {
                while (!operatorStack.isEmpty() && operatorStack.top() != "(") {
                    postfix += operatorStack.pop();
                    postfix += " ";
                }
                operatorStack.pop();  // Удаляем открывающую скобку
            }
        }

        while (!operatorStack.isEmpty()) {
            postfix += operatorStack.pop();
            postfix += " ";
        }

        return postfix;
    }

    double evaluatePostfix(const std::string& postfixExpression) {
        Stack<double> operandStack;
        DoubleLinkedList<std::string> tokens = tokenize(postfixExpression);

        for (size_t i = 0; i < tokens.getLength(); i++) {
            std::string token = tokens.get(i);
            if (isdigit(token[0])) {
                operandStack.push(std::stod(token));
            }
            else if (isOperator(token)) {
                if (token.length() == 1) {
                    // Для обычных бинарных операторов
                    double operand2 = operandStack.pop();
                    double operand1 = operandStack.pop();
                    double result = applyOperator(operand1, operand2, token[0]);
                    operandStack.push(result);
                }
                else {
                    // Унарные операторы (например, cos, sin)
                    double operand = operandStack.pop();
                    double result = applyUnaryOperator(operand, token);
                    operandStack.push(result);
                }
            }
        }

        if (operandStack.isEmpty()) {
            std::cerr << "Ошибка: невозможно вычислить результат" << std::endl;
            return 0.0; // Возврат значения по умолчанию
        }

        return operandStack.top(); // Возвращаем верхний элемент стека с результатом
    }

private:
    bool isOperator(const std::string& token) const {
        return token == "+" || token == "-" || token == "*" || token == "/" || token == "^" || token == "sin" || token == "cos";
    }

    int getOperatorPriority(const std::string& op) const {
        if (op == "+" || op == "-") {
            return 1;
        }
        else if (op == "*" || op == "/") {
            return 2;
        }
        else if (op == "^") {
            return 3;
        }
        else if (op == "sin" || op == "cos") {
            return 4; // Приоритет унарных операторов (косинус и синус)
        }
        return 0;
    }

    double applyOperator(double operand1, double operand2, char op) const {
        switch (op) {
        case '+':
            return operand1 + operand2;
        case '-':
            return operand1 - operand2;
        case '*':
            return operand1 * operand2;
        case '/':
            return operand1 / operand2;
        case '^':
            return std::pow(operand1, operand2);
        default:
            return 0.0;
        }
    }

    double applyUnaryOperator(double operand, const std::string& op) const {
        if (op == "sin") {
            return std::sin(operand);
        }
        else if (op == "cos") {
            return std::cos(operand);
        }
        return 0.0;
    }

    DoubleLinkedList<std::string> tokenize(const std::string& expression) {
        DoubleLinkedList<std::string> tokens;
        std::string token;

        for (size_t i = 0; i < expression.size(); i++) {
            char c = expression[i];
            if (std::isspace(c)) {
                if (!token.empty()) {
                    if (isOperator(token)) {
                        tokens.append(token);
                    }
                    else {
                        tokens.append(token);
                    }
                    token.clear();
                }
            }
            else if (c == '(' || c == ')') {
                if (!token.empty()) {
                    tokens.append(token);
                    token.clear();
                }
                tokens.append(std::string(1, c));
            }
            else {
                token += c;
                if (isOperator(token) && (i + 1) < expression.size() && expression[i + 1] != '(') {
                    tokens.append(token);
                    token.clear();
                }
            }
        }

        if (!token.empty()) {
            if (isOperator(token)) {
                tokens.append(token);
            }
            else {
                tokens.append(token);
            }
        }

        return tokens;
    }

    Stack<std::string> operatorStack;
};
