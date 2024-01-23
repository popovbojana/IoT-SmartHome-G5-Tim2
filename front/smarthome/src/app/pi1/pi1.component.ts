import { Component } from '@angular/core';
import { SafeResourceUrl, DomSanitizer } from '@angular/platform-browser';

@Component({
  selector: 'app-pi1',
  templateUrl: './pi1.component.html',
  styleUrls: ['./pi1.component.css']
})
export class Pi1Component {
  grafanaUrl: SafeResourceUrl;

  constructor(private sanitizer: DomSanitizer) {
    this.grafanaUrl = this.sanitizer.bypassSecurityTrustResourceUrl('http://localhost:3000/d/f49a4897-ab0b-4f5a-aee3-b60db1f61fe5/dht?orgId=1&from=1706028288518&to=1706049888518&viewPanel=1');
  }
}
