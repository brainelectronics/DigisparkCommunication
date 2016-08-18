#define USB_CFG_DEVICE_NAME     'D','i','g','i','B','l','i','n','k'
#define USB_CFG_DEVICE_NAME_LEN 9
#include <DigiUSB.h>
byte in = 0;
unsigned int powerMeterCounter = 0;

void setup() {
  DigiUSB.begin();
  attachInterrupt(0, incrementCounter, RISING);
}


void loop()
{
  DigiUSB.refresh();
  if (DigiUSB.available() > 0)
  {
    in = 0;

    in = DigiUSB.read();
    if (in == 115)
    {
      // DigiUSB.println("Start");
      // DigiUSB.println(powerMeterCounter);
      // powerMeterCounter = 0;
      returnCounter();
    }
  }
  // powerMeterCounter++;
}

// prints the counter value via serial connection and resets counter
void returnCounter()
{
  DigiUSB.println(powerMeterCounter);
  powerMeterCounter = 0;  // reset counter
}

// function called by interrupt
void incrementCounter()
{
  powerMeterCounter++;
}

