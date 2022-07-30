import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AnimeLinkGuideComponent } from './anime-link-guide.component';

describe('AnimeLinkGuideComponent', () => {
  let component: AnimeLinkGuideComponent;
  let fixture: ComponentFixture<AnimeLinkGuideComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [AnimeLinkGuideComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(AnimeLinkGuideComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
