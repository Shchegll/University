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

void merge(DynamicArray<int>& mass, int l, int m, int r)
{
    int* Left = new int[m - l + 1];
    int* Right = new int[r - m];
    for (int i = 0; i < m - l + 1; i++)
        Left[i] = mass[l + i];
    for (int i = 0; i < r - m; i++)
        Right[i] = mass[m + 1 + i];
    int i = 0, j = 0, k = l, testL = 0, testR = 0;
    while (i < m - l + 1 && j < r - m)
    {
        if (Left[i] <= Right[j]) {
            mass[k] = Left[i];
            i++;
            testL++;
            testR = 0;
        }
        else {
            mass[k] = Right[j];
            j++;
            testR++;
            testL = 0;
        }
        k++;
    }

    if (testL >= 7)  //галоп начинается тут, после того как из массива Left были взяты 7 раз элементы
    {
        int gallopStep = 1;
        bool col_mass_bro = 1;
        for (int g = i; g < m - l + 1;)
        {
            if (Left[g] <= Right[j])
            {
                g += gallopStep;
                gallopStep *= 2;
            }
            else
            {
                col_mass_bro = 0;
                testL = 0;
                testR = 0;
            }
        }
        if (col_mass_bro)
        {
            for (int g = 0; g < m - l + 1; g++)
            {
                mass[k] = Left[g];
                k++;
                i++;
                testL = 0;
                testR = 0;
            }
        }
    }
    else if (testR >= 7) //галоп начинается тут
    {
        int gallopStep = 1;
        bool col_mass_bro = 1;
        for (int g = i; g < r - m;)
        {
            if (Right[g] <= Left[i])
            {
                g += gallopStep;
                gallopStep *= 2;
            }
            else
            {
                col_mass_bro = 0;
                testL = 0;
                testR = 0;
            }
        }
        if (col_mass_bro)
        {
            for (int g = 0; g < r - m; g++)
            {
                mass[k] = Left[g];
                k++;
                j++;
                testL = 0;
                testR = 0;
            }
        }
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

