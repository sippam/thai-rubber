import { DatePipe } from '@angular/common';
import { Component, HostListener, inject, OnInit } from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';
import {
  DateAdapter,
  MAT_DATE_FORMATS,
  MAT_DATE_LOCALE,
} from '@angular/material/core';
import { MatDatepickerModule } from '@angular/material/datepicker';
import {
  MatFormField,
  MatFormFieldModule,
  MatLabel,
} from '@angular/material/form-field';
import { MatIcon } from '@angular/material/icon';
import { RouterLink } from '@angular/router';
import { AdaptiveService } from '@services/adaptive/adaptive.service';
import { NgxChartsModule } from '@swimlane/ngx-charts';
import { ThaiDateAdapter } from 'src/app/shared/pipes/thai-date-adapter';
import { THAI_DATE_FORMATS } from 'src/app/shared/pipes/thai-date-formats';
import { TableComponent } from './table/table.component';

@Component({
  selector: 'app-adaptive-model',
  standalone: true,
  imports: [
    MatIcon,
    RouterLink,
    ReactiveFormsModule,
    NgxChartsModule,
    MatFormField,
    MatLabel,
    MatDatepickerModule,
    MatFormFieldModule,
    TableComponent,
  ],
  templateUrl: './adaptive-model.component.html',
  styleUrl: './adaptive-model.component.scss',
  providers: [
    { provide: DateAdapter, useClass: ThaiDateAdapter },
    { provide: MAT_DATE_LOCALE, useValue: 'th-TH' },
    { provide: MAT_DATE_FORMATS, useValue: THAI_DATE_FORMATS },
    DatePipe,
  ],
})
export class AdaptiveModelComponent implements OnInit {
  #adaptiveService = inject(AdaptiveService);
  view: [number, number] = [700, 400]; // Default chart size

  dataset_powder: {
    name: string;
    series: { name: string; value: number }[];
  }[] = [
    {
      name: 'accuracy_7_day',
      series: [],
    },
    {
      name: 'accuracy_14_day',
      series: [],
    },
    {
      name: 'accuracy_outbreak',
      series: [],
    },
  ];
  yScaleMinPowder = 0;

  dataset_newfall: {
    name: string;
    series: { name: string; value: number }[];
  }[] = [
    {
      name: 'การเกิดโรคในอีก 7 วัน',
      series: [],
    },
    {
      name: 'การเกิดโรคในอีก 14 วัน',
      series: [],
    },
    {
      name: 'ความเสี่ยงในการระบาด',
      series: [],
    },
  ];
  yScaleMinNewfall = 0;

  startDate: string | null = null; // Track start date
  endDate: string | null = null; // Track end date

  startDate2: string | null = null; // Track start date
  endDate2: string | null = null; // Track end date

  onDateRangeChange(event: any, type: 'start' | 'end') {
    if (type === 'start') {
      this.startDate = new Date(event.value).toISOString().split('T')[0];
    } else if (type === 'end') {
      this.endDate = new Date(event.value).toISOString().split('T')[0];

      // Trigger the API when end date is selected
      if (this.startDate && this.endDate) {
        this.#adaptiveService
          .getAdaptivePlotPowder('powder', this.startDate, this.endDate)
          .subscribe({
            next: (response: any) => {
              if (response.status == 200) {
                const newDataset: {
                  name: string;
                  series: { name: string; value: number }[];
                }[] = [
                  { name: 'การเกิดโรคในอีก 7 วัน', series: [] },
                  { name: 'การเกิดโรคในอีก 14 วัน', series: [] },
                  { name: 'ความเสี่ยงในการระบาด', series: [] },
                ];

                response.data.forEach((item: any) => {
                  newDataset[0].series.push({
                    name: new Date(item.create_at).toLocaleDateString(),
                    value: item.accuracy_7_day,
                  });
                  newDataset[1].series.push({
                    name: new Date(item.create_at).toLocaleDateString(),
                    value: item.accuracy_14_day,
                  });
                  newDataset[2].series.push({
                    name: new Date(item.create_at).toLocaleDateString(),
                    value: item.accuracy_outbreak,
                  });
                });

                this.dataset_powder = newDataset;

                const minValue = Math.min(
                  ...this.dataset_powder.flatMap((d) =>
                    d.series.map((s) => s.value)
                  )
                );

                this.yScaleMinPowder = minValue * 0.9;
              }
            },
            error: (error) => {
              console.error(error);
            },
          });
      }
    }
  }

  onDateRangeChange2(event: any, type: 'start' | 'end') {
    if (type === 'start') {
      this.startDate2 = new Date(event.value).toISOString().split('T')[0];
    } else if (type === 'end') {
      this.endDate2 = new Date(event.value).toISOString().split('T')[0];

      // Trigger the API when end date is selected
      if (this.startDate2 && this.endDate2) {
        this.#adaptiveService
          .getAdaptivePlotPowder('newfall', this.startDate2, this.endDate2)
          .subscribe({
            next: (response: any) => {
              if (response.status == 200) {
                const newDataset: {
                  name: string;
                  series: { name: string; value: number }[];
                }[] = [
                  { name: 'การเกิดโรคในอีก 7 วัน', series: [] },
                  { name: 'การเกิดโรคในอีก 14 วัน', series: [] },
                  { name: 'ความเสี่ยงในการระบาด', series: [] },
                ];

                response.data.forEach((item: any) => {
                  newDataset[0].series.push({
                    name: new Date(item.create_at).toLocaleDateString(),
                    value: item.accuracy_7_day,
                  });
                  newDataset[1].series.push({
                    name: new Date(item.create_at).toLocaleDateString(),
                    value: item.accuracy_14_day,
                  });
                  newDataset[2].series.push({
                    name: new Date(item.create_at).toLocaleDateString(),
                    value: item.accuracy_outbreak,
                  });
                });

                this.dataset_newfall = newDataset;

                const minValue = Math.min(
                  ...this.dataset_newfall.flatMap((d) =>
                    d.series.map((s) => s.value)
                  )
                );

                this.yScaleMinNewfall = minValue * 0.9;
              }
            },
            error: (error) => {
              console.error(error);
            },
          });
      }
    }
  }

  ngOnInit() {
    this.updateChartSize();

    this.#adaptiveService.getAdaptivePlotPowder('powder').subscribe({
      next: (response: any) => {
        if (response.status == 200) {
          const newDataset: {
            name: string;
            series: { name: string; value: number }[];
          }[] = [
            { name: 'การเกิดโรคในอีก 7 วัน', series: [] },
            { name: 'การเกิดโรคในอีก 14 วัน', series: [] },
            { name: 'ความเสี่ยงในการระบาด', series: [] },
          ];

          response.data.forEach((item: any) => {
            newDataset[0].series.push({
              name: new Date(item.create_at).toLocaleDateString(), // Format x-axis as date
              value: item.accuracy_7_day,
            });
            newDataset[1].series.push({
              name: new Date(item.create_at).toLocaleDateString(),
              value: item.accuracy_14_day,
            });
            newDataset[2].series.push({
              name: new Date(item.create_at).toLocaleDateString(),
              value: item.accuracy_outbreak,
            });
          });

          // Reassign the dataset to trigger change detection
          this.dataset_powder = newDataset;

          const minValue = Math.min(
            ...this.dataset_powder.flatMap((d) => d.series.map((s) => s.value))
          );

          this.yScaleMinPowder = minValue * 0.9;
        }
      },
      error: (error) => {
        console.error(error);
      },
    });

    this.#adaptiveService.getAdaptivePlotPowder('newfall').subscribe({
      next: (response: any) => {
        if (response.status == 200) {
          const newDataset: {
            name: string;
            series: { name: string; value: number }[];
          }[] = [
            { name: 'การเกิดโรคในอีก 7 วัน', series: [] },
            { name: 'การเกิดโรคในอีก 14 วัน', series: [] },
            { name: 'ความเสี่ยงในการระบาด', series: [] },
          ];

          response.data.forEach((item: any) => {
            newDataset[0].series.push({
              name: new Date(item.create_at).toLocaleDateString(), // Format x-axis as date
              value: item.accuracy_7_day,
            });
            newDataset[1].series.push({
              name: new Date(item.create_at).toLocaleDateString(),
              value: item.accuracy_14_day,
            });
            newDataset[2].series.push({
              name: new Date(item.create_at).toLocaleDateString(),
              value: item.accuracy_outbreak,
            });
          });

          // Reassign the dataset to trigger change detection
          this.dataset_newfall = newDataset;

          const minValue = Math.min(
            ...this.dataset_newfall.flatMap((d) => d.series.map((s) => s.value))
          );

          this.yScaleMinNewfall = minValue * 0.9;
        }
      },
      error: (error) => {
        console.error(error);
      },
    });
  }

  @HostListener('window:resize', ['$event'])
  onResize() {
    this.updateChartSize();
  }

  updateChartSize(): void {
    const width = window.innerWidth * 0.9; // 90% of the window width
    const height = window.innerHeight * 0.5; // 50% of the window height

    const widthLimit = 800;
    const heightLimit = 400;

    // Limit the chart size to prevent overflow
    if (width > widthLimit) {
      this.view = [widthLimit, height];
    } else if (height > heightLimit) {
      this.view = [width, heightLimit];
    } else {
      this.view = [width, height];
    }
  }

}
