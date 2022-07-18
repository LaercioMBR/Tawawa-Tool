import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MmoComponent } from './mmo.component';

describe('MmoComponent', () => {
  let component: MmoComponent;
  let fixture: ComponentFixture<MmoComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [MmoComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(MmoComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
