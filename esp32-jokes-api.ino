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

const String url = "https://wttr.in/Melbourne,Australia?format=j1";

String getWeather() {
  HTTPClient http;
  http.useHTTP10(true);
  http.begin(url);
  http.GET();
  String result = http.getString();
  String temp = "";
  
  DynamicJsonDocument doc(2048);
  DeserializationError error = deserializeJson(doc, result);
    // Test if parsing succeeds.
  if (error) {
    Serial.print("deserializeJson() failed: ");
    Serial.println(error.c_str());
    return "<error>";
  }

  temp += "Feels like " + doc["current_condition"][0]["FeelsLikeC"].as<String>();
  temp += "\nMax: " + doc["weather"][0]["maxtempC"].as<String>();
  temp += "\nMin: " + doc["weather"][0]["mintempC"].as<String>();
  
  /*
  DynamicJsonDocument doc(2048);
  DeserializationError error = deserializeJson(doc, result);

  // Test if parsing succeeds.
  if (error) {
    Serial.print("deserializeJson() failed: ");
    Serial.println(error.c_str());
    return "<error>";
  }
  String type = doc["type"].as<String>();
  String joke = doc["joke"].as<String>();
  String setup = doc["setup"].as<String>();
  String delivery = doc["delivery"].as<String>();
  */
  http.end();
  return temp;
  //return type.equals("single") ? joke : setup + "  " + delivery;
}

void showWeather() {
  tft.setTextColor(ILI9341_WHITE);
  tft.println("\nLoading weather...");

  String weather = getWeather();
  tft.setTextColor(ILI9341_GREEN);
  tft.println(weather);
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

  showWeather();
}

void loop() {
  if (digitalRead(BTN_PIN) == LOW) {
    tft.fillScreen(ILI9341_BLACK);
    tft.setCursor(0, 0);
    showWeather();
  }

  delay(100);
}