#include <iostream>
#include <fstream>
#include <vector>
#include <random>
#include <string>
#include "AES.cpp"

using namespace std;

void phex(unsigned char x){
    cout << hex << (x>>4) << (x&15) << dec;
}

int main(int argc, char* argv[]){
    vector<unsigned char> res;
    array<unsigned char, 16> key;
    string wtf;

    cout << "What do you wanna do with data? (enc or dec): " << wtf << " ";
    cin >> wtf;

 
    // Check filename
    if (argc != 3) {
        cerr << "Usage: " << argv[0] << " <input_file> <output_file>" << endl;
        return 1;
    }


    // Reading a data from file
    ifstream inputFile(argv[1], ios::binary);
    if (!inputFile) {
        cerr << "Error: Unable to open input file." << endl;
        return 1;
    }

    vector<unsigned char> data((istreambuf_iterator<char>(inputFile)), istreambuf_iterator<char>());
    inputFile.close();

    if(wtf == "enc") {
        
        // Creating key generator
        random_device rd;  // a seed source for the random number engine
        mt19937 gen(rd()); // mersenne_twister_engine seeded with rd()
        uniform_int_distribution<> distrib(0, 255);
        
        for(int i = 0; i < 16; i++) {
            key[i] = distrib(gen);
        }

        ofstream outputFile("key.txt", ios::binary);
        if (!outputFile) {
            cerr << "Error: Unable to open output file." << endl;
            return 1;
        }
        outputFile.write(reinterpret_cast<const char*>(key.data()), key.size());
        size_t data_size = data.size();
        cout << "DATA SIZE: " << data_size << '\n';
        outputFile.write(reinterpret_cast<const char*>(&data_size), sizeof(data_size));
        outputFile.close();

        // Encryption
        res = AES::AES128(key).encrypt(data);
        cout << "Encryption completed successfully." << endl;
    } else {
        ifstream inputFile("key.txt", ios::binary);
        // Checking to correctly opens
        if (!inputFile) {
            cerr << "Error: Unable to open the file." << endl;
            return 1;
        }
        
        inputFile.read(reinterpret_cast<char*>(key.data()), key.size());
        size_t data_size = 0;
        inputFile.read(reinterpret_cast<char*>(&data_size), sizeof(data_size));
        cout << "DATA SIZE: " << data_size << '\n';
        inputFile.close();

        //Decryption
        res = AES::AES128(key).decrypt(data);
        res.resize(data_size);
        cout << "Decryption completed successfully." << endl;
    }

    // Record the data
    ofstream outputFile(argv[2], ios::binary);
    if (!outputFile) {
        cerr << "Error: Unable to open output file." << endl;
        return 1;
    }

    outputFile.write(reinterpret_cast<const char*>(res.data()), res.size());
    outputFile.close();

    // cout << "Data:   "; for(auto x : data) phex(x); cout << '\n';
    cout << "Key:    "; for(auto x : key) phex(x); cout << '\n';
    // cout << "Result: "; for(auto x : res) phex(x); cout << '\n';

    return 0;
}