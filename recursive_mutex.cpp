#include <iostream>
#include <mutex>
#include <thread>
#include <chrono>

void recurse(const std::string& ident, int depth) {

	static std::recursive_mutex mutex;
	
	
	if(depth > 0) {
		
		mutex.lock();
		
		std::this_thread::yield();
		std::this_thread::sleep_for(std::chrono::milliseconds(100));
	
		std::cout << "at depth " << depth << " for ident " << ident << std::endl;
	
		recurse(ident, depth - 1);	
	
		mutex.unlock();	
	}
}


int main() {
	
    std::function<void()> a = std::bind(recurse, "a", 9);
    std::function<void()> b = std::bind(recurse, "b", 9);
    std::function<void()> c = std::bind(recurse, "c", 9);
	
	std::thread u(a);
	std::thread v(b);
	std::thread w(c);
	
	u.join();
	v.join();
	w.join();
}