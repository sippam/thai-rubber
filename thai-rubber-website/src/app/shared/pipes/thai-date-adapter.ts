import { DatePipe } from '@angular/common';
import { Injectable } from '@angular/core';
import { NativeDateAdapter } from '@angular/material/core';

@Injectable()
export class ThaiDateAdapter extends NativeDateAdapter {
  constructor(private datePipe: DatePipe) {
    super();
  }

  override getYear(date: Date): number {
    return date.getFullYear();
  }

  override format(date: Date, displayFormat: string): string {
    const day = date.getDate();
    const month = date.toLocaleString('th-TH', { month: 'long' });
    const year = date.getFullYear() + 543;
    return `${day} ${month} ${year}`;
  }

  // Override parse method to correctly handle the Thai year
  override parse(value: any): Date | null {
    if ((typeof value === 'string') && value.indexOf('/') > -1) {
      const str = value.split('/');
      const year = parseInt(str[2], 10) - 543;
      const month = parseInt(str[1], 10) - 1;
      const day = parseInt(str[0], 10);
      return new Date(year, month, day);
    }
    const timestamp = typeof value === 'number' ? value : Date.parse(value);
    return isNaN(timestamp) ? null : new Date(timestamp);
  }
}