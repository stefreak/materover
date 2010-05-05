package communication_serial;

import gnu.io.CommPortIdentifier;
import gnu.io.SerialPort;

import java.io.InputStream;
import java.io.OutputStream;
import java.util.Enumeration;

public class PortWriter
{
    Enumeration ports;
    CommPortIdentifier pID;
    OutputStream outStream;
    InputStream inputStream;
    public SerialPort serPort;
    
    public PortWriter() throws Exception{
    	ports = CommPortIdentifier.getPortIdentifiers();
        while(ports.hasMoreElements())
        {
            pID = (CommPortIdentifier)ports.nextElement();
            System.out.println("Port " + pID.getName());
            
            if (pID.getPortType() == CommPortIdentifier.PORT_SERIAL)
            {
                if (pID.getName().equals("COM5"))
                {
                    System.out.println("COM5 found");
                }
            }
        }
        
        serPort = (SerialPort)pID.open("PortWriter",2000);
        outStream = serPort.getOutputStream();
        inputStream = serPort.getInputStream();

        serPort.setSerialPortParams(
        		9600, 
        		SerialPort.DATABITS_8,
        		SerialPort.STOPBITS_1,
        		SerialPort.PARITY_NONE
        		);
    }   
    
    public void write(char[] a) throws Exception{
    	String s = new String(a);
        outStream.write(s.getBytes());
        System.out.println(inputStream.read());
    }
    
    public void close() throws Exception{
    	outStream.close();
    	inputStream.close();
    	serPort.close();
    }
    
    public static void main(String[] args) throws Exception{
    	PortWriter p = new PortWriter();
        char[] a = new char[]{0x58, 0xee, 0xee, 0x55, 0x55};
        p.write(a);	System.out.println("Gesendet");
        p.close();  System.out.println("quit");
    }
}

   