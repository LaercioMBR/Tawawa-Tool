import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MangaLinkGuideComponent } from './manga-link-guide.component';

describe('MangaLinkGuideComponent', () => {
  let component: MangaLinkGuideComponent;
  let fixture: ComponentFixture<MangaLinkGuideComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [MangaLinkGuideComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(MangaLinkGuideComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
