import { Component } from '@angular/core';
import { Button } from '../devices/button';
import { Diode } from '../devices/diode';
import { DUS } from '../devices/dus';
import { Buzzer } from '../devices/buzzer';
import { PIR } from '../devices/pir';
import { DMS } from '../devices/dms';
import { DHT } from '../devices/dht';

@Component({
  selector: 'app-pi1',
  templateUrl: './pi1.component.html',
  styleUrls: ['./pi1.component.css']
})
export class Pi1Component {
  ds1: Button = {
    pi: 'PI1',
    name: 'DS1',
    simulated: false,
    timestamp: '',
    door_unlocked: false,
    code: ''
  }

  dl: Diode = {
    pi: '',
    name: '',
    simulated: false,
    timestamp: '',
    light_state: false
  }

  dus1: DUS = {
    pi: '',
    name: '',
    simulated: false,
    timestamp: '',
    distance: 0
  }

  db: Buzzer = {
    pi: '',
    name: '',
    simulated: false,
    timestamp: '',
    pitch: 0,
    duration: 0
  }

  dpir1: PIR = {
    pi: '',
    name: '',
    simulated: false,
    timestamp: '',
    motion_detected: false
  }

  dms: DMS = {
    pi: '',
    name: '',
    simulated: false,
    timestamp: '',
    key: ''
  }

  rpir1: PIR = {
    pi: '',
    name: '',
    simulated: false,
    timestamp: '',
    motion_detected: false
  }

  rpir2: PIR = {
    pi: '',
    name: '',
    simulated: false,
    timestamp: '',
    motion_detected: false
  }

  rdht1: DHT = {
    pi: '',
    name: '',
    simulated: false,
    timestamp: '',
    humidity: 0,
    temperature: 0
  }

  rdht2: DHT = {
    pi: '',
    name: '',
    simulated: false,
    timestamp: '',
    humidity: 0,
    temperature: 0
  }

  constructor() {
  }
}
