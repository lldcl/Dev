//import arduino packages
#include <Wire.h>
#include <Statistic.h>
#include <Adafruit_ADS1015.h>

//create instances for adafruit adc's on sensor board (each with unique adrs)
Adafruit_ADS1115 ads1115_48(0x48);
Adafruit_ADS1115 ads1115_49(0x49);
Adafruit_ADS1115 ads1115_4A(0x4A);
Adafruit_ADS1115 ads1115_4B(0x4B);

//create statistics for each sensor and millis
Statistic MOS1_stats;
Statistic MOS2_stats;
Statistic MOS3_stats;
Statistic MOS4_stats;
Statistic MOS5_stats;
Statistic MOS6_stats;
Statistic MOS7_stats;
Statistic MOS8_stats;
Statistic Temp_stats;
Statistic RH_stats;
Statistic Millis_stats;

// last sample and delay time to set serial print frequencies
unsigned long lastSample;
//set delaytime to data serial print frequency wanted (ms)
int delayTime = 1000;
//set temp and RH sensor analogue pins on arduino
int RH_pin = A1;
int Temp_pin = A0;

//multiplier for ads1115 to set the bit voltage (depends on gains set in setup loop)
float multiplier = 0.125F*1e-3;

  // The ADC input range (or gain) can be changed via the following
  // functions, but be careful never to exceed VDD +0.3V max, or to
  // exceed the upper and lower limits if you adjust the input range!
  // Setting these values incorrectly may destroy your ADC!
  //                                                                ADS1115
  //                                                                -------
  // ads.setGain(GAIN_TWOTHIRDS);  // 2/3x gain +/- 6.144V  1 bit = 0.1875mV (default)
  // ads.setGain(GAIN_ONE);        // 1x gain   +/- 4.096V  1 bit = 0.125mV
  // ads.setGain(GAIN_TWO);        // 2x gain   +/- 2.048V  1 bit = 0.0625mV
  // ads.setGain(GAIN_FOUR);       // 4x gain   +/- 1.024V  1 bit = 0.03125mV
  // ads.setGain(GAIN_EIGHT);      // 8x gain   +/- 0.512V  1 bit = 0.015625mV
  // ads.setGain(GAIN_SIXTEEN);    // 16x gain  +/- 0.256V  1 bit = 0.0078125mV
  
void setup(void)
{
  Wire.begin();
  Serial.begin(9600);
 //set adc gain and initialise 
  ads1115_48.setGain(GAIN_ONE);        // 1x gain   +/- 4.096V  1 bit = 0.125mV
  ads1115_48.begin();
  ads1115_49.setGain(GAIN_ONE);        // 1x gain   +/- 4.096V  1 bit = 0.125mV
  ads1115_49.begin();
  ads1115_4A.setGain(GAIN_ONE);        // 1x gain   +/- 4.096V  1 bit = 0.125mV
  ads1115_4A.begin();
  ads1115_4B.setGain(GAIN_ONE);        // 1x gain   +/- 4.096V  1 bit = 0.125mV
  ads1115_4B.begin();

//ensure all statistic instances are empty
  MOS1_stats.clear();
  MOS2_stats.clear();
  MOS3_stats.clear();
  MOS4_stats.clear();
  MOS5_stats.clear();
  MOS6_stats.clear();
  MOS7_stats.clear();
  MOS8_stats.clear();
  Temp_stats.clear();
  RH_stats.clear();
  Millis_stats.clear();
  
  pinMode(13,OUTPUT);
}

//take sample loop reads each sensor voltage and adds to statistic instance
void takeSample()
{
  MOS1_stats.add(ads1115_4B.readADC_Differential_0_1()*multiplier);
  MOS2_stats.add(ads1115_49.readADC_Differential_2_3()*multiplier);
  MOS3_stats.add(ads1115_4A.readADC_Differential_2_3()*multiplier);
  MOS4_stats.add(ads1115_48.readADC_Differential_2_3()*multiplier);
  MOS5_stats.add(ads1115_4A.readADC_Differential_0_1()*multiplier);
  MOS6_stats.add(ads1115_48.readADC_Differential_0_1()*multiplier);
  MOS7_stats.add(ads1115_4B.readADC_Differential_2_3()*multiplier);
  MOS8_stats.add(ads1115_49.readADC_Differential_0_1()*multiplier);
  Temp_stats.add(analogRead(Temp_pin)*0.49);
  RH_stats.add(analogRead(RH_pin));
  Millis_stats.add(millis());
  delay(10);
}

void loop(void)
{
  unsigned long currentMillis = millis();
 
 //once chosen delay time has lapsed create floats from statistics and print to serial 
  if (currentMillis - lastSample > delayTime)
  {
    lastSample = currentMillis;
    
    long Millis_min = Millis_stats.minimum();
    long Millis_max = Millis_stats.maximum();
    double MOS1_Av = MOS1_stats.average();
    double MOS1_stddev =  MOS1_stats.pop_stdev();    
    double MOS2_Av = MOS2_stats.average();
    double MOS2_stddev =  MOS2_stats.pop_stdev();
    double MOS3_Av = MOS3_stats.average();
    double MOS3_stddev =  MOS3_stats.pop_stdev();
    double MOS4_Av = MOS4_stats.average();
    double MOS4_stddev =  MOS4_stats.pop_stdev();
    double MOS5_Av = MOS5_stats.average();
    double MOS5_stddev =  MOS5_stats.pop_stdev();
    double MOS6_Av = MOS6_stats.average();
    double MOS6_stddev =  MOS6_stats.pop_stdev();
    double MOS7_Av = MOS7_stats.average();
    double MOS7_stddev =  MOS7_stats.pop_stdev();
    double MOS8_Av = MOS8_stats.average();
    double MOS8_stddev =  MOS8_stats.pop_stdev();
    double Temp_Av = Temp_stats.average();
    double Temp_stddev =  Temp_stats.pop_stdev();
    double RH_Av = RH_stats.average();
    double RH_stddev =  RH_stats.pop_stdev();

    digitalWrite(13,HIGH);

//    Serial.print(Millis_min);
//    Serial.print(",");
//    Serial.print(Millis_max);
//    Serial.print(",");
//    Serial.print(MOS1_stats.count());
//    Serial.print(",");    
    Serial.print(MOS1_Av, 8);
    Serial.print(",");
//    Serial.print(MOS1_stddev, 8);
//    Serial.print(",");
//    Serial.print(MOS2_stats.count());
//    Serial.print(",");    
    Serial.print(MOS2_Av, 8);
    Serial.print(",");
//    Serial.print(MOS2_stddev, 8);
//    Serial.print(",");
//    Serial.print(MOS3_stats.count());
//    Serial.print(",");    
    Serial.print(MOS3_Av, 8);
    Serial.print(",");
//    Serial.print(MOS3_stddev, 8);
//    Serial.print(",");
//    Serial.print(MOS4_stats.count());
//    Serial.print(",");    
    Serial.print(MOS4_Av, 8);
    Serial.print(",");
//    Serial.print(MOS4_stddev, 8);
//    Serial.print(",");
//    Serial.print(MOS5_stats.count());
//    Serial.print(",");    
    Serial.print(MOS5_Av, 8);
    Serial.print(",");
//    Serial.print(MOS5_stddev, 8);
//    Serial.print(",");
//    Serial.print(MOS6_stats.count());
//    Serial.print(",");    
    Serial.print(MOS6_Av, 8);
    Serial.print(",");
//    Serial.print(MOS6_stddev, 8);
//    Serial.print(",");
//    Serial.print(MOS7_stats.count());
//    Serial.print(",");    
    Serial.print(MOS7_Av, 8);
    Serial.print(",");
//    Serial.print(MOS7_stddev, 8);
//    Serial.print(",");
//    Serial.print(MOS8_stats.count());
//    Serial.print(",");    
    Serial.println(MOS8_Av, 8);
//    Serial.print(",");
//    Serial.print(MOS8_stddev, 8);
//    Serial.print(",");
//    Serial.print(Temp_Av);
//    Serial.print(",");
//    Serial.print(Temp_stddev);
//    Serial.print(",");
//    Serial.print(((((RH_Av*4.9)/5.)-0.16)/0.0062)/(1.0546-(0.00216*Temp_Av))*0.001);
//    Serial.print(",");
//    Serial.println(((((RH_stddev*4.9)/5.)-0.16)/0.0062)/(1.0546-(0.00216*Temp_Av))*0.001);

    digitalWrite(13,LOW);
    
    //clear the serial port and empty statistic instances
    Serial.flush();
    MOS1_stats.clear();
    MOS2_stats.clear();
    MOS3_stats.clear();
    MOS4_stats.clear();
    MOS5_stats.clear();
    MOS6_stats.clear();
    MOS7_stats.clear();
    MOS8_stats.clear();
    Temp_stats.clear();
    RH_stats.clear();
    Millis_stats.clear();

  }
  
  takeSample();  
}
  
