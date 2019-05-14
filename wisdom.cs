using System;


public class Program {
	public static void Main(string[] args) {
		
		bool result = true;
		
		result &= BooleanFunction("a", true);
		result &= BooleanFunction("b", true);
		result &= BooleanFunction("c", true);
		
		System.Console.WriteLine(string.Format("Final boolean result: {0}", result));
	}
	
	private static bool BooleanFunction(string name, bool outcome) {
		System.Console.WriteLine(string.Format("BooleanFunction({0})", name));
		
		return outcome;
	}
}