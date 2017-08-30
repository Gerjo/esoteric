using System;


public class Message {
	public readonly string ident;
	
	public Message(string ident) {
		this.ident = ident;
	}
}

public class NumberMessage : Message {
	public readonly int number;
	
	public NumberMessage(int number) : base("number") {
		this.number = number;
	}
}

public class BoolMessage : Message {
	public readonly bool flag;
	
	public BoolMessage(bool flag) : base("bool-flag") {
		this.flag = flag;
	}
}

public interface Listener<T> where T : Message {
	void Accept(T message);
}

public class MyListener : Listener<NumberMessage>, Listener<Message> {
	public static void Main() {
		Console.WriteLine("Application started");
		
		MyListener listener = new MyListener();
		
		listener.Accept(new NumberMessage(1987));
		listener.Accept(new Message("november"));
		
		// Calls the generic Accept(Message)
		listener.Accept(new BoolMessage(true));
	}
	
	public void Accept(NumberMessage message) {
		Console.WriteLine("Message with number received.");
	}
	
	public void Accept(Message message) {
		Console.WriteLine("Message with no number received.");
	}
}
