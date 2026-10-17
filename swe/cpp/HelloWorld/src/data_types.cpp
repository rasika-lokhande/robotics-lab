#include <iostream>


using namespace std;
void dtypes(){
    char name = 65; //will print A
    char name2 = 1;
    int num = 65; //will print 65
    int new_num = 'A'; // will print value of with A , =65
    cout<< name << endl;
    cout<< name2 << endl;
    cout<< num << endl;
    cout<< new_num << endl;

    char sum_of_char = name2 + name; // 65 + 1 = 66 = B
    int  sum_of_char2 = name2 + name;
    cout << sum_of_char << endl;
    cout << sum_of_char2 << endl;


    float var = 3.1f;
    double var2 = 3.1;
    cout << var << " " << var2 << endl;


    bool b = true;
    cout<< b<< endl;


    cout << sizeof(int) <<endl;
    name = 66;


    const char* string = "Hey";
    cout<< string <<endl;

}

// int main(){
//     dtypes();
// }