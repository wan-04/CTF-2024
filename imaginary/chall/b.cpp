#include <iostream>
#include <string>
#include <thread>
#include <mutex>
#include <iomanip>
#include <openssl/sha.h>
#include <vector>
std::mutex mtx;
bool found = false;
unsigned int totalIterations = 0xffffffff;  // Số lần lặp tối đa
std::string targetHash = "cbd4cdd046820600f68ff86ea41e35c46653c14564ec0e9571c00e0eed913b97";
std::string suffix = "g4feS8TH0uUpPWKlkBsc0/LUz1WmO4Nt";

std::string sha256(const std::string& str) {
    unsigned char hash[SHA256_DIGEST_LENGTH];
    SHA256_CTX sha256;
    SHA256_Init(&sha256);
    SHA256_Update(&sha256, str.c_str(), str.size());
    SHA256_Final(hash, &sha256);

    std::stringstream ss;
    for (int i = 0; i < SHA256_DIGEST_LENGTH; ++i) {
        ss << std::hex << std::setw(2) << std::setfill('0') << (int)hash[i];
    }

    return ss.str();
}

void findXXXX(unsigned int start, unsigned int end) {
    unsigned int chunkSize = end - start;
    unsigned int progress = 0;

    for (unsigned int XXXX = start; XXXX < end; ++XXXX) {
        std::string value = std::to_string(XXXX);
        std::string hashInput = value + suffix;
        std::string hashedValue = sha256(hashInput);

        if (hashedValue == targetHash) {
            std::lock_guard<std::mutex> lock(mtx);
            found = true;
            break;
        }

        // Cập nhật tiến trình
        std::lock_guard<std::mutex> lock(mtx);
        ++progress;
        std::cout << "Thread " << std::this_thread::get_id() << ": "
                  << std::fixed << std::setprecision(2)
                  << static_cast<double>(progress) / chunkSize * 100 << "%\r";
        std::cout.flush();
    }
}

int main() {
    unsigned int numThreads = std::thread::hardware_concurrency();  // Số lượng luồng tối đa

    std::vector<std::thread> threads;

    unsigned int chunkSize = totalIterations / numThreads;
    unsigned int start = 0;
    unsigned int end = chunkSize;

    // Tạo và khởi động các luồng
    for (unsigned int i = 0; i < numThreads; ++i) {
        if (i == numThreads - 1) {
            end = totalIterations;  // Luồng cuối cùng xử lý phần còn lại
        }

        threads.emplace_back(findXXXX, start, end);

        start = end;
        end += chunkSize;
    }

    // Chờ tất cả các luồng kết thúc
    for (auto& thread : threads) {
        thread.join();
    }

    std::cout << std::endl;

    if (found) {
        std::cout << "Tìm thấy giá trị XXXX!" << std::endl;
    } else {
        std::cout << "Không tìm thấy giá trị XXXX sau " << totalIterations << " lần lặp." << std::endl;
    }

    return 0;
}