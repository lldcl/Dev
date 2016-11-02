// MUST ADD ALL RELEVANT LIBRARIES
#include <Wire.h>
extern "C" { 
#include "utility/twi.h"  // from Wire library, so we can do bus scanning
}
#include <Statistic.h>
#include <Adafruit_ADS1015.h>
//#include <Adafruit_Sensor.h>
//#include <Adafruit_HMC5883_U.h>
#include <Adafruit_BMP085.h>
Adafruit_BMP085 bmp;
//#include <Adafruit_HTU21DF.h>
//Adafruit_HTU21DF htu;

// Define the multiplexer name and its address.
#define TCAADDR1 0x70

// Write the exact number of eurocircuit boards that you want to use.
#define numOfBoards 2
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
//Setting addresses for the three other sensors.
Adafruit_ADS1115 ads1115_A;
Adafruit_ADS1115 ads1115_B;
Adafruit_ADS1115 ads1115_C;

// Setting adresses for the first eurocircuit board
Adafruit_ADS1115 ads1115_48(0x48);
Adafruit_ADS1115 ads1115_49(0x49);
Adafruit_ADS1115 ads1115_4A(0x4A);
Adafruit_ADS1115 ads1115_4B(0x4B);
// Setting addresses for the second eurocircuit board.
Adafruit_ADS1115 ads1115_48b(0x48);
Adafruit_ADS1115 ads1115_49b(0x49);
Adafruit_ADS1115 ads1115_4Ab(0x4A);
Adafruit_ADS1115 ads1115_4Bb(0x4B);



// Create statisitics for each sensor and millis
// Statisitics header for the first eurocircuit board.
Statistic MOS1_stats;
Statistic MOS2_stats;
Statistic MOS3_stats;
Statistic MOS4_stats;
Statistic MOS5_stats;
Statistic MOS6_stats;
Statistic MOS7_stats;
Statistic MOS8_stats;
//Statistics header for the second eurocircuit boardss' sensors.
Statistic MOS1b_stats;
Statistic MOS2b_stats;
Statistic MOS3b_stats;
Statistic MOS4b_stats;
Statistic MOS5b_stats;
Statistic MOS6b_stats;
Statistic MOS7b_stats;
Statistic MOS8b_stats;
// Header for the ozone, NO and CO sensors to use the statistics library. 
Statistic O3_1_OP1_stats;
Statistic O3_1_OP2_stats;
Statistic NO2_1_OP1_stats;
Statistic NO2_1_OP2_stats;
Statistic NO_1_OP1_stats;
Statistic NO_1_OP2_stats;
Statistic CO_1_OP1_stats;
Statistic CO_1_OP2_stats;
Statistic CO2_1_stats;
// Temperature, RH, supplay voltage headers.
Statistic Temp1_stats;
//Statistic Press1_stats;
Statistic Temp2_stats;
Statistic RH1_stats;
// Take these out so they do not overcomplicate things.
//Statistic HIH1_stats;
//Statistic LM65T1_stats;
//Statistic SV_stats;
//Statistic Millis_stats;

// last sample and delay time to set serial print frequencies
unsigned long lastSample;
//set delaytime to data serial print frequency wanted (ms, therefore every second if = 1000)
int delayTime = 2000;
//multiplier for ads1115 to set the bit voltage (depends on gains set in setup loop)
float gaintwo_multiplier = 0.0625; /* ADS1115  @ +/- 4.096V gain (16-bit results) */


void setup()
  // Setup code, this will run once:
{
  Wire.begin();
  Serial.begin(9600);
  //Set the channel for the first eurocircuit board
//The MOS sensors are typically gain one - there are a set amount of bins available for the data and this is to do with the range over which the bins are spread.
// A large range, means lower resolution data becasue there are limited bins, but the gain must cover the expected range. If the voltage goes above
// this gain then the signal will "flat out".
  tcaselect(4);
  ads1115_48.setGain(GAIN_ONE);        // 2x gain   +/- 2.048V  1 bit = 1mV      0.0625mV
  ads1115_48.begin();
  ads1115_49.setGain(GAIN_ONE);        // 2x gain   +/- 2.048V  1 bit = 1mV      0.0625mV
  ads1115_49.begin();
  ads1115_4A.setGain(GAIN_ONE);        // 2x gain   +/- 2.048V  1 bit = 1mV      0.0625mV
  ads1115_4A.begin();
  ads1115_4B.setGain(GAIN_ONE);        // 2x gain   +/- 2.048V  1 bit = 1mV      0.0625mV
  ads1115_4B.begin();
//Set the channel for the second eurocircuit board
  tcaselect(5);
  ads1115_48b.setGain(GAIN_ONE);        // 2x gain   +/- 2.048V  1 bit = 1mV      0.0625mV
  ads1115_48b.begin();
  ads1115_49b.setGain(GAIN_ONE);        // 2x gain   +/- 2.048V  1 bit = 1mV      0.0625mV
  ads1115_49b.begin();
  ads1115_4Ab.setGain(GAIN_ONE);        // 2x gain   +/- 2.048V  1 bit = 1mV      0.0625mV
  ads1115_4Ab.begin();
  ads1115_4Bb.setGain(GAIN_ONE);        // 2x gain   +/- 2.048V  1 bit = 1mV      0.0625mV
  ads1115_4Bb.begin();
// Set the channel for the ozone and NO2 sensors
  tcaselect(0); 
  ads1115_A.setGain(GAIN_ONE);        // 2x gain   +/- 2.048V  1 bit = 1mV      0.0625mV
  ads1115_A.begin();
// Set the channel for the NO and CO sensors.
  tcaselect(1);  
  ads1115_B.setGain(GAIN_ONE);        // 2x gain   +/- 2.048V  1 bit = 1mV      0.0625mV
  ads1115_B.begin();
// Set the channel for the voltag and pressure channels. 
//  tcaselect(6);
//  ads1115_C.setGain(GAIN_TWOTHIRDS);        // 2x gain   +/- 2.048V  1 bit = 1mV      0.0625mV
//  ads1115_C.begin();

//  if (!bmp.begin()){
//    Serial.println("Could not find a valid BMP085 or BMP180 sensor");
//    while(1){}
//  }

//  if (!htu.begin()) {
//    Serial.println("Couldn't find sensor!");
//    while (1);
//  }
  
//  Serial.println("End set up bd 2");
// Ensure all statistic instances are empty before any information is stored in them. 
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

  O3_1_OP1_stats.clear();
  O3_1_OP2_stats.clear();
  NO2_1_OP1_stats.clear();
  NO2_1_OP2_stats.clear();
  NO_1_OP1_stats.clear();
  NO_1_OP2_stats.clear();
  CO_1_OP1_stats.clear();
  CO_1_OP2_stats.clear();
  CO2_1_stats.clear();

//  Temp1_stats.clear();
//  Press1_stats.clear();
//  Temp2_stats.clear();
//  RH1_stats.clear();
//  HIH1_stats.clear();
//  LM65T1_stats.clear();
//  SV_stats.clear();

  pinMode(13, OUTPUT);
//End of set up code  
}
//multiplier for ads1115 to set the bit voltage (depends on gains set in setup loop)

float gaintwothirds_multiplier = 0.1875;
float gainone_multiplier = 0.125;
float multiplier = 0.125F*1e-3;
void takeSample()
{  
//  Serial.println("takesample");
// One green eurocircuit board to be connected to SD0,SC0 and the other is on the SD1/SC1 port. 
//take sample loop reads each sensor voltage and adds to statistic instance. Don't add the multiplier here, it is best to add it in later.
  tcaselect(4);
  MOS1_stats.add(ads1115_4B.readADC_Differential_0_1());
  MOS2_stats.add(ads1115_49.readADC_Differential_2_3());
  MOS3_stats.add(ads1115_4A.readADC_Differential_2_3());
  MOS4_stats.add(ads1115_48.readADC_Differential_2_3());
  MOS5_stats.add(ads1115_4A.readADC_Differential_0_1());
  MOS6_stats.add(ads1115_48.readADC_Differential_0_1());
  MOS7_stats.add(ads1115_4B.readADC_Differential_2_3());
  MOS8_stats.add(ads1115_49.readADC_Differential_0_1());
  tcaselect(5);
  MOS1b_stats.add(ads1115_4Bb.readADC_Differential_0_1());
  MOS2b_stats.add(ads1115_49b.readADC_Differential_2_3());
  MOS3b_stats.add(ads1115_4Ab.readADC_Differential_2_3());
  MOS4b_stats.add(ads1115_48b.readADC_Differential_2_3());
  MOS5b_stats.add(ads1115_4Ab.readADC_Differential_0_1());
  MOS6b_stats.add(ads1115_48b.readADC_Differential_0_1());
  MOS7b_stats.add(ads1115_4Bb.readADC_Differential_2_3());
  MOS8b_stats.add(ads1115_49b.readADC_Differential_0_1());

//  Temp1_stats.add(bmp.readTemperature());
//  Press1_stats.add(bmp.readPressure());
//  Temp2_stats.add(htu.readTemperature());
//  RH1_stats.add(htu.readHumidity());

  tcaselect(0);
  O3_1_OP1_stats.add(ads1115_A.readADC_SingleEnded(0));
  O3_1_OP2_stats.add(ads1115_A.readADC_SingleEnded(1));
  NO2_1_OP1_stats.add(ads1115_A.readADC_SingleEnded(2));
  NO2_1_OP2_stats.add(ads1115_A.readADC_SingleEnded(3));

  tcaselect(1);
  NO_1_OP1_stats.add(ads1115_B.readADC_SingleEnded(0));
  NO_1_OP2_stats.add(ads1115_B.readADC_SingleEnded(1));
  CO_1_OP1_stats.add(ads1115_B.readADC_SingleEnded(2));
  CO_1_OP2_stats.add(ads1115_B.readADC_SingleEnded(3));

//  tcaselect(6);
//  HIH1_stats.add(ads1115_C.readADC_SingleEnded(0));
//  LM65T1_stats.add(ads1115_C.readADC_SingleEnded(1));
//  SV_stats.add(ads1115_C.readADC_Differential_2_3());  
}
// Begin the loop to keep recording data.
void loop(void)
{
  // put your main code here, to run repeatedly:
  unsigned long currentMillis = millis();
  
  if (currentMillis - lastSample > delayTime)
  {
    lastSample = currentMillis;

// Telling the data to be averaged and the standard deviation for the MOS to be calculated. Multiply the signal by the correct gain multiplier.
    double MOS1_Av = MOS1_stats.average()*gainone_multiplier*1e-3;
    double MOS1_stddev =  MOS1_stats.pop_stdev()*gainone_multiplier*1e-3;    
    double MOS2_Av = MOS2_stats.average()*gainone_multiplier*1e-3;
    double MOS2_stddev =  MOS2_stats.pop_stdev()*gainone_multiplier*1e-3;
    double MOS3_Av = MOS3_stats.average()*gainone_multiplier*1e-3;
    double MOS3_stddev =  MOS3_stats.pop_stdev()*gainone_multiplier*1e-3;
    double MOS4_Av = MOS4_stats.average()*gainone_multiplier*1e-3;
    double MOS4_stddev =  MOS4_stats.pop_stdev()*gainone_multiplier*1e-3;
    double MOS5_Av = MOS5_stats.average()*gainone_multiplier*1e-3;
    double MOS5_stddev =  MOS5_stats.pop_stdev()*gainone_multiplier*1e-3;
    double MOS6_Av = MOS6_stats.average()*gainone_multiplier*1e-3;
    double MOS6_stddev =  MOS6_stats.pop_stdev()*gainone_multiplier*1e-3;
    double MOS7_Av = MOS7_stats.average()*gainone_multiplier*1e-3;
    double MOS7_stddev =  MOS7_stats.pop_stdev()*gainone_multiplier*1e-3;
    double MOS8_Av = MOS8_stats.average()*gainone_multiplier*1e-3;
    double MOS8_stddev =  MOS8_stats.pop_stdev()*gainone_multiplier*1e-3;

    double MOS1b_Av = MOS1b_stats.average()*gainone_multiplier*1e-3;
    double MOS1b_stddev =  MOS1b_stats.pop_stdev()*gainone_multiplier*1e-3;    
    double MOS2b_Av = MOS2b_stats.average()*gainone_multiplier*1e-3;
    double MOS2b_stddev =  MOS2b_stats.pop_stdev()*gainone_multiplier*1e-3;
    double MOS3b_Av = MOS3b_stats.average()*gainone_multiplier*1e-3;
    double MOS3b_stddev =  MOS3b_stats.pop_stdev()*gainone_multiplier*1e-3;
    double MOS4b_Av = MOS4b_stats.average()*gainone_multiplier*1e-3;
    double MOS4b_stddev =  MOS4b_stats.pop_stdev()*gainone_multiplier*1e-3;
    double MOS5b_Av = MOS5b_stats.average()*gainone_multiplier*1e-3;
    double MOS5b_stddev =  MOS5b_stats.pop_stdev()*gainone_multiplier*1e-3;
    double MOS6b_Av = MOS6b_stats.average()*gainone_multiplier*1e-3;
    double MOS6b_stddev =  MOS6b_stats.pop_stdev()*gainone_multiplier*1e-3;
    double MOS7b_Av = MOS7b_stats.average()*gainone_multiplier*1e-3;
    double MOS7b_stddev =  MOS7b_stats.pop_stdev()*gainone_multiplier*1e-3;
    double MOS8b_Av = MOS8b_stats.average()*gainone_multiplier*1e-3;
    double MOS8b_stddev =  MOS8b_stats.pop_stdev()*gainone_multiplier*1e-3;

    double O3_1_OP1_Av = O3_1_OP1_stats.average()*gainone_multiplier*1e-3;
    double O3_1_OP1_stddev =  O3_1_OP1_stats.pop_stdev()*gainone_multiplier*1e-3;
    double O3_1_OP2_Av = O3_1_OP2_stats.average()*gainone_multiplier*1e-3;
    double O3_1_OP2_stddev =  O3_1_OP2_stats.pop_stdev()*gainone_multiplier*1e-3;

    double NO2_1_OP1_Av = NO2_1_OP1_stats.average()*gainone_multiplier*1e-3;
    double NO2_1_OP1_stddev =  NO2_1_OP1_stats.pop_stdev()*gainone_multiplier*1e-3;
    double NO2_1_OP2_Av = NO2_1_OP2_stats.average()*gainone_multiplier*1e-3;
    double NO2_1_OP2_stddev =  NO2_1_OP2_stats.pop_stdev()*gainone_multiplier*1e-3;
 
    double NO_1_OP1_Av = NO_1_OP1_stats.average()*gainone_multiplier*1e-3;
    double NO_1_OP1_stddev =  NO_1_OP1_stats.pop_stdev()*gainone_multiplier*1e-3;
    double NO_1_OP2_Av = NO_1_OP2_stats.average()*gainone_multiplier*1e-3;
    double NO_1_OP2_stddev =  NO_1_OP2_stats.pop_stdev()*gainone_multiplier*1e-3;

    double CO_1_OP1_Av = CO_1_OP1_stats.average()*gainone_multiplier*1e-3;
    double CO_1_OP1_stddev =  CO_1_OP1_stats.pop_stdev()*gainone_multiplier*1e-3;
    double CO_1_OP2_Av = CO_1_OP2_stats.average()*gainone_multiplier*1e-3;
    double CO_1_OP2_stddev =  CO_1_OP2_stats.pop_stdev()*gainone_multiplier*1e-3;

//    double Temp1_Av = Temp1_stats.average();
//    double Temp1_stddev =  Temp1_stats.pop_stdev();
//    double Press1_Av = Press1_stats.average();
//    double Press1_stddev =  Press1_stats.pop_stdev();
//    double Temp2_Av = Temp2_stats.average();
//    double Temp2_stddev =  Temp2_stats.pop_stdev();
//    double RH1_Av = RH1_stats.average();
//    double RH1_stddev =  RH1_stats.pop_stdev();
//    double HIH1_Av = HIH1_stats.average()*gaintwothirds_multiplier*1e-3;
//    double HIH1_stddev =  HIH1_stats.pop_stdev()*gaintwothirds_multiplier*1e-3;
//    double LM65T1_Av = LM65T1_stats.average()*gaintwothirds_multiplier*1e-3;
//    double LM65T1_stddev =  LM65T1_stats.pop_stdev()*gaintwothirds_multiplier*1e-3;

//    double SV_Av = SV_stats.average()*gaintwothirds_multiplier*1e-3;
//    double SV_stddev =  SV_stats.pop_stdev()*gaintwothirds_multiplier*1e-3;  
 

// Print and store the average. Must call each multiplexer address before printing information from that section.  
      tcaselect(4);
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
      Serial.print(MOS8_Av, 8);
      Serial.print(",");

      tcaselect(5);
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
      Serial.print(MOS8b_Av, 8);
      Serial.print(",");

      tcaselect(0);
      Serial.print (O3_1_OP1_stats.count());    
      Serial.print (",");
      Serial.print (O3_1_OP1_Av, 8);
      Serial.print (",");
      Serial.print (O3_1_OP1_stddev, 8);
      Serial.print (",");
      Serial.print (O3_1_OP2_stats.count()); 
      Serial.print (",");
      Serial.print (O3_1_OP2_Av, 8);   
      Serial.print (",");
      Serial.print (O3_1_OP2_stddev, 8);
      Serial.print (",");
      Serial.print (NO2_1_OP1_stats.count());    
      Serial.print (",");
      Serial.print (NO2_1_OP1_Av, 8);
      Serial.print (",");
      Serial.print (NO2_1_OP1_stddev, 8);
      Serial.print (",");
      Serial.print (NO2_1_OP2_stats.count()); 
      Serial.print (",");
      Serial.print (NO2_1_OP2_Av, 8);   
      Serial.print (",");
      Serial.print (NO2_1_OP2_stddev, 8);
      Serial.print (",");
      tcaselect(1);
      Serial.print (NO_1_OP1_stats.count());    
      Serial.print (",");
      Serial.print (NO_1_OP1_Av, 8);
      Serial.print (",");
      Serial.print (NO_1_OP1_stddev, 8);
      Serial.print (",");
      Serial.print (NO_1_OP2_stats.count()); 
      Serial.print (",");
      Serial.print (NO_1_OP2_Av, 8);   
      Serial.print (",");
      Serial.print (NO_1_OP2_stddev, 8);
      Serial.print (",");
      Serial.print (CO_1_OP1_stats.count());    
      Serial.print (",");
      Serial.print (CO_1_OP1_Av, 8);
      Serial.print (",");
      Serial.print (CO_1_OP1_stddev, 8);
      Serial.print (",");
      Serial.print (CO_1_OP2_stats.count()); 
      Serial.print (",");
      Serial.print (CO_1_OP2_Av, 8);   
      Serial.print (",");
      Serial.print (CO_1_OP2_stddev, 8);
      Serial.println (",");
      
    
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

    O3_1_OP1_stats.clear();
    O3_1_OP2_stats.clear();
    NO2_1_OP1_stats.clear();
    NO2_1_OP2_stats.clear();
    NO_1_OP1_stats.clear();
    NO_1_OP2_stats.clear();
    CO_1_OP1_stats.clear();
    CO_1_OP2_stats.clear();
//    Temp1_stats.clear();
//    Press1_stats.clear();
//    Temp2_stats.clear();
//    RH1_stats.clear();
//    HIH1_stats.clear();
//    LM65T1_stats.clear();
//    SV_stats.clear();
    

    digitalWrite(13, !digitalRead(13));
  }

  takeSample();

  
}
