

import java.io.BufferedReader;
import java.io.BufferedWriter;

import java.io.InputStreamReader;
import java.io.OutputStreamWriter;

import java.net.InetSocketAddress;
import java.net.Socket;
import java.net.UnknownHostException;
import java.io.IOException;

import java.io.PrintWriter;

// Definir los siguientes parametros

// SERVER_IP, SERVERPORT


static public Socket connect_to_server(){
	
		Socket socket = new Socket();
		socket.connect(new InetSocketAddress(SERVER_IP, SERVERPORT), 3000);
		return socket;
}


static public void send_init(MyCallback callback){

	try {

	    Socket s = connect_to_server()
	    BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
	    PrintWriter out = new PrintWriter(new BufferedWriter(new OutputStreamWriter(socket.getOutputStream())), true);

	    out.print("init/state");
	    out.flush();

	    String status_string = in.readLine();

	    if(String(status_string).equals("on"))
	    	callback(true)

	   	else
	   		callback(false)
	    

	} catch (UnknownHostException e1) {
	    e1.printStackTrace();
	} catch (IOException e1) {
	    e1.printStackTrace();
	}

}

static public void send_on(MyCallback callback){
		try {

	    Socket s = connect_to_server()
	    BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
	    PrintWriter out = new PrintWriter(new BufferedWriter(new OutputStreamWriter(socket.getOutputStream())), true);

	    out.print("switch/on");
	    out.flush();

	    String status_string = in.readLine();

	    callback(true);

	} catch (UnknownHostException e1) {
	    e1.printStackTrace();
	} catch (IOException e1) {
	    e1.printStackTrace();
	}

}

static public void send_off(MyCallback callback){
	try {

	    Socket s = connect_to_server()
	    BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
	    PrintWriter out = new PrintWriter(new BufferedWriter(new OutputStreamWriter(socket.getOutputStream())), true);

	    out.print("switch/off");
	    out.flush();

	    String status_string = in.readLine();

	    callback(true);

	} catch (UnknownHostException e1) {
	    e1.printStackTrace();
	} catch (IOException e1) {
	    e1.printStackTrace();
	}

}

static public void add_program_switch(String name, String start_time, String stop_time, MyCallback callback ){
	try {

	    Socket s = connect_to_server()
	    BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
	    PrintWriter out = new PrintWriter(new BufferedWriter(new OutputStreamWriter(socket.getOutputStream())), true);

	    out.print("command/sched/" + start_time.split(":")[0] + "/" + stop_time.split(":")[0]);
	    out.flush();

	    String status_string = in.readLine();

	    callback(true);

	} catch (UnknownHostException e1) {
	    e1.printStackTrace();
	} catch (IOException e1) {
	    e1.printStackTrace();
	}

}

static public void add_eco_switch(String name, String deadline, String charge_time, MyCallback callback ){
		try {

	    Socket s = connect_to_server()
	    BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
	    PrintWriter out = new PrintWriter(new BufferedWriter(new OutputStreamWriter(socket.getOutputStream())), true);

	    out.print("command/eco/" + deadline.split(":")[0] + "/" + charge_time.split(":")[0]);
	    out.flush();

	    String status_string = in.readLine();

	    callback(true);

	} catch (UnknownHostException e1) {
	    e1.printStackTrace();
	} catch (IOException e1) {
	    e1.printStackTrace();
	}

}
