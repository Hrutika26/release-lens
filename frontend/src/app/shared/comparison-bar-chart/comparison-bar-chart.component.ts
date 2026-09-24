import {AfterViewInit,
  Component,
  ElementRef,
  Input,
  OnChanges,
  SimpleChanges,
  ViewChild,
} from '@angular/core';

import * as d3 from 'd3';


export interface ComparisonChartItem {
  label: string;
  base: number;
  target: number;
}


@Component({
  selector: 'app-comparison-bar-chart',
  standalone: true,
  imports: [],
  templateUrl: './comparison-bar-chart.component.html',
  styleUrl: './comparison-bar-chart.component.css',
})
export class ComparisonBarChartComponent
  implements AfterViewInit, OnChanges {

  @ViewChild('chartContainer')
  private chartContainer?: ElementRef<HTMLDivElement>;

  @Input()
  data: ComparisonChartItem[] = [];
  @Input()
  maxItems = 10;

  @Input()
  chartTitle = '';
  @Input()
  baseLabel = 'Base';

  @Input()
  targetLabel = 'Target';

  @Input()
  unit = '';

  private viewInitialized = false;


  ngAfterViewInit(): void {
    this.viewInitialized = true;
    this.renderChart();
  }


  ngOnChanges(
    changes: SimpleChanges,
  ): void {
    if (
      this.viewInitialized &&
      changes['data']
    ) {
      this.renderChart();
    }
  }

private renderChart(): void {
  if (!this.chartContainer) {
    return;
  }

  const container =
    this.chartContainer.nativeElement;

  d3.select(container)
    .selectAll('*')
    .remove();

  const chartData = this.displayData;

  if (!chartData.length) {
    return;
  }

  const rowHeight = 42;
  const width = container.clientWidth || 800;
  const margin = {
    top: 20,
    right: 24,
    bottom: 30,
    left: 220,
  };

  const chartHeight =
    chartData.length * rowHeight;

  const height =
    chartHeight +
    margin.top +
    margin.bottom;

  const svg = d3
    .select(container)
    .append('svg')
    .attr('width', '100%')
    .attr('height', height)
    .attr(
      'viewBox',
      `0 0 ${width} ${height}`,
    );

  const innerWidth =
    width - margin.left - margin.right;

  const innerHeight =
    height - margin.top - margin.bottom;

  const chart = svg
    .append('g')
    .attr(
      'transform',
      `translate(${margin.left}, ${margin.top})`,
    );

  const y = d3
    .scaleBand<string>()
    .domain(chartData.map(item => item.label))
    .range([0, innerHeight])
    .padding(0.25);

  const subY = d3
    .scaleBand<string>()
    .domain(['base', 'target'])
    .range([0, y.bandwidth()])
    .padding(0.08);

  const maxValue =
    d3.max(
      chartData.flatMap(item => [
        item.base,
        item.target,
      ]),
    ) ?? 0;

  const x = d3
    .scaleLinear()
    .domain([0, maxValue * 1.1])
    .nice()
    .range([0, innerWidth]);

  chart
    .append('g')
    .call(d3.axisLeft(y))
    .call(axis =>
      axis.select('.domain').remove(),
    );

  chart
    .append('g')
    .attr(
      'transform',
      `translate(0, ${innerHeight})`,
    )
    .call(d3.axisBottom(x).ticks(5))
    .call(axis =>
      axis.select('.domain').remove(),
    );

  const groups = chart
    .selectAll<SVGGElement, ComparisonChartItem>(
      'g.endpoint-group',
    )
    .data(chartData)
    .join('g')
    .attr('class', 'endpoint-group')
    .attr(
      'transform',
      item =>
        `translate(0, ${y(item.label) ?? 0})`,
    );

  const baseBars = groups
    .append('rect')
    .attr('class', 'base-bar')
    .attr('x', 0)
    .attr(
      'y',
      subY('base') ?? 0,
    )
    .attr('height', subY.bandwidth())
    .attr('width', item => x(item.base));

  const targetBars = groups
    .append('rect')
    .attr('class', 'target-bar')
    .attr('x', 0)
    .attr(
      'y',
      subY('target') ?? 0,
    )
    .attr('height', subY.bandwidth())
    .attr('width', item => x(item.target));

  this.addTooltip(baseBars, targetBars, container);
}


private addTooltip(
  baseBars: d3.Selection<
    SVGRectElement,
    ComparisonChartItem,
    SVGGElement,
    unknown
  >,
  targetBars: d3.Selection<
    SVGRectElement,
    ComparisonChartItem,
    SVGGElement,
    unknown
  >,
  container: HTMLDivElement,
): void {

  const tooltip = d3
    .select(container)
    .append('div')
    .style('position', 'absolute')
    .style('z-index', '100')
    .style('padding', '10px 12px')
    .style('border', '1px solid #e2e8f0')
    .style('border-radius', '8px')
    .style('background', '#ffffff')
    .style('color', '#334155')
    .style('font-size', '12px')
    .style('line-height', '1.5')
    .style('pointer-events', 'none')
    .style('opacity', '0')
    .style('box-shadow', '0 6px 18px rgba(15, 23, 42, 0.12)')
    .style('white-space', 'nowrap');


  const showTooltip = (
    event: MouseEvent,
    item: ComparisonChartItem,
  ): void => {

    const [x, y] = d3.pointer(
      event,
      container,
    );

    const delta =
      item.base === 0
        ? null
        : (
            (
              item.target -
              item.base
            ) /
            item.base
          ) * 100;

          tooltip
  .html(`
    <div style="font-weight: 600; margin-bottom: 6px;">
      ${item.label}
    </div>

    <div>
      ${this.baseLabel}:
      ${item.base.toFixed(2)}${this.unit}
    </div>

    <div>
      ${this.targetLabel}:
      ${item.target.toFixed(2)}${this.unit}
    </div>
  `)
  .style('left', `${x + 12}px`)
  .style('top', `${y + 12}px`)
  .style('visibility', 'visible')
  .style('opacity', '1');
  };


  const moveTooltip = (
    event: MouseEvent,
  ): void => {

    const [x, y] = d3.pointer(
      event,
      container,
    );

    tooltip
      .style('left', `${x + 12}px`)
      .style('top', `${y + 12}px`);
  };


  const hideTooltip = (): void => {
tooltip
  .style('visibility', 'hidden')
  .style('opacity', '0');
  };


  baseBars
    .on('mouseenter', showTooltip)
    .on('mousemove', moveTooltip)
    .on('mouseleave', hideTooltip);


  targetBars
    .on('mouseenter', showTooltip)
    .on('mousemove', moveTooltip)
    .on('mouseleave', hideTooltip);
}

  private get displayData(): ComparisonChartItem[] {
  return [...this.data]
    .sort(
      (a, b) =>
        Math.max(b.base, b.target) -
        Math.max(a.base, a.target),
    )
    .slice(0, this.maxItems);
}
}