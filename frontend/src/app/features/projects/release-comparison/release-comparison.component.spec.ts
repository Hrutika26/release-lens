import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ReleaseComparisonComponent } from './release-comparison.component';

describe('ReleaseComparisonComponent', () => {
  let component: ReleaseComparisonComponent;
  let fixture: ComponentFixture<ReleaseComparisonComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ReleaseComparisonComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ReleaseComparisonComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
