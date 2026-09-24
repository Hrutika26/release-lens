import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ComparisonBarChartComponent } from './comparison-bar-chart.component';

describe('ComparisonBarChartComponent', () => {
  let component: ComparisonBarChartComponent;
  let fixture: ComponentFixture<ComparisonBarChartComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ComparisonBarChartComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ComparisonBarChartComponent);
    component = fixture.componentInstance;
    component.data = [
      { label: 'GET /api/health', base: 120, target: 140 },
      { label: 'GET /api/users', base: 80, target: 90 },
    ];
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should show the tooltip when the pointer enters a bar', () => {
    const bar = fixture.nativeElement.querySelector('.base-bar') as SVGRectElement;
    const tooltip = fixture.nativeElement.querySelector('.chart-tooltip') as HTMLDivElement;

    expect(bar).toBeTruthy();
    expect(tooltip).toBeTruthy();

    bar.dispatchEvent(new PointerEvent('pointerenter', {
      bubbles: true,
      clientX: 100,
      clientY: 50,
    }));

    expect(tooltip.style.visibility).toBe('visible');
    expect(tooltip.style.opacity).toBe('1');
  });
});
