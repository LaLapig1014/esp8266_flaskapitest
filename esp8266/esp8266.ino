
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <ArduinoJson.h>

//#define WIFI_SSID "TP-Link_CAEC"
//#define WIFI_PASSWORD "81391028"
#define WIFI_SSID "CHT0606-1"
#define WIFI_PASSWORD "0933766044"

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
    WiFiClientSecure client;

  /* Add this */
    client.setInsecure();

    http.begin(client,"https://esp8266-flaskapitest.vercel.app/getdata"); 

    http.setFollowRedirects(HTTPC_STRICT_FOLLOW_REDIRECTS);
    int httpCode = http.GET(); // 發送 GET 請求
    
    Serial.print("HTTP Response Code: ");
    Serial.println(httpCode);
    if (httpCode > 0) {
      String payload = http.getString(); // 獲取回應資料
      Serial.println("HTTP Response:");
      Serial.println(payload); // 輸出到串列監視器
      
      //StaticJsonDocument<512> doc; // 調整大小以適應你的 JSON 結構
      //DeserializationError error = deserializeJson(doc, payload);
      DynamicJsonDocument doc(512);  // 使用動態內存分配來處理 JSON 資料
      DeserializationError error = deserializeJson(doc, payload);

      String MID= doc["ID"];
      String status= doc["status"];
      
      Serial.print("ID: ");
      Serial.println(MID);
      Serial.print("status:");
      Serial.println(status);
      if(status=="on"){
        digitalWrite(LED_CTR, HIGH);
      }else if(status=="off"){
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
  
  delay(1000);
}
