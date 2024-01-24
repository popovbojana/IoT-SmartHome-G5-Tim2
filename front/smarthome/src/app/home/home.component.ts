import { Component, OnInit } from '@angular/core';
import { AlarmClock, DevicesService } from '../service/devices/devices.service';
import { DMS } from '../devices/dms';
import { IR } from '../devices/ir';
import { Socket } from 'ngx-socket-io';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css'],
})
export class HomeComponent implements OnInit {
  isSystemActive: boolean = false;
  isAlarmActive: boolean = false;
  isAlarmClockActive: boolean = false;
  peopleInside: number = 0;

  keypadRows: string[][] = [
    ['1', '2', '3', 'A'],
    ['4', '5', '6', 'B'],
    ['7', '8', '9', 'C'],
    ['*', '0', '#', 'D']
  ];

  receiverRows: string[][] = [
    ['1', '2', '3'],
    ['4', '5', '6'],
    ['7', '8', '9'],
    ['*', '0', '#'],
    ['↑'],
    ['←', 'OK', '→'],
    ['↓'],
  ];

  passcode: string[] = ['', '', '', ''];

  constructor(private deviceService: DevicesService, private socket: Socket) { }

  ngOnInit() {
    //system
    this.socket.on('system', (response: boolean) => {
      this.isSystemActive = response;
    });

    //alarm
    this.socket.on('alarm', (response: boolean) => {
      this.isAlarmActive = response;
    });

    //alarm_clock
    this.socket.on('alarm_clock', (response: boolean) => {
      this.isAlarmClockActive = response;
    });

    //people_inside
    this.socket.on('people_inside', (response: number) => {
      this.peopleInside = response;
    });
  }

  onKeyPress(digit: string): void {
    const index = this.passcode.findIndex(entry => entry === '');
    if (index !== -1) {
      this.passcode[index] = digit;
    }
    console.log('Passcode: ', this.passcode.join(''));
  }

  onKeyPressReceiver(digit: string): void {
    var currentDate = new Date();
    var currentTimestamp = Math.floor(currentDate.getTime() / 1000);

    const irDTO: IR = {
      pi: "PI3",
      name: "BIR",
      simulated: true,
      timestamp: currentTimestamp.toString(),
      button: digit
    }

    this.deviceService.ir(irDTO).subscribe((response) => {
      console.log(response);
    });

    alert('Pressed: ' + digit);
  }

  onApplyClickDMS(): void { 
    const passcodeString = this.passcode.map(num => num.toString()).join(',');
    alert('Passcode: ' + passcodeString);

    var currentDate = new Date();
    var currentTimestamp = Math.floor(currentDate.getTime() / 1000);

    const dmsDTO: DMS = {
      pi: "PI1",
      name: "DMS",
      simulated: true,
      timestamp: currentTimestamp.toString(),
      key: passcodeString
    }

    this.deviceService.dms(dmsDTO).subscribe((response) => {
      console.log(response);
    });

    this.resetPasscode();
  }

  onCancelClickDMS(): void {
    console.log('Cancel clicked. Passcode reset.');
    this.resetPasscode();
  }

  private resetPasscode(): void {
    this.passcode = ['', '', '', ''];
  }

  selectedHour: string[] = ['', ''];
  selectedMinute: string[] = ['', ''];

  onApplyClickAlarmClock(): void {
    const isValidTime = this.validateTime();
    
    if (isValidTime) {
      const formattedTime = this.selectedHour.join('') + ':' + this.selectedMinute.join('');
      alert('Set alarm clock for: ' + formattedTime);
      
      const alarmClock: AlarmClock = {
        time: formattedTime,
        action: "add"
      }
  
      this.deviceService.alarmClock(alarmClock).subscribe((response) => {
        console.log(response);
      });

      this.onCancelClickAlarmClock();
    } else {
      alert('Invalid time. Please enter valid digits for hours and minutes.');
      console.log('Invalid time. Please enter valid digits for hours and minutes.');
    }
  }

  onCancelClickAlarmClock(): void {
    this.selectedHour = ['', ''];
    this.selectedMinute = ['', ''];
  }

  private validateTime(): boolean {
    const isHourValid =
      (/^[0-1]$/.test(this.selectedHour[0]) && /^\d$/.test(this.selectedHour[1])) ||
      (/^2$/.test(this.selectedHour[0]) && /^[0-3]$/.test(this.selectedHour[1]));

    const isMinuteValid = /^[0-5]$/.test(this.selectedMinute[0]) && /^\d$/.test(this.selectedMinute[1]);

    return isHourValid && isMinuteValid;
  }

  disableAlarmClock(): void {
    const alarmClock: AlarmClock = {
      time: '',
      action: "turn-off"
    }

    this.deviceService.alarmClock(alarmClock).subscribe((response) => {
      console.log(response);
    });
  }
}
