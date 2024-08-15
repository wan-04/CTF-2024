#include <iostream>

int main() {
    const long long size = 250000000000; // Number of elements
    const int chunkSize = 1000000; // Number of elements in each chunk

    // Calculate the number of chunks required
    const int numChunks = size / chunkSize + (size % chunkSize != 0);

    // Allocate memory for each chunk
    for (int chunk = 0; chunk < numChunks; ++chunk) {
        // Calculate the size of the current chunk
        const int currentSize = (chunk == numChunks - 1) ? size % chunkSize : chunkSize;

        // Dynamically allocate memory for the chunk
        int* data = new int[currentSize];

        // Use the chunk for processing or storage

        // Deallocate memory for the chunk
        delete[] data;
    }

    return 0;
}