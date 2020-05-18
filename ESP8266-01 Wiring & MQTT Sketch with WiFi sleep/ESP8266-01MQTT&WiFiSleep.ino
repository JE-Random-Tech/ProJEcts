#include "ESP8266WiFi.h"
#include <PubSubClient.h>
#include <Arduino_JSON.h>

#include "secret.h"

//TODO define pins
#define relaisuppin 3
#define relaisdownpin 2

char* wifi_ssid = wifissid;
char* wifi_password = wifipassword;

char* mqtt_server = mqttserver;
int mqtt_port = mqttport;
//Not necessary if password is not enabled on Broker
char* mqtt_clientID = "YOUR CLIENT ID";
char* mqtt_username = mqttusername;
char* mqtt_password = mqttpassword;
//TODO Channel to subscribe to ;-)
char* blinds01subscribe = "YouTube/JE_Random_Tech";

WiFiClient espClient;
PubSubClient client(espClient);

void setup() {
  
  pinMode(relaisuppin, OUTPUT);
  pinMode(relaisdownpin, OUTPUT);
  setup_wifi();
  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);
}

void setup_wifi() {

  delay(10);
  WiFi.begin(wifi_ssid, wifi_password);
  int NAcounts=0;
  while (WiFi.status() != WL_CONNECTED && NAcounts < 7 ) {
    delay(500);
    NAcounts++;
  }
  if(WiFi.status() == WL_CONNECTED)
  {
    //Succsefully connected
  }else{
    ESP.restart();  
  }
}

boolean fetchedretainedmsg=false;

void callback(char* topic, byte* payload, unsigned int length) {
  String msg;
  for (int i = 0; i < length; i++) {
    msg+=(char)payload[i];
  }
  fetchedretainedmsg=true;
  // Trick to debug if MQTT connection works client.publish("debug/test", "called", false);
  JSONVar msgobject = JSON.parse(msg);
  //TODO do something when channel subbed has new !RETAINED! message
  //To Test send something e.g via MQTT.fx to "YouTube/JE_Random_Tech" with Message: {"property": true} or {"property": false}
  if(msgobject.hasOwnProperty("property"))
  {
    digitalWrite(relaisuppin, (bool)msgobject["property"]);
  }
}

void reconnect1() {
  while (!client.connected()) {
    if (client.connect(mqtt_clientID,mqtt_username,mqtt_password)) {
      fetchedretainedmsg=false;
      //TODO Subscribe
      client.subscribe(blinds01subscribe);
      while(!fetchedretainedmsg)
      {
        client.loop();
        delay(100);  
      }      
    } else {
      delay(5000);
    }
  }
}

void loop() {
  if (WiFi.status()!=WL_CONNECTED) {
    setup_wifi();
  }
  if (!client.connected()) {
    reconnect1();
  }
  client.loop();
  client.unsubscribe(blinds01subscribe);
  client.disconnect();
  WiFi.disconnect();
  WiFi.mode(WIFI_OFF);
  WiFi.forceSleepBegin();
  delay(5000);
  WiFi.forceSleepWake();
  WiFi.mode(WIFI_STA);
  //Sleep for a few seconds
  delay(10);
  setup_wifi();
  reconnect1();

 //TODO publish eg. client.publish("subscribe/to", "YouTube_JE_RANDOM_TECH", true); ;-)

}
