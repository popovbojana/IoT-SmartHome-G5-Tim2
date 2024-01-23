import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Pi2Component } from './pi2.component';

describe('Pi2Component', () => {
  let component: Pi2Component;
  let fixture: ComponentFixture<Pi2Component>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [Pi2Component]
    });
    fixture = TestBed.createComponent(Pi2Component);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
