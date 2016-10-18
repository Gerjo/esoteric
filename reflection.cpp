#include <cstdlib>
#include <iostream>

using namespace std;


class Bar {
public:
    Bar(std::string thoughts) : _thoughts(thoughts) {

    }

    void foo(void) {
        cout << "Foolicious: " << _thoughts << endl;
    }

private:
    std::string _thoughts;
};


int main(int argc, char** argv) {
    
    // Pointer to method:
    void (Bar::* method) (void) = &Bar::foo;

    // Works for stack:
    Bar bar("Quite indeed.");
    (bar.*method)();

    // Works for heap:
    Bar* barPointer = new Bar("You are wrong.");
    (barPointer->*method)();


    // Now we've got that covered: How about using the auto keyword?
    auto method2 = &Bar::foo;
    (bar.*method2)();

    // No memory leakage in this example.
    delete barPointer;

    return 0;
}

