#include <iostream>
#include <fstream>
#include <vector>

#include "AES.cpp"

using namespace std;

void phex(unsigned char x){
    cout << hex << (x>>4) << (x&15) << dec;
}

int main(int argc, char* argv[]){
    {
        string sdata = "Blowfish";
        vector<unsigned char> data(sdata.begin(), sdata.end());
        string skey = "1a3d2sa1d3a4sd64";
        array<unsigned char, 16> key;
        for(int i = 0; i < 16; i++) key[i] = skey[i];

        auto res = AES::AES128(key).encrypt(data);
        // auto res_dec = AES::AES128(key).decrypt(data);
        // cout << "Data:   "; for(auto x : data) phex(x); cout << '\n';
        // cout << "Key:    "; for(auto x : key) phex(x); cout << '\n';
        // cout << "Result: "; for(auto x : res) phex(x); cout << '\n';
    }
    if (argc != 4) {
        cerr << "Usage: " << argv[0] << " <input_file> <output_file> <encryption_key>" << endl;
        return 1;
    }

    string skey = argv[3];
    array<unsigned char, 16> key;
    for(int i = 0; i < 16 && i < skey.size(); i++) {
        key[i] = skey[i];
    }

    // Чтение данных из файла
    ifstream inputFile(argv[1], ios::binary);
    if (!inputFile) {
        cerr << "Error: Unable to open input file." << endl;
        return 1;
    }

    vector<unsigned char> data((istreambuf_iterator<char>(inputFile)), istreambuf_iterator<char>());
    inputFile.close();

    // Шифрование данных
    auto res = AES::AES128(key).decrypt(data);
    // auto res = AES::AES128(key).encrypt(data);

    // Запись зашифрованных данных в файл
    ofstream outputFile(argv[2], ios::binary);
    if (!outputFile) {
        cerr << "Error: Unable to open output file." << endl;
        return 1;
    }

    outputFile.write(reinterpret_cast<const char*>(res.data()), res.size());
    outputFile.close();

    cout << "Encryption completed successfully." << endl;

    cout << "Data:   "; for(auto x : data) phex(x); cout << '\n';
    cout << "Key:    "; for(auto x : key) phex(x); cout << '\n';
    cout << "Result: "; for(auto x : res) phex(x); cout << '\n';

    return 0;
}