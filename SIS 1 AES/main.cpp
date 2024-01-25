#include <iostream>

#include "AES.cpp"

using namespace std;

void phex(unsigned char x){
    cout << hex << (x>>4) << (x&15) << dec;
}

int main(){
    string sdata = "1";
    vector<unsigned char> data(sdata.begin(), sdata.end());
    string skey = "1a3d2sa1d3a4sd64";
    array<unsigned char, 16> key;
    for(int i = 0; i < 16; i++) key[i] = skey[i];

    auto res = AES::AES128(key).encrypt(data);
    cout << "Data:   "; for(auto x : data) phex(x); cout << '\n';
    cout << "Key:    "; for(auto x : key) phex(x); cout << '\n';
    cout << "Result: "; for(auto x : res) phex(x); cout << '\n';

    return 0;
}