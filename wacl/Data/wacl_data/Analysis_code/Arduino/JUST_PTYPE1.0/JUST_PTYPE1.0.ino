// MUST ADD ALL RELEVANT LIBRARIES
#include <Wire.h>
extern "C" { 
#include "utility/twi.h"  // from Wire library, so we can do bus scanning
}
#include <Statistic.h>
#include <Adafruit_ADS1015.h>

// Define the multiplexer name and its address.
#define TCAADDR1 0x70

// Write the exact number of eurocircuit boards that you want to use.

// Helps to select the port on the multiplexer. Then call tcaselect(0) thru tcaselect(7) to set up the multiplexer.
//If using tcaselect(3), plug the blue wire from Eurocircuit cable into SC3, and the white wire into SD3 by the multiplexer.
void tcaselect(uint8_t i) 
{
  if (i > 7) return;
  Wire.beginTransmission(TCAADDR1);
  Wire.write(1 << i);
  Wire.endTransmission();  
}

//Create instances for adafruit adc's on sensor board (each with unique adrs). 
// There is only one p-type sensor and the signal from the sensor is analog and comes in via the A0 and A1 channels on the 
// ADS1115 address board. To reduce electrical noise and interference, this is converted to a digital signal via the SDA channel.
// The SCL (clock) is also connected to ensure the data points have the correct time. 

// The ADS1115 address boards can have four different addresses - depending on how you supply voltage to some of the channels.
// With no voltage aplied the address is 0x48, see below.
Adafruit_ADS1115 ads1115_48(0x48);


// Create statisitics for the p-type sensor to put data into.

Statistic ptype_stats;


// last sample and delay time to set serial print frequencies
unsigned long lastSample;
//set delaytime to data serial print frequency wanted (ms, therefore every second if = 1000)
int delayTime = 1000;

void setup()
  // Setup code, this will run once:
{
  Wire.begin();
  Serial.begin(9600);
  tcaselect(4);
  ads1115_48.setGain(GAIN_ONE);        // 2x gain   +/- 2.048V  1 bit = 1mV      0.0625mV
  ads1115_48.begin();

// Set the gain to one forthe p-type sensor. Whe the signal is converted to a digital signal, the voltage is binned. The gain
// refers to the size of these bins - smaller = higher resolution, but have a smaller range of volatges available as the 
// number of bins cannot be increased.

//ensure all statistic instances are empty before I put data in them. 
  
  ptype_stats.clear();

// Set LED to flash if Arduino is working.
  pinMode(13, OUTPUT);
//End of set up code  
}

float multiplier = 0.125F*1e-3;
void takeSample()
{  

//take sample loop reads each sensor voltage and adds to statistic instance.
  
  tcaselect(4);
  ptype_stats.add(ads1115_48.readADC_Differential_0_1());
  
}
// Begin the loop to keep recording data.
void loop(void)
{
  // put your main code here, to run repeatedly:
  unsigned long currentMillis = millis();
  
  if (currentMillis - lastSample > delayTime)
  {
    lastSample = currentMillis;

// Arduino data comes in on a 10Hz basis - but we average this every second, and collect the stddev of this data.
//Telling the data to be averaged and the standard deviation for the MOS to be calculated
    double ptype_Av = ptype_stats.average()*multiplier;
    double ptype_stddev =  ptype_stats.pop_stdev()*multiplier;

// Print and store the average. Must call each multiplexer address before printing information from that section.  
           
      tcaselect(4);
      Serial.print(ptype_Av, 8);
      Serial.print(",");
      Serial.print(ptype_stddev, 8);
      Serial.println(",");
    

    
    Serial.flush();
// Clear the stats for the next re-iteration of the loop.
  
    ptype_stats.clear();
//
    digitalWrite(13, !digitalRead(13));
  }

  takeSample();

  
}
