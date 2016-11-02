#include <Wire.h>
extern "C" { 
#include "utility/twi.h"  // from Wire library, so we can do bus scanning
}

#include <Statistic.h>

#include <Adafruit_BMP085.h>
Adafruit_BMP085 bmp;
// adrs = 77

#include <Adafruit_HTU21DF.h>
Adafruit_HTU21DF htu;
// adrs = 40

#include <Adafruit_ADS1015.h>
Adafruit_ADS1115 ads1115_A;
Adafruit_ADS1115 ads1115_B;
Adafruit_ADS1115 ads1115_C;

Adafruit_ADS1115 ads1115_48(0x48);
Adafruit_ADS1115 ads1115_49(0x49);
Adafruit_ADS1115 ads1115_4A(0x4A);
Adafruit_ADS1115 ads1115_4B(0x4B);

float gaintwothirds_multiplier = 0.1875;
float gainone_multiplier = 0.125;
float gaintwo_multiplier = 0.0625; /* ADS1115  @ +/- 4.096V gain (16-bit results) */

Statistic O3_1_OP1_stats;
Statistic O3_1_OP2_stats;
Statistic NO2_1_OP1_stats;
Statistic NO2_1_OP2_stats;
Statistic NO_1_OP1_stats;
Statistic NO_1_OP2_stats;
Statistic CO_1_OP1_stats;
Statistic CO_1_OP2_stats;
Statistic CO2_1_stats;

Statistic MOS1_stats;
Statistic MOS2_stats;
Statistic MOS3_stats;
Statistic MOS4_stats;
Statistic MOS5_stats;
Statistic MOS6_stats;
Statistic MOS7_stats;
Statistic MOS8_stats;

Statistic Temp1_stats;
Statistic Press1_stats;
Statistic Temp2_stats;
Statistic RH1_stats;
Statistic HIH1_stats;
Statistic LM65T1_stats;

unsigned long lastSample;
int delayTime = 2000;


#define TCAADDR 0x70
 
void tcaselect(uint8_t i) 
{
  if (i > 7) return;
  Wire.beginTransmission(TCAADDR);
  Wire.write(1 << i);
  Wire.endTransmission();  
}


void setup(void) 
{
  Wire.begin();
  Serial.begin(9600); 

  //                                                                ADS1015  ADS1115
  //                                                                -------  -------
  // ads.setGain(GAIN_TWOTHIRDS);  // 2/3x gain +/- 6.144V  1 bit = 3mV      0.1875mV (default)
  // ads.setGain(GAIN_ONE);        // 1x gain   +/- 4.096V  1 bit = 2mV      0.125mV
  // ads.setGain(GAIN_TWO);        // 2x gain   +/- 2.048V  1 bit = 1mV      0.0625mV
  // ads.setGain(GAIN_FOUR);       // 4x gain   +/- 1.024V  1 bit = 0.5mV    0.03125mV
  // ads.setGain(GAIN_EIGHT);      // 8x gain   +/- 0.512V  1 bit = 0.25mV   0.015625mV
  // ads.setGain(GAIN_SIXTEEN);    // 16x gain  +/- 0.256V  1 bit = 0.125mV  0.0078125mV

  ads1115_48.setGain(GAIN_ONE);        // 2x gain   +/- 2.048V  1 bit = 1mV      0.0625mV
  ads1115_48.begin();
  ads1115_49.setGain(GAIN_ONE);        // 2x gain   +/- 2.048V  1 bit = 1mV      0.0625mV
  ads1115_49.begin();
  ads1115_4A.setGain(GAIN_ONE);        // 2x gain   +/- 2.048V  1 bit = 1mV      0.0625mV
  ads1115_4A.begin();
  ads1115_4B.setGain(GAIN_ONE);        // 2x gain   +/- 2.048V  1 bit = 1mV      0.0625mV
  ads1115_4B.begin();

  tcaselect(0); 
  ads1115_A.setGain(GAIN_ONE);        // 2x gain   +/- 2.048V  1 bit = 1mV      0.0625mV
  ads1115_A.begin();

  tcaselect(1);  
  ads1115_B.setGain(GAIN_ONE);        // 2x gain   +/- 2.048V  1 bit = 1mV      0.0625mV
  ads1115_B.begin();

  tcaselect(2);
  ads1115_C.setGain(GAIN_TWOTHIRDS);        // 2x gain   +/- 2.048V  1 bit = 1mV      0.0625mV
  ads1115_C.begin();

  if (!bmp.begin()){
    Serial.println("Could not find a valid BMP085 or BMP180 sensor");
    while(1){}
  }

  if (!htu.begin()) {
    Serial.println("Couldn't find sensor!");
    while (1);
  }

  O3_1_OP1_stats.clear();
  O3_1_OP2_stats.clear();
  NO2_1_OP1_stats.clear();
  NO2_1_OP2_stats.clear();
  NO_1_OP1_stats.clear();
  NO_1_OP2_stats.clear();
  CO_1_OP1_stats.clear();
  CO_1_OP2_stats.clear();
  CO2_1_stats.clear();

  MOS1_stats.clear();
  MOS2_stats.clear();
  MOS3_stats.clear();
  MOS4_stats.clear();
  MOS5_stats.clear();
  MOS6_stats.clear();
  MOS7_stats.clear();
  MOS8_stats.clear();

  Temp1_stats.clear();
  Press1_stats.clear();
  Temp2_stats.clear();
  RH1_stats.clear();
  HIH1_stats.clear();
  LM65T1_stats.clear();

}

void takeSample()
{
  Temp1_stats.add(bmp.readTemperature());
  Press1_stats.add(bmp.readPressure());
  Temp2_stats.add(htu.readTemperature());
  RH1_stats.add(htu.readHumidity());

  MOS1_stats.add(ads1115_4B.readADC_Differential_0_1());
  MOS2_stats.add(ads1115_49.readADC_Differential_2_3());
  MOS3_stats.add(ads1115_4A.readADC_Differential_2_3());
  MOS4_stats.add(ads1115_48.readADC_Differential_2_3());
  MOS5_stats.add(ads1115_4A.readADC_Differential_0_1());
  MOS6_stats.add(ads1115_48.readADC_Differential_0_1());
  MOS7_stats.add(ads1115_4B.readADC_Differential_2_3());
  MOS8_stats.add(ads1115_49.readADC_Differential_0_1());
 
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

  tcaselect(2);
  HIH1_stats.add(ads1115_C.readADC_SingleEnded(0));
  LM65T1_stats.add(ads1115_C.readADC_SingleEnded(1));
//  CO2_1_stats.add(ads1115_C.readADC_Differential_2_3());

}


void loop(void) 
{
  unsigned long currentMillis = millis();
  
  if (currentMillis - lastSample > delayTime)
  {
    lastSample = currentMillis;

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

//    double CO2_1_Av = CO2_1_stats.average()*gaintwothirds_multiplier*1e-3;
//    double CO2_1_stddev =  CO2_1_stats.pop_stdev()*gaintwothirds_multiplier*1e-3;

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

    double Temp1_Av = Temp1_stats.average();
    double Temp1_stddev =  Temp1_stats.pop_stdev();
    double Press1_Av = Press1_stats.average();
    double Press1_stddev =  Press1_stats.pop_stdev();
    double Temp2_Av = Temp2_stats.average();
    double Temp2_stddev =  Temp2_stats.pop_stdev();
    double RH1_Av = RH1_stats.average();
    double RH1_stddev =  RH1_stats.pop_stdev();
    double HIH1_Av = HIH1_stats.average()*gaintwothirds_multiplier*1e-3;
    double HIH1_stddev =  HIH1_stats.pop_stdev()*gaintwothirds_multiplier*1e-3;
    double LM65T1_Av = LM65T1_stats.average()*gaintwothirds_multiplier*1e-3;
    double LM65T1_stddev =  LM65T1_stats.pop_stdev()*gaintwothirds_multiplier*1e-3;

//    Serial.print ("O3");
//    Serial.print (",");
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

//    Serial.print ("NO2");
//    Serial.print (",");
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

//    Serial.print ("NO");
//    Serial.print (",");
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

//    Serial.print ("CO");
//    Serial.print (",");
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
    Serial.print (",");
    
//    Serial.print ("CO2");
//    Serial.print (",");
//    Serial.print (CO2_1_Av, 8);   
//    Serial.print (",");
//    Serial.println (CO2_1_stddev, 8);
//    Serial.print(",");

    Serial.print(MOS1_stats.count());
    Serial.print(",");    
    Serial.print(MOS1_Av, 8);
    Serial.print(",");
    Serial.print(MOS1_stddev, 8);
    Serial.print(",");
    Serial.print(MOS2_stats.count());
    Serial.print(",");    
    Serial.print(MOS2_Av, 8);
    Serial.print(",");
    Serial.print(MOS2_stddev, 8);
    Serial.print(",");
    Serial.print(MOS3_stats.count());
    Serial.print(",");    
    Serial.print(MOS3_Av, 8);
    Serial.print(",");
    Serial.print(MOS3_stddev, 8);
    Serial.print(",");
    Serial.print(MOS4_stats.count());
    Serial.print(",");    
    Serial.print(MOS4_Av, 8);
    Serial.print(",");
    Serial.print(MOS4_stddev, 8);
    Serial.print(",");
    Serial.print(MOS5_stats.count());
    Serial.print(",");    
    Serial.print(MOS5_Av, 8);
    Serial.print(",");
    Serial.print(MOS5_stddev, 8);
    Serial.print(",");
    Serial.print(MOS6_stats.count());
    Serial.print(",");    
    Serial.print(MOS6_Av, 8);
    Serial.print(",");
    Serial.print(MOS6_stddev, 8);
    Serial.print(",");
    Serial.print(MOS7_stats.count());
    Serial.print(",");    
    Serial.print(MOS7_Av, 8);
    Serial.print(",");
    Serial.print(MOS7_stddev, 8);
    Serial.print(",");
    Serial.print(MOS8_stats.count());
    Serial.print(",");    
    Serial.print(MOS8_Av, 8);
    Serial.print(",");
    Serial.print(MOS8_stddev, 8);
    
    Serial.print(",");
    Serial.print(Temp1_Av);
    Serial.print(",");
    Serial.print(Temp1_stddev);
    Serial.print(",");
    Serial.print(Press1_Av);
    Serial.print(",");
    Serial.print(Press1_stddev);
    Serial.print(",");
    Serial.print(Temp2_Av);
    Serial.print(",");
    Serial.print(Temp2_stddev);
    Serial.print(",");
    Serial.print(RH1_Av);
    Serial.print(",");
    Serial.print(RH1_stddev);
    Serial.print(",");
    Serial.print(HIH1_Av);
    Serial.print(",");
    Serial.print(HIH1_stddev);
    Serial.print(",");
    Serial.print(LM65T1_Av,8);
    Serial.print(",");
    Serial.println(LM65T1_stddev);
    
    Serial.flush();
    O3_1_OP1_stats.clear();
    O3_1_OP2_stats.clear();
    NO2_1_OP1_stats.clear();
    NO2_1_OP2_stats.clear();
    NO_1_OP1_stats.clear();
    NO_1_OP2_stats.clear();
    CO_1_OP1_stats.clear();
    CO_1_OP2_stats.clear();
    
//    CO2_1_stats.clear();

    MOS1_stats.clear();
    MOS2_stats.clear();
    MOS3_stats.clear();
    MOS4_stats.clear();
    MOS5_stats.clear();
    MOS6_stats.clear();
    MOS7_stats.clear();
    MOS8_stats.clear();

    Temp1_stats.clear();
    Press1_stats.clear();
    Temp2_stats.clear();
    RH1_stats.clear();
    HIH1_stats.clear();
    LM65T1_stats.clear();

  }
  
  takeSample();  
}
