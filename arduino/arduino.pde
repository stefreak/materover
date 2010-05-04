long lasttime;
byte SYNCBYTE = 0x58;
int SECURETIMEOUT = 10000;

/* setup the serial line */
void setup()
{
	// start serial port at 9600 bps:
	Serial.begin(9600);
	delay(300);
}

/* write the values to the pwm pins */
void set_motor(char array[])
{
	// motor 1
	analogWrite(11, array[0]);
	analogWrite(10, array[1]);
	// motor 2
	analogWrite(9, array[2]);
	analogWrite(6, array[3]);
}

/* shut the motors down if there were no bytes
   for 2 seconds */
void motorsecuritycheck()
{
	if(millis() - lasttime > SECURETIMEOUT)
	{
		char array[4] = {0,0,0,0};
		set_motor(array);
	}
}

/* read one byte from the serial line. blocking. */
char read_byte()
{
	while (Serial.available()==0)
		motorsecuritycheck();
	lasttime = millis();
	return Serial.read();
}

/* main loop */
void loop()
{
	char array[4] = {0,0,0,0};
	lasttime = millis();

	/* wait for sync byte */
	while (true) {
          if (read_byte() == SYNCBYTE) {
            break;
          }
        }

	/* receive the 4 bytes */
	for (int i=0; i <= 3; i++)
	{
		array[i] = read_byte();
		/* if stop byte is received reset receive loop */
		if (array[i] == SYNCBYTE) i = -1;
	}
 
	/* send the received bytes back */
	for (int i=0; i <= 3; i++)
		Serial.print(array[i], BYTE);
        
	Serial.println();
        set_motor(array);

	delay(10);
}
