#include <iostream>
#include <queue>
#include <Stack.h>
#include <fstream>
#include <string>

using namespace std;

struct Node {
    Node* left;
    Node* right;
    int data;

    Node(int element)
    {
        data = element;
        this->left = nullptr;
        this->right = nullptr;
    }
};

void preorder(Node* root)
{
    if (!root)
        return;

    cout << root->data << " ";
    preorder(root->left);
    preorder(root->right);
}

Node* constructTree(string s)
{
    Node* root = new Node(s[0] - '0');
    stack<Node*> stk;

    for (int i = 1; i < s.length(); i++) {
        if (s[i] == '(') {
            stk.push(root);
        }
        else if (s[i] == ')') {
            root = stk.top();
            stk.pop();
        }
        else {
            if (root->left == nullptr) {
                Node* left = new Node(s[i] - '0');
                root->left = left;
                root = root->left;
            }
            else if (root->right == nullptr) {
                Node* right = new Node(s[i] - '0');
                root->right = right;
                root = root->right;
            }
        }
    }

    return root;
}

void printBreadthFirst(Node* root) {
    if (root == nullptr) {
        return;
    }

    queue<Node*> q;
    q.push(root);

    while (!q.empty()) {
        Node* curr = q.front();
        q.pop();
        cout << curr->data << " ";

        if (curr->left != nullptr) {
            q.push(curr->left);
        }
        if (curr->right != nullptr) {
            q.push(curr->right);
        }
    }

    cout << endl;
}

void printPreorder(Node* root) {
    if (root == nullptr) {
        return;
    }

    cout << root->data << " ";
    printPreorder(root->left);
    printPreorder(root->right);
}

void printInorder(Node* root) {
    if (root == nullptr) {
        return;
    }

    printInorder(root->left);
    cout << root->data << " ";
    printInorder(root->right);
}

void printPostorder(Node* root) {
    if (root == nullptr) {
        return;
    }

    printPostorder(root->left);
    printPostorder(root->right);
    cout << root->data << " ";
}


int main()
{
    setlocale(LC_ALL, "Russian");

    ifstream File("input.txt");

    if (!File.is_open()) {
        cout << "Îøèáêà îòêðûòèÿ ôàéëà." << endl;
        return 1;
    }

    string expression;
    getline(File, expression);

    File.close();

    cout << "Òî÷íàÿ çàïèñü: " << expression << endl;;


    cout << "Ñ÷èòûâàíèå ôàéëà: ";
    Node* root = constructTree(expression);
    preorder(root);
    cout << endl;

    cout << "Îáõîä â øèðèíó: ";
    printBreadthFirst(root);

    cout << "Ïðåôèêñíûé îáõîä: ";
    printPreorder(root);
    cout << endl;

    cout << "Èíôèêñíûé îáõîä: ";
    printInorder(root);
    cout << endl;

    cout << "Ïîñòôèêñíûé îáõîä: ";
    printPostorder(root);
    cout << endl;

    return 0;
}
