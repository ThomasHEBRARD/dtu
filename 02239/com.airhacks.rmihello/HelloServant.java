import java.rmi.server.UnicastRemoteObject;
import java.rmi.RemoteException;

public class HelloServant extends UnicastRemoteObject implements HelloService {
    public HelloServant() throws RemoteException {
        super();

    }

    public String echo(String input) throws RemoteException {
        return "From server: " + input;

    }
}