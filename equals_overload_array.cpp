#include <array>
#include <iostream>


// Operator overload already exists. Overloading in a namespace
// allows a non ambiguous call.
namespace gerard {
    
template <typename T, size_t S>
std::array<bool, S> operator==(const std::array<T, S>& l, const std::array<T, S>& r) {

    std::array<bool, S> res;
    
    for(size_t i = 0; i < S; ++i) {
        res[i] = l[i] == r[i];
    }

    return res;    
}

}

int main() {

    std::array<float, 4> a{0.f, 0.f, 8.f, 9.f};
    std::array<decltype(a)::value_type, a.size()> b{0.f, 3.1415f, 8.f, 0.f};    
    
    auto res = gerard::operator==(a, b);
    
    std::cout << std::boolalpha;
    
    for(auto r : res) {
        std::cout << r << std::endl;
    }
}
