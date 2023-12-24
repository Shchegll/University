#include <iostream>
#include <Stack.h>

using namespace std;

const int MIN_RUN = 32;

void insertionSort(int* arr, int left, int right) {
    for (int i = left + 1; i <= right; i++) {
        int key = arr[i];
        int j = i - 1;
        while (j >= left && arr[j] > key) {
            arr[j + 1] = arr[j];
            j--;
        }
        arr[j + 1] = key;
    }
}

void merge(int* arr, int start, int mid, int end) {
    int len1 = mid - start + 1;
    int len2 = end - mid;
    int* left = new int[len1];
    int* right = new int[len2];

    for (int i = 0; i < len1; i++) {
        left[i] = arr[start + i];
    }
    for (int i = 0; i < len2; i++) {
        right[i] = arr[mid + 1 + i];
    }

    int i = 0, j = 0, k = start;

    while (i < len1 && j < len2) {
        if (left[i] <= right[j]) {
            arr[k] = left[i];
            i++;
        }
        else {
            arr[k] = right[j];
            j++;
        }
        k++;
    }

    while (i < len1) {
        arr[k] = left[i];
        i++;
        k++;
    }

    while (j < len2) {
        arr[k] = right[j];
        j++;
        k++;
    }

    delete[] left;
    delete[] right;
}

void timSort(int* arr, int n) {
    Stack<pair<int, int>> Stack;

    for (int i = 0; i < n; i += MIN_RUN) {
        insertionSort(arr, i, min(i + MIN_RUN - 1, n - 1));
        Stack.push(make_pair(i, min(i + MIN_RUN - 1, n - 1)));
    }

    while (Stack.size() > 1) {
        int start1, end1, start2, end2;
        end1 = Stack.top().second;
        Stack.pop();
        start1 = Stack.top().first;
        end2 = start1 - 1;
        Stack.pop();
        start2 = Stack.isEmpty() ? 0 : Stack.top().first;
        merge(arr, start2, end2, end1);
        Stack.push(make_pair(start2, end1));
    }
}

int main() {
    int arr[] = { 9, 2, 5, 1, 7, 4, 8, 3, 6, 4, 7, 9, 67, 48, 29, 29, 5, 7, 9, 2, 11, 25, 42, 65, 28, 1, 92, 19, 34, 73, 85, 47, 92, 34, 21, 23, 43, 21 };
    int n = sizeof(arr) / sizeof(arr[0]);
    cout << "Before sorting: ";
    for (int i = 0; i < n; i++) {
        cout << arr[i] << " ";
    }
    cout << endl;

    timSort(arr, n);

    cout << "After sorting: ";
    for (int i = 0; i < n; i++) {
        cout << arr[i] << " ";
    }
    cout << endl;

    return 0;
}

