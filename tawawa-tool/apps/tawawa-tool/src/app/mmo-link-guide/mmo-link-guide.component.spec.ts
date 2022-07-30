import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MmoLinkGuideComponent } from './mmo-link-guide.component';

describe('MmoLinkGuideComponent', () => {
  let component: MmoLinkGuideComponent;
  let fixture: ComponentFixture<MmoLinkGuideComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [MmoLinkGuideComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(MmoLinkGuideComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
