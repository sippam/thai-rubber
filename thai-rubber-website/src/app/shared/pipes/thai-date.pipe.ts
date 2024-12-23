import { Pipe, PipeTransform } from '@angular/core';
import { formatDate } from '@angular/common';

@Pipe({
  name: 'thaiDate',
  standalone: true,
})

export class ThaiDatePipe implements PipeTransform {
  transform(
    value: any,
    format = 'dd MMMM yyyy',
    locale = 'th-TH'
  ): any {
    const thaiYear = new Date(value).getFullYear() + 543;
    const formattedDate = formatDate(value, format, locale);
    return formattedDate.replace(/(\d{4})/, thaiYear.toString());
  }
}

@Pipe({
  name: 'thaiDateNoTime',
  standalone: true,
})
export class ThaiDateNoTimePipe implements PipeTransform {
  transform(value: any): string {
    if (!value) return '';
    // Only display the date without the time
    const thaiDate = value.toLocaleDateString('th-TH', { year: 'numeric', month: 'long', day: 'numeric' });
    return thaiDate;
  }
}