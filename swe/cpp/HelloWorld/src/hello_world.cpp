#include <iostream> 
// Preprocessor statement - Gets evaluated before the file.
// include copypastes code from whatever is being included
#include <printing.h> //has declarations for function print_number()



// Main function is the entry point to the APPLICATION
int main(){ 
    std::cout<<"Number is: ";
    print_number(2);
    std::cout<<std::endl;
    return 0;
}