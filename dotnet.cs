using System;

public static class main {

	private delegate void Event(string str);
	
	private static void MyName(string str) {
		Console.WriteLine(string.Format("My name is {0}.", str));
	}
	
	private static event Event Callees;
	
    public static void Main(string[] args) {
		
		Callees += delegate(string str) { Console.WriteLine("a"); };
		Callees += MyName;
		Callees += delegate(string str) { Console.WriteLine("b"); };
		Callees += MyName;
		Callees += delegate(string str) { Console.WriteLine("c"); };
		Callees -= MyName; // Removes the last instance
		Callees += delegate(string str) { Console.WriteLine("d"); };
		
		Callees("Gerard");
    }
}
