// MUST ADD ALL RELEVANT LIBRARIES
#include <Wire.h>
extern "C" { 
#include "utility/twi.h"  // from Wire library, so we can do bus scanning
}
#include <Statistic.h>
#include <Adafruit_ADS1015.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_HMC5883_U.h>

// Define the multiplexer name and its address.
#define TCAADDR1 0x70

// Write the exact number of eurocircuit boards that you want to use.
#define numOfBoards 3
#define numOfMOS 8
// Helps to select the port on the multiplexer. Then call tcaselect(0) thru tcaselect(7) to set up the multiplexer.
//If using tcaselect(3), plug the blue wire from Eurocircuit cable into SC3, and the white wire into SD3 by the multiplexer.
void tcaselect(uint8_t i) 
{
  if (i > 7) return;
  Wire.beginTransmission(TCAADDR1);
  Wire.write(1 << i);
  Wire.endTransmission();  
}



//Create instances for adafruit adc's on sensor board (each with unique adrs). Each eurocircuit has 4 Adafruit ADCs.
Adafruit_ADS1115 ads1115_48(0x48);
Adafruit_ADS1115 ads1115_49(0x49);
Adafruit_ADS1115 ads1115_4A(0x4A);
Adafruit_ADS1115 ads1115_4B(0x4B);

Adafruit_ADS1115 ads1115_48b(0x48);
Adafruit_ADS1115 ads1115_49b(0x49);
Adafruit_ADS1115 ads1115_4Ab(0x4A);
Adafruit_ADS1115 ads1115_4Bb(0x4B);

Adafruit_ADS1115 ads1115_48c(0x48);
Adafruit_ADS1115 ads1115_49c(0x49);
Adafruit_ADS1115 ads1115_4Ac(0x4A);
Adafruit_ADS1115 ads1115_4Bc(0x4B);

// Create statisitics for each sensor and millis
Statistic MOS1_stats;
Statistic MOS2_stats;
Statistic MOS3_stats;
Statistic MOS4_stats;
Statistic MOS5_stats;
Statistic MOS6_stats;
Statistic MOS7_stats;
Statistic MOS8_stats;

Statistic MOS1b_stats;
Statistic MOS2b_stats;
Statistic MOS3b_stats;
Statistic MOS4b_stats;
Statistic MOS5b_stats;
Statistic MOS6b_stats;
Statistic MOS7b_stats;
Statistic MOS8b_stats;

Statistic MOS1c_stats;
Statistic MOS2c_stats;
Statistic MOS3c_stats;
Statistic MOS4c_stats;
Statistic MOS5c_stats;
Statistic MOS6c_stats;
Statistic MOS7c_stats;
Statistic MOS8c_stats;

Statistic Millis_stats;

// last sample and delay time to set serial print frequencies
unsigned long lastSample;
//set delaytime to data serial print frequency wanted (ms, therefore every second if = 1000)
int delayTime = 1000;

//multiplier for ads1115 to set the bit voltage (depends on gains set in setup loop)
float gaintwo_multiplier = 0.0625; /* ADS1115  @ +/- 4.096V gain (16-bit results) */


void setup()
  // Setup code, this will run once:
{
  Wire.begin();
  Serial.begin(9600);
  tcaselect(0);
  ads1115_48.setGain(GAIN_TWO);        // 2x gain   +/- 2.048V  1 bit = 1mV      0.0625mV
  ads1115_48.begin();
  ads1115_49.setGain(GAIN_TWO);        // 2x gain   +/- 2.048V  1 bit = 1mV      0.0625mV
  ads1115_49.begin();
  ads1115_4A.setGain(GAIN_TWO);        // 2x gain   +/- 2.048V  1 bit = 1mV      0.0625mV
  ads1115_4A.begin();
  ads1115_4B.setGain(GAIN_TWO);        // 2x gain   +/- 2.048V  1 bit = 1mV      0.0625mV
  ads1115_4B.begin();

  tcaselect(1);
  ads1115_48b.setGain(GAIN_TWO);        // 2x gain   +/- 2.048V  1 bit = 1mV      0.0625mV
  ads1115_48b.begin();
  ads1115_49b.setGain(GAIN_TWO);        // 2x gain   +/- 2.048V  1 bit = 1mV      0.0625mV
  ads1115_49b.begin();
  ads1115_4Ab.setGain(GAIN_TWO);        // 2x gain   +/- 2.048V  1 bit = 1mV      0.0625mV
  ads1115_4Ab.begin();
  ads1115_4Bb.setGain(GAIN_TWO);        // 2x gain   +/- 2.048V  1 bit = 1mV      0.0625mV
  ads1115_4Bb.begin();

  tcaselect(2);
  ads1115_48c.setGain(GAIN_TWO);        // 2x gain   +/- 2.048V  1 bit = 1mV      0.0625mV
  ads1115_48c.begin();
  ads1115_49c.setGain(GAIN_TWO);        // 2x gain   +/- 2.048V  1 bit = 1mV      0.0625mV
  ads1115_49c.begin();
  ads1115_4Ac.setGain(GAIN_TWO);        // 2x gain   +/- 2.048V  1 bit = 1mV      0.0625mV
  ads1115_4Ac.begin();
  ads1115_4Bc.setGain(GAIN_TWO);        // 2x gain   +/- 2.048V  1 bit = 1mV      0.0625mV
  ads1115_4Bc.begin();
//  Serial.println("End set up bd 2");
//ensure all statistic instances are empty
  MOS1_stats.clear();
  MOS2_stats.clear();
  MOS3_stats.clear();
  MOS4_stats.clear();
  MOS5_stats.clear();
  MOS6_stats.clear();
  MOS7_stats.clear();
  MOS8_stats.clear();

  MOS1b_stats.clear();
  MOS2b_stats.clear();
  MOS3b_stats.clear();
  MOS4b_stats.clear();
  MOS5b_stats.clear();
  MOS6b_stats.clear();
  MOS7b_stats.clear();
  MOS8b_stats.clear();

  MOS1c_stats.clear();
  MOS2c_stats.clear();
  MOS3c_stats.clear();
  MOS4c_stats.clear();
  MOS5c_stats.clear();
  MOS6c_stats.clear();
  MOS7c_stats.clear();
  MOS8c_stats.clear();

  pinMode(13, OUTPUT);
//End of set up code  
}

float multiplier = 0.125F*1e-3;
void takeSample()
{  
//  Serial.println("takesample");
// One green eurocircuit board to be connected to SD0,SC0 and the other is on the SD1/SC1 port. 
//take sample loop reads each sensor voltage and adds to statistic instance
  tcaselect(0);
  MOS1_stats.add(ads1115_4B.readADC_Differential_0_1()*multiplier);
  MOS2_stats.add(ads1115_49.readADC_Differential_2_3()*multiplier);
  MOS3_stats.add(ads1115_4A.readADC_Differential_2_3()*multiplier);
  MOS4_stats.add(ads1115_48.readADC_Differential_2_3()*multiplier);
  MOS5_stats.add(ads1115_4A.readADC_Differential_0_1()*multiplier);
  MOS6_stats.add(ads1115_48.readADC_Differential_0_1()*multiplier);
  MOS7_stats.add(ads1115_4B.readADC_Differential_2_3()*multiplier);
  MOS8_stats.add(ads1115_49.readADC_Differential_0_1()*multiplier);
  tcaselect(1);
  MOS1b_stats.add(ads1115_4Bb.readADC_Differential_0_1()*multiplier);
  MOS2b_stats.add(ads1115_49b.readADC_Differential_2_3()*multiplier);
  MOS3b_stats.add(ads1115_4Ab.readADC_Differential_2_3()*multiplier);
  MOS4b_stats.add(ads1115_48b.readADC_Differential_2_3()*multiplier);
  MOS5b_stats.add(ads1115_4Ab.readADC_Differential_0_1()*multiplier);
  MOS6b_stats.add(ads1115_48b.readADC_Differential_0_1()*multiplier);
  MOS7b_stats.add(ads1115_4Bb.readADC_Differential_2_3()*multiplier);
  MOS8b_stats.add(ads1115_49b.readADC_Differential_0_1()*multiplier);
  tcaselect(2);
  MOS1c_stats.add(ads1115_4Bc.readADC_Differential_0_1()*multiplier);
  MOS2c_stats.add(ads1115_49c.readADC_Differential_2_3()*multiplier);
  MOS3c_stats.add(ads1115_4Ac.readADC_Differential_2_3()*multiplier);
  MOS4c_stats.add(ads1115_48c.readADC_Differential_2_3()*multiplier);
  MOS5c_stats.add(ads1115_4Ac.readADC_Differential_0_1()*multiplier);
  MOS6c_stats.add(ads1115_48c.readADC_Differential_0_1()*multiplier);
  MOS7c_stats.add(ads1115_4Bc.readADC_Differential_2_3()*multiplier);
  MOS8c_stats.add(ads1115_49c.readADC_Differential_0_1()*multiplier);
  
}
// Begin the loop to keep recording data.
void loop(void)
{
  // put your main code here, to run repeatedly:
  unsigned long currentMillis = millis();
  
  if (currentMillis - lastSample > delayTime)
  {
    lastSample = currentMillis;

// Telling the data to be averaged and the standard deviation for the MOS to be calculated
    double MOS1_Av = MOS1_stats.average()*gaintwo_multiplier*1e-3;
    double MOS1_stddev =  MOS1_stats.pop_stdev()*gaintwo_multiplier*1e-3;    
    double MOS2_Av = MOS2_stats.average()*gaintwo_multiplier*1e-3;
    double MOS2_stddev =  MOS2_stats.pop_stdev()*gaintwo_multiplier*1e-3;
    double MOS3_Av = MOS3_stats.average()*gaintwo_multiplier*1e-3;
    double MOS3_stddev =  MOS3_stats.pop_stdev()*gaintwo_multiplier*1e-3;
    double MOS4_Av = MOS4_stats.average()*gaintwo_multiplier*1e-3;
    double MOS4_stddev =  MOS4_stats.pop_stdev()*gaintwo_multiplier*1e-3;
    double MOS5_Av = MOS5_stats.average()*gaintwo_multiplier*1e-3;
    double MOS5_stddev =  MOS5_stats.pop_stdev()*gaintwo_multiplier*1e-3;
    double MOS6_Av = MOS6_stats.average()*gaintwo_multiplier*1e-3;
    double MOS6_stddev =  MOS6_stats.pop_stdev()*gaintwo_multiplier*1e-3;
    double MOS7_Av = MOS7_stats.average()*gaintwo_multiplier*1e-3;
    double MOS7_stddev =  MOS7_stats.pop_stdev()*gaintwo_multiplier*1e-3;
    double MOS8_Av = MOS8_stats.average()*gaintwo_multiplier*1e-3;
    double MOS8_stddev =  MOS8_stats.pop_stdev()*gaintwo_multiplier*1e-3;

    double MOS1b_Av = MOS1b_stats.average()*gaintwo_multiplier*1e-3;
    double MOS1b_stddev =  MOS1b_stats.pop_stdev()*gaintwo_multiplier*1e-3;    
    double MOS2b_Av = MOS2b_stats.average()*gaintwo_multiplier*1e-3;
    double MOS2b_stddev =  MOS2b_stats.pop_stdev()*gaintwo_multiplier*1e-3;
    double MOS3b_Av = MOS3b_stats.average()*gaintwo_multiplier*1e-3;
    double MOS3b_stddev =  MOS3b_stats.pop_stdev()*gaintwo_multiplier*1e-3;
    double MOS4b_Av = MOS4b_stats.average()*gaintwo_multiplier*1e-3;
    double MOS4b_stddev =  MOS4b_stats.pop_stdev()*gaintwo_multiplier*1e-3;
    double MOS5b_Av = MOS5b_stats.average()*gaintwo_multiplier*1e-3;
    double MOS5b_stddev =  MOS5b_stats.pop_stdev()*gaintwo_multiplier*1e-3;
    double MOS6b_Av = MOS6b_stats.average()*gaintwo_multiplier*1e-3;
    double MOS6b_stddev =  MOS6b_stats.pop_stdev()*gaintwo_multiplier*1e-3;
    double MOS7b_Av = MOS7b_stats.average()*gaintwo_multiplier*1e-3;
    double MOS7b_stddev =  MOS7b_stats.pop_stdev()*gaintwo_multiplier*1e-3;
    double MOS8b_Av = MOS8b_stats.average()*gaintwo_multiplier*1e-3;
    double MOS8b_stddev =  MOS8b_stats.pop_stdev()*gaintwo_multiplier*1e-3;

    double MOS1c_Av = MOS1c_stats.average()*gaintwo_multiplier*1e-3;
    double MOS1c_stddev =  MOS1c_stats.pop_stdev()*gaintwo_multiplier*1e-3;    
    double MOS2c_Av = MOS2c_stats.average()*gaintwo_multiplier*1e-3;
    double MOS2c_stddev =  MOS2c_stats.pop_stdev()*gaintwo_multiplier*1e-3;
    double MOS3c_Av = MOS3c_stats.average()*gaintwo_multiplier*1e-3;
    double MOS3c_stddev =  MOS3c_stats.pop_stdev()*gaintwo_multiplier*1e-3;
    double MOS4c_Av = MOS4c_stats.average()*gaintwo_multiplier*1e-3;
    double MOS4c_stddev = MOS4c_stats.pop_stdev()*gaintwo_multiplier*1e-3;
    double MOS5c_Av = MOS5c_stats.average()*gaintwo_multiplier*1e-3;
    double MOS5c_stddev =  MOS5c_stats.pop_stdev()*gaintwo_multiplier*1e-3;
    double MOS6c_Av = MOS6c_stats.average()*gaintwo_multiplier*1e-3;
    double MOS6c_stddev = MOS6c_stats.pop_stdev()*gaintwo_multiplier*1e-3;
    double MOS7c_Av = MOS7c_stats.average()*gaintwo_multiplier*1e-3;
    double MOS7c_stddev =  MOS7c_stats.pop_stdev()*gaintwo_multiplier*1e-3;
    double MOS8c_Av = MOS8c_stats.average()*gaintwo_multiplier*1e-3;
    double MOS8c_stddev =  MOS8c_stats.pop_stdev()*gaintwo_multiplier*1e-3;

// Print and store the average. Must call each multiplexer address before printing information from that section.  
      
      Serial.println();

       
      tcaselect(0);
      Serial.print("Board");
      Serial.print("0");
      Serial.print(",");
      Serial.print(MOS1_Av, 8);
      Serial.print(",");
      Serial.print(MOS2_Av, 8);
      Serial.print(",");
      Serial.print(MOS3_Av, 8);
      Serial.print(",");
      Serial.print(MOS4_Av, 8);
      Serial.print(",");
      Serial.print(MOS5_Av, 8);
      Serial.print(",");
      Serial.print(MOS6_Av, 8);
      Serial.print(",");
      Serial.print(MOS7_Av, 8);
      Serial.print(",");
      Serial.println(MOS8_Av, 8);

      tcaselect(1);
      Serial.print("Board");
      Serial.print("1");
      Serial.print(",");
      Serial.print(MOS1b_Av, 8);
      Serial.print(",");
      Serial.print(MOS2b_Av, 8);
      Serial.print(",");
      Serial.print(MOS3b_Av, 8);
      Serial.print(",");
      Serial.print(MOS4b_Av, 8);
      Serial.print(",");
      Serial.print(MOS5b_Av, 8);
      Serial.print(",");
      Serial.print(MOS6b_Av, 8);
      Serial.print(",");
      Serial.print(MOS7b_Av, 8);
      Serial.print(",");
      Serial.println(MOS8b_Av, 8);

      tcaselect(2);
      Serial.print("Board");
      Serial.print("2");
      Serial.print(",");
      Serial.print(MOS1c_Av, 8);
      Serial.print(",");
      Serial.print(MOS2c_Av, 8);
      Serial.print(",");
      Serial.print(MOS3c_Av, 8);
      Serial.print(",");
      Serial.print(MOS4c_Av, 8);
      Serial.print(",");
      Serial.print(MOS5c_Av, 8);
      Serial.print(",");
      Serial.print(MOS6c_Av, 8);
      Serial.print(",");
      Serial.print(MOS7c_Av, 8);
      Serial.print(",");
      Serial.println(MOS8_Av, 8);
    

    
    Serial.flush();
// Clear the stats for the next re-iteration of the loop.
    MOS1_stats.clear();
    MOS2_stats.clear();
    MOS3_stats.clear();
    MOS4_stats.clear();
    MOS5_stats.clear();
    MOS6_stats.clear();
    MOS7_stats.clear();
    MOS8_stats.clear();

    MOS1b_stats.clear();
    MOS2b_stats.clear();
    MOS3b_stats.clear();
    MOS4b_stats.clear();
    MOS5b_stats.clear();
    MOS6b_stats.clear();
    MOS7b_stats.clear();
    MOS8b_stats.clear();

    MOS1c_stats.clear();
    MOS2c_stats.clear();
    MOS3c_stats.clear();
    MOS4c_stats.clear();
    MOS5c_stats.clear();
    MOS6c_stats.clear();
    MOS7c_stats.clear();
    MOS8c_stats.clear();


    digitalWrite(13, !digitalRead(13));
  }

  takeSample();

  
}
