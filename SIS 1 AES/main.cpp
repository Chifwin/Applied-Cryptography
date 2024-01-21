#include <iostream>

#include "AES.cpp"

using namespace std;

char h[17] = "0123456789abcdef";
void phex(unsigned char x){
    cout << h[x>>4] << h[x&15];
}

int main(){
    string sdata = "da1s21asd4a6s5d4as87d98ad465465;15465op46[51;l2/13.2,1/32/.4l654;l4;l;9l8;79l8;42d13as1d32asd5a]";
    vector<unsigned char> data(sdata.begin(), sdata.end());
    string skey = "1a3d2sa1d3a4sd64";
    array<unsigned char, 16> key;
    for(int i = 0; i < 16; i++) key[i] = skey[i];

    AES::AES128 aes(key);
    auto res = aes.encrypt(data);
    for(auto x : data) phex(x); cout << '\n';
    for(auto x : key) phex(x); cout << '\n';
    for(auto x : res) phex(x); cout << '\n';

    return 0;
}