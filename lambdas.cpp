#include <cstdlib>
#include <iostream>
#include <functional>

using namespace std;

// http://en.cppreference.com/w/cpp/language/lambda

int main(int argc, char** argv) {
    // Completely inline:
    [] () {
        cout << "I'm so inline. " << endl;
    }();

    // Not using the auto keyword, great if you want to pass an anonymous
    // function as argument, imo this is also more human readable than function
    // pointers.
    std::function<int(int, int)> multiply = [] (int a, int b) -> int {
        int result = a * b;
        cout << "multiplied: " << result << endl;
        return result;
    };
    multiply(24, 3);


    // Ok, with function pointer:
    void (*fPointer) () = [] () {
        cout << "Function pointer syntax!" << endl;
    };
    fPointer();

    // Works with auto, too:
    auto withAuto = [] () {
        cout << "Auto makes life easier." << endl;
    };
    withAuto();

    // Ok, note the ampersand I've added. This lets you write javascript style
    // code in C++. Amazing. The ampersand actually brings everything in scope
    // as a reference, there are other options, too. So examples below when I
    // test pass by value.
    int number = 42;
    [&] () {
        cout << "Number: " << number << endl;
    }();


    // Explicitly capture the return value:
    int bar1  = [] () -> int { return 12; }();
    // Implicitly capture return value:
    int bar2  = [] () { return 13; }();
    // Implicitly inferred capture of return value:
    auto bar3 = [] () { return 14; }();

    cout << bar1 << " " << bar2 << " " << bar3 << endl;




    // OK, let's test some scoping:
    std::function<void(int)> functions[10];

    for(int i = 0; i < 10; ++i) {
        // Note how I is passed as value.
        functions[i] = [i] (int index) {
            cout << "The value of i is " << i << ". At index:" << index << endl;
        };

        // Reminder: this compiles, but passes i as reference. This is
        // generally how it works with a language such as JavaScript and is
        // usually undesirable:
        // functions[i] = [&] (int index) {
        // functions[i] = [&i] (int index) { // <-- same deal.
    }

    for(int j = 0; j < 10; ++j) {
        functions[j](j);
    }


    // Mutable, per default it would appear that pass-by-value is done via const.
    // Due to copy semantics, this is generally OK. But in case you work with anything
    // but a POD:
    std::string str;
    [str] () mutable -> std::string {
        return str += " concatenating";
    }();

    return 0;
}
