import { Component } from '@angular/core';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent {
  isSystemActive: boolean = true;
  isAlarmActive: boolean = true;
  isAlarmClockActive: boolean = true;
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

  onKeyPress(digit: string): void {
    const index = this.passcode.findIndex(entry => entry === '');
    if (index !== -1) {
      this.passcode[index] = digit;
    }
    console.log('Passcode:', this.passcode.join(''));
  }

  onKeyPressReceiver(digit: string): void {
    alert('Pressed: ' + digit);
    console.log('Pressed: ' + digit);
  }

  onApplyClickDMS(): void {
    console.log('Apply clicked. Passcode:', this.passcode.join(''));
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
      console.log('Set alarm clock for: ', formattedTime);
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
}
