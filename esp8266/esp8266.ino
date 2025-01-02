
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <ArduinoJson.h>

#define WIFI_SSID "TP-Link_CAEC"
#define WIFI_PASSWORD "81391028"

#define LED_PIN LED_BUILTIN 
#define LED_CTR D2 
void setup() {
  Serial.begin(9600);
  pinMode(LED_PIN, OUTPUT);
  pinMode(LED_CTR, OUTPUT); 
  digitalWrite(LED_PIN, HIGH);
  digitalWrite(LED_CTR, LOW);
  // connect to wifi.
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("connecting");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }
  Serial.println();
  Serial.print("connected: ");
  Serial.println(WiFi.localIP());

  
}

int n = 0;
int ledst=0;

int ctrled=0;

void loop() {
  // set value
  
  ledst = !ledst;
  digitalWrite(LED_PIN, ledst ? LOW : HIGH);
  
  
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin("http://192.168.38.100:8080/getdata"); // 替換為目標網址
    int httpCode = http.GET(); // 發送 GET 請求

    if (httpCode > 0) {
      String payload = http.getString(); // 獲取回應資料
      Serial.println("HTTP Response:");
      Serial.println(payload); // 輸出到串列監視器

      StaticJsonDocument<512> doc; // 調整大小以適應你的 JSON 結構
      DeserializationError error = deserializeJson(doc, payload);
      /*
      JsonDocument doc;
      doc["ID"]="0";
      doc["name"]="1";
      deserializeJson(doc, Serial);
      */
      String MID= doc["ID"];
      String state= doc["state"];
      
      Serial.print("ID: ");
      Serial.println(MID);
      Serial.print("state:");
      Serial.println(state);
      if(state=="on"){
        digitalWrite(LED_CTR, HIGH);
      }else if(state=="off"){
        digitalWrite(LED_CTR, LOW);
      }
    } else {
      Serial.print("Error on HTTP request: ");
      Serial.println(httpCode);
    }
    http.end(); // 關閉連接
  } else {
    Serial.println("Wi-Fi not connected");
  }

  delay(3000);
}
