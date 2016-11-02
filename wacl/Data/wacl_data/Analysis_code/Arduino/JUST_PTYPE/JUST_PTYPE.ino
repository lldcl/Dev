// MUST ADD ALL RELEVANT LIBRARIES
#include <Wire.h>
extern "C" { 
#include "utility/twi.h"  // from Wire library, so we can do bus scanning
}
#include <Statistic.h>
#include <Adafruit_ADS1015.h>
//#include <Adafruit_Sensor.h>
//#include <Adafruit_HMC5883_U.h>

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

//Create instances for adafruit adc's on sensor board (each with unique adrs). Each eurocircuit has 4 Adafruit ADCs.
Adafruit_ADS1115 ads1115_48(0x48);
//Adafruit_ADS1115 ads1115_49(0x49);
//Adafruit_ADS1115 ads1115_4A(0x4A);
//Adafruit_ADS1115 ads1115_4B(0x4B);

// Create statisitics for each sensor and millis

//Statistic ptype_stats;
Statistic P1_stats;
Statistic P2_stats;
Statistic P3_stats;
Statistic P4_stats;
Statistic P5_stats;
Statistic P6_stats;
Statistic P7_stats;
Statistic P8_stats;
//Statistic Millis_stats;

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
  tcaselect(4);
  ads1115_48.setGain(GAIN_ONE);        // 2x gain   +/- 2.048V  1 bit = 1mV      0.0625mV
  ads1115_48.begin();


//  tcaselect(2);
//  ads1115_48B.setGain(GAIN_TWO);        // 2x gain   +/- 2.048V  1 bit = 1mV      0.0625mV
//  ads1115_48B.begin();
//  ads1115_49B.setGain(GAIN_TWO);        // 2x gain   +/- 2.048V  1 bit = 1mV      0.0625mV
//  ads1115_49B.begin();
//  ads1115_4AB.setGain(GAIN_TWO);        // 2x gain   +/- 2.048V  1 bit = 1mV      0.0625mV
//  ads1115_4AB.begin();
//  ads1115_4BB.setGain(GAIN_TWO);        // 2x gain   +/- 2.048V  1 bit = 1mV      0.0625mV
//  ads1115_4BB.begin();
//

//  Serial.println("End set up bd 2");
//ensure all statistic instances are empty
  P1_stats.clear();
  P2_stats.clear();
  P3_stats.clear();
  P4_stats.clear();
  P5_stats.clear();
  P6_stats.clear();
  P7_stats.clear();
  P8_stats.clear();

 // ptype_stats.clear();
//  MOS1b_stats.clear();
//  MOS2b_stats.clear();
//  MOS3b_stats.clear();
//  MOS4b_stats.clear();
//  MOS5b_stats.clear();
//  MOS6b_stats.clear();
//  MOS7b_stats.clear();
//  MOS8b_stats.clear();

  pinMode(13, OUTPUT);
//End of set up code  
}

float multiplier = 0.125F*1e-3;
void takeSample()
{  
//  Serial.println("takesample");
// One green eurocircuit board to be connected to SD0,SC0 and the other is on the SD1/SC1 port. 
//take sample loop reads each sensor voltage and adds to statistic instance
//  tcaselect(0);
//  MOS1_stats.add(ads1115_4B.readADC_Differential_0_1());
//  MOS2_stats.add(ads1115_49.readADC_Differential_2_3());
//  MOS3_stats.add(ads1115_4A.readADC_Differential_2_3());
//  MOS4_stats.add(ads1115_48.readADC_Differential_2_3());
//  MOS5_stats.add(ads1115_4A.readADC_Differential_0_1());
//  MOS6_stats.add(ads1115_48.readADC_Differential_0_1());
//  MOS7_stats.add(ads1115_4B.readADC_Differential_2_3());
//  MOS8_stats.add(ads1115_49.readADC_Differential_0_1());
  tcaselect(4);
//  P4_stats.add(ads1115_48.readADC_Differential_2_3());
  P6_stats.add(ads1115_48.readADC_Differential_0_1());


//  tcaselect(2);
//  MOS1b_stats.add(ads1115_4BB.readADC_Differential_0_1()*multiplier); 
//  MOS2b_stats.add(ads1115_49B.readADC_Differential_2_3()*multiplier);
//  MOS3b_stats.add(ads1115_4AB.readADC_Differential_2_3()*multiplier);
//  MOS4b_stats.add(ads1115_48B.readADC_Differential_2_3()*multiplier);
//  MOS5b_stats.add(ads1115_4AB.readADC_Differential_0_1()*multiplier);
//  MOS6b_stats.add(ads1115_48B.readADC_Differential_0_1()*multiplier);
//  MOS7b_stats.add(ads1115_4BB.readADC_Differential_2_3()*multiplier);
//  MOS8b_stats.add(ads1115_49B.readADC_Differential_0_1()*multiplier);
  
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
    double P1_Av = P1_stats.average()*multiplier*1e-3;
    double P1_stddev =  P1_stats.pop_stdev()*multiplier*1e-3;    
    double P2_Av = P2_stats.average()*multiplier*1e-3;
    double P2_stddev =  P2_stats.pop_stdev()*multiplier*1e-3;
    double P3_Av = P3_stats.average()*multiplier*1e-3;
    double P3_stddev =  P3_stats.pop_stdev()*multiplier*1e-3;
    double P4_Av = P4_stats.average()*multiplier*1e-3;
    double P4_stddev =  P4_stats.pop_stdev()*multiplier*1e-3;
    double P5_Av = P5_stats.average()*multiplier*1e-3;
    double P5_stddev =  P5_stats.pop_stdev()*multiplier*1e-3;
    double P6_Av = P6_stats.average()*multiplier*1e-3;
    double P6_stddev =  P6_stats.pop_stdev()*multiplier*1e-3;
    double P7_Av = P7_stats.average()*multiplier*1e-3;
    double P7_stddev =  P7_stats.pop_stdev()*multiplier*1e-3;
    double P8_Av = P8_stats.average()*multiplier*1e-3;
    double P8_stddev =  P8_stats.pop_stdev()*multiplier*1e-3;

//    double ptype_Av = ptype_stats.average()*multiplier;
//    double MOS1b_Av = MOS2b_stats.average()*gaintwo_multiplier*1e-3;
//    double MOS1b_stddev =  MOS1b_stats.pop_stdev()*gaintwo_multiplier*1e-3;    
//    double MOS2b_Av = MOS2b_stats.average()*gaintwo_multiplier*1e-3;
//    double MOS2b_stddev =  MOS2b_stats.pop_stdev()*gaintwo_multiplier*1e-3;
//    double MOS3b_Av = MOS3b_stats.average()*gaintwo_multiplier*1e-3;
//    double MOS3b_stddev =  MOS3b_stats.pop_stdev()*gaintwo_multiplier*1e-3;
//    double MOS4b_Av = MOS4b_stats.average()*gaintwo_multiplier*1e-3;
//    double MOS4b_stddev =  MOS4b_stats.pop_stdev()*gaintwo_multiplier*1e-3;
//    double MOS5b_Av = MOS5b_stats.average()*gaintwo_multiplier*1e-3;
//    double MOS5b_stddev =  MOS5b_stats.pop_stdev()*gaintwo_multiplier*1e-3;
//    double MOS6b_Av = MOS6b_stats.average()*gaintwo_multiplier*1e-3;
//    double MOS6b_stddev =  MOS6b_stats.pop_stdev()*gaintwo_multiplier*1e-3;
//    double MOS7b_Av = MOS7b_stats.average()*gaintwo_multiplier*1e-3;
//    double MOS7b_stddev =  MOS7b_stats.pop_stdev()*gaintwo_multiplier*1e-3;
//    double MOS8b_Av = MOS8b_stats.average()*gaintwo_multiplier*1e-3;
//    double MOS8b_stddev =  MOS8b_stats.pop_stdev()*gaintwo_multiplier*1e-3;

// Print and store the average. Must call each multiplexer address before printing information from that section.  
      


      Serial.println(); 
      tcaselect(4);
      Serial.print("Hello");
      Serial.print(P1_Av, 8);
      Serial.print(",");
      Serial.print(P2_Av, 8);
      Serial.print(",");
      Serial.print(P3_Av, 8);
      Serial.print(",");
      Serial.print(P4_Av, 8);
      Serial.print(",");
      Serial.print(P5_Av, 8);
      Serial.print(",");
      Serial.print(P6_Av, 8);
      Serial.print(",");
      Serial.print(P7_Av, 8);
      Serial.print(",");
      Serial.print(P8_Av, 8);
      Serial.println(",");

//      tcaselect(1);
//      Serial.print("Board");
//      Serial.print("1");
//      Serial.print(",");
//      tcaselect(4);
//      Serial.print(ptype_Av, 8);

//      tcaselect(2);
//      Serial.print(",");
//      Serial.print(MOS1b_Av, 8);
//      Serial.print(",");
//      Serial.print(MOS2b_Av, 8);
//      Serial.print(",");
//      Serial.print(MOS3b_Av, 8);
//      Serial.print(",");
//      Serial.print(MOS4b_Av, 8);
//      Serial.print(",");
//      Serial.print(MOS5b_Av, 8);
//      Serial.print(",");
//      Serial.print(MOS6b_Av, 8);
//      Serial.print(",");
//      Serial.print(MOS7b_Av, 8);
//      Serial.print(",");
//      Serial.println(MOS8b_Av, 8);
      
//
//      tcaselect(2);
//      Serial.print("Board");
//      Serial.print("2");
//      Serial.print(",");
//      Serial.print(MOS1c_Av, 8);
//      Serial.print(",");
//      Serial.print(MOS2c_Av, 8);
//      Serial.print(",");
//      Serial.print(MOS3c_Av, 8);
//      Serial.print(",");
//      Serial.print(MOS4c_Av, 8);
//      Serial.print(",");
//      Serial.print(MOS5c_Av, 8);
//      Serial.print(",");
//      Serial.print(MOS6c_Av, 8);
//      Serial.print(",");
//      Serial.print(MOS7c_Av, 8);
//      Serial.print(",");
//      Serial.println(MOS8_Av, 8);
    

    
    Serial.flush();
// Clear the stats for the next re-iteration of the loop.
    P1_stats.clear();
    P2_stats.clear();
    P3_stats.clear();
    P4_stats.clear();
    P5_stats.clear();
    P6_stats.clear();
    P7_stats.clear();
    P8_stats.clear();

//    ptype_stats.clear();
//    MOS1b_stats.clear();
//    MOS2b_stats.clear();
//    MOS3b_stats.clear();
//    MOS4b_stats.clear();
//    MOS5b_stats.clear();
//    MOS6b_stats.clear();
//    MOS7b_stats.clear();
//    MOS8b_stats.clear();
//


    digitalWrite(13, !digitalRead(13));
  }

  takeSample();

  
}
