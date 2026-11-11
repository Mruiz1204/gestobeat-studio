/*
  GestoBeat · ESP32 en Wokwi — Miguel Ruiz
  Recibe por MQTT las notas que se tocan en la app y las acompaña:
  enciende el LED de la nota y la toca en el buzzer.

  Mensaje esperado (tópico gestobeat_miguelruiz):
    {"nota": "Mi", "instrumento": "piano"}

  Conexiones:
    LED Do  (rojo)     → GPIO 13
    LED Re  (naranja)  → GPIO 12
    LED Mi  (amarillo) → GPIO 14
    LED Fa  (lima)     → GPIO 33
    LED Sol (verde)    → GPIO 27
    LED La  (morado)   → GPIO 26
    Buzzer             → GPIO 25
*/

#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

const char* ssid = "Wokwi-GUEST";
const char* password = "";
const char* mqtt_server = "broker.hivemq.com";
const int mqtt_port = 1883;
const char* topico = "gestobeat_miguelruiz";

const char* NOMBRES[6] = {"Do", "Re", "Mi", "Fa", "Sol", "La"};
const int LEDS[6] = {13, 12, 14, 33, 27, 26};
const int FRECUENCIAS[6] = {523, 587, 659, 698, 784, 880};   // Do5, Re5, Mi5, Fa5, Sol5, La5
const int BUZZER = 25;
const unsigned long DURACION = 220;                      // ms que dura cada nota

WiFiClient espClient;
PubSubClient client(espClient);

int ledEncendido = -1;
unsigned long apagarEn = 0;
unsigned long notasRecibidas = 0;

void tocarNota(int i) {
  if (ledEncendido >= 0) digitalWrite(LEDS[ledEncendido], LOW);
  digitalWrite(LEDS[i], HIGH);
  tone(BUZZER, FRECUENCIAS[i], DURACION);
  ledEncendido = i;
  apagarEn = millis() + DURACION + 60;
}

void callback(char* topic, byte* payload, unsigned int length) {
  StaticJsonDocument<200> doc;
  DeserializationError error = deserializeJson(doc, payload, length);
  if (error) {
    Serial.print("JSON inválido: ");
    Serial.println(error.c_str());
    return;
  }
  const char* nota = doc["nota"] | "";
  const char* instrumento = doc["instrumento"] | "-";
  for (int i = 0; i < 6; i++) {
    if (strcasecmp(nota, NOMBRES[i]) == 0) {
      tocarNota(i);
      notasRecibidas++;
      Serial.printf("#%lu  Nota: %-3s  (%s)\n", notasRecibidas, NOMBRES[i], instrumento);
      return;
    }
  }
  Serial.printf("Nota desconocida: %s\n", nota);
}

void conectarWiFi() {
  Serial.print("Conectando a WiFi");
  WiFi.begin(ssid, password, 6);   // canal 6: así Wokwi conecta al instante
  while (WiFi.status() != WL_CONNECTED) {
    delay(250);
    Serial.print(".");
  }
  Serial.println(" listo");
}

void reconectar() {
  while (!client.connected()) {
    Serial.print("Conectando a MQTT... ");
    String id = "esp32-gestobeat-" + String(random(0xffff), HEX);
    if (client.connect(id.c_str())) {
      Serial.println("MQTT conectado");
      client.subscribe(topico);
      Serial.printf("Escuchando el tópico %s\n", topico);
    } else {
      Serial.printf("falló (rc=%d), reintento en 2 s\n", client.state());
      delay(2000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  for (int i = 0; i < 6; i++) pinMode(LEDS[i], OUTPUT);
  pinMode(BUZZER, OUTPUT);

  // Saludo: recorre las cinco notas
  for (int i = 0; i < 6; i++) {
    digitalWrite(LEDS[i], HIGH);
    tone(BUZZER, FRECUENCIAS[i], 120);
    delay(150);
    digitalWrite(LEDS[i], LOW);
  }

  conectarWiFi();
  randomSeed(micros());
  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);
}

void loop() {
  if (!client.connected()) reconectar();
  client.loop();
  if (ledEncendido >= 0 && millis() > apagarEn) {
    digitalWrite(LEDS[ledEncendido], LOW);
    ledEncendido = -1;
  }
}
