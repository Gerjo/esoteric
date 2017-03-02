#include <iostream>
#include <cassert>

struct Counter {
	int count{0};
		
	void retain() {
		++count;
	}
	
	void release() {
		--count;
	}
	
	int get() {
		return count;
	}
};


struct Left : public virtual Counter {};

struct Right : public virtual Counter {};

struct Coupler: public Left, public Right {
	Coupler() : Left(), Right() {
		Left::count = -4;
		Right::count = 2;
		
		assert(Left::count == Right::count);
	}
};

int main() {
	std::cout << "Testing virtual inheritance.\n" << std::endl;
	
	Coupler c;
	Left& l = c;
	Left& r = c;
	
	std::cout << "(1.a) Counter getter: " << c.get() << std::endl;
	std::cout << "(1.b) Counter value : " << c.count << std::endl;
	assert(c.get() == c.count);
	
	l.retain();
	r.retain();
	c.retain();
	c.release();
	
	std::cout << "(2.a) Counter getter: " << c.get() << std::endl;
	std::cout << "(2.b) Counter value : " << c.count << std::endl;
	assert(c.get() == c.count);
	
	l.count = 10;
	r.count = 14;
	
	std::cout << "(3.a) Left value : " << l.count << std::endl;
	std::cout << "(3.b) Right value: " << r.count << std::endl;	
	assert(l.count == r.count);
	
	std::cout << "(4.a) Left value ptr : " << &l.count << std::endl;
	std::cout << "(4.b) Right value ptr: " << &r.count << std::endl;
	assert(&l.count ==  &l.count);
}