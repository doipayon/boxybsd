/*
  ESP32 HTTPClient Jokes API Example

  https://wokwi.com/projects/342032431249883731

  Copyright (C) 2022, Uri Shaked
*/

#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <Adafruit_GFX.h>
#include <Adafruit_ILI9341.h>

const char* ssid = "Wokwi-GUEST";
const char* password = "";

#define BTN_PIN 5
#define TFT_DC 2
#define TFT_CS 15
Adafruit_ILI9341 tft = Adafruit_ILI9341(TFT_CS, TFT_DC);

const String url = "https://wttr.in/werribee?format=j1";

String getJoke() {
  HTTPClient http;
  http.useHTTP10(true);
  http.begin(url);
  http.GET();
  String result = http.getString();

  DynamicJsonDocument doc(2048);
  DeserializationError error = deserializeJson(doc, result);

  // Test if parsing succeeds.
  if (error) {
    Serial.print("deserializeJson() failed: ");
    Serial.println(error.c_str());
    return "<error>";
  }

  //Serial.println(doc["current_condition"].as<String>());
  //doc["stargazers"]["totalCount"];
  /*
  String joke = doc["current_condition"]["FeelsLikeC"].as<String>();
  String setup = doc["current_condition"]["humidity"].as<String>();
  String delivery = doc["current_condition"]["localObsDateTime"].as<String>();
  */
  //String curr_cond = doc["current_condition"].as<String>();
  String temp = "Feels like " + doc["current_condition"][0]["FeelsLikeC"].as<String>();
  
  http.end();

  //return joke + setup + "  " + delivery;
  return temp;
}

void nextJoke() {
  tft.setTextColor(ILI9341_WHITE);
  tft.println("\nLoading joke...");

  String joke = getJoke();
  tft.setTextColor(ILI9341_GREEN);
  tft.println(joke);
}

void setup() {
  pinMode(BTN_PIN, INPUT_PULLUP);

  WiFi.begin(ssid, password, 6);

  tft.begin();
  tft.setRotation(1);

  tft.setTextColor(ILI9341_WHITE);
  tft.setTextSize(2);
  tft.print("Connecting to WiFi");

  while (WiFi.status() != WL_CONNECTED) {
    delay(100);
    tft.print(".");
  }

  tft.print("\nOK! IP=");
  tft.println(WiFi.localIP());

  nextJoke();
}

void loop() {
  if (digitalRead(BTN_PIN) == LOW) {
    tft.fillScreen(ILI9341_BLACK);
    tft.setCursor(0, 0);
    nextJoke();
  }

  delay(100);
}
