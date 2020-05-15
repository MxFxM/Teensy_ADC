#include <Arduino.h>

//#define BRUTE_FORCE_TEST
# define SYNC_READ_TEST

#ifdef SYNC_READ_TEST
#include <ADC.h>
ADC *adc = new ADC();
ADC::Sync_result result1;
ADC::Sync_result result2;
IntervalTimer timer_measurement;
volatile boolean b_newSamples = false;
void sample(void);
#endif

void setup() {
  // put your setup code here, to run once:
  pinMode(A0, INPUT);
  pinMode(A1, INPUT);
  pinMode(A2, INPUT);
  pinMode(A3, INPUT);

  pinMode(LED_BUILTIN, OUTPUT);

  Serial.begin(9600); // usb is always 12Mbit/s

  #ifdef SYNC_READ_TEST
  // adc 0
  adc->adc0->setAveraging(1);
  adc->adc0->setResolution(16);
  adc->adc0->setConversionSpeed(ADC_CONVERSION_SPEED::VERY_HIGH_SPEED);
  adc->adc0->setSamplingSpeed(ADC_SAMPLING_SPEED::VERY_HIGH_SPEED);
  // adc 1
  adc->adc1->setAveraging(1);
  adc->adc1->setResolution(16);
  adc->adc1->setConversionSpeed(ADC_CONVERSION_SPEED::VERY_HIGH_SPEED);
  adc->adc1->setSamplingSpeed(ADC_SAMPLING_SPEED::VERY_HIGH_SPEED);

  timer_measurement.begin(sample, 10);
  #endif

}

void loop() {
  // put your main code here, to run repeatedly:
  #ifdef BRUTE_FORCE_TEST
  analogRead(A0);
  digitalWriteFast(LED_BUILTIN, HIGH);
  analogRead(A1);
  digitalWriteFast(LED_BUILTIN, LOW);
  analogRead(A2);
  digitalWriteFast(LED_BUILTIN, HIGH);
  analogRead(A3);
  digitalWriteFast(LED_BUILTIN, LOW);
  #endif

  #ifdef SYNC_READ_TEST
  if (b_newSamples) { 
    digitalWriteFast(LED_BUILTIN, HIGH);
    Serial.write(0x00);
    Serial.write(result1.result_adc0);
    Serial.write(result1.result_adc0>>8);
    Serial.write(result1.result_adc1);
    Serial.write(result1.result_adc1>>8);
    Serial.write(result2.result_adc0);
    Serial.write(result2.result_adc0>>8);
    Serial.write(result2.result_adc1);
    Serial.write(result2.result_adc1>>8);
    b_newSamples = false;
    digitalWriteFast(LED_BUILTIN, LOW);
  }
  #endif
}

#ifdef SYNC_READ_TEST
void sample(void) {
  result1 = adc->analogSyncRead(A0, A1);
  result2 = adc->analogSyncRead(A2, A3);

  b_newSamples = true;
}
#endif

/* RESULTS:
 *
 * BRUTE_FORCE_TEST
 * this test runs 4 analog read commands one after the other
 * the sampling rate seems very consistent at about 28kHz
 * each analog read takes about the same time at 17.7us
 * this can be used for sampling four analog pins, but it is rather slow
 * and each measurement is offset by the time 17.7us
 * the time offset can be removed mathematically but i think it can get better
 * 
 * SYNC_READ_TEST
 * this test runs 2 analog synchronous reads
 * at 8 bit resolution:
 *  the sampling rate seems very consistent at about 353kHz
 *  each synchronous read takes about 1.4us
 * at 12 bit resolution:
 *  the sampling rate is barely slower with 312kHz
 *  each synchronous read takes about 1.6us
 * at 16 bit resolution:
 *  the sampling rate is about the same at 311kHz
 * when setting the sampling and conversion rate to very high speed,
 * the samples per second can be brought down even further
 * the time offset can be removed mathematically
 * a function to split the results is necessary and will lower the maximum rate
 */