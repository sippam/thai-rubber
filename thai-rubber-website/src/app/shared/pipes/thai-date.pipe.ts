import { Pipe, PipeTransform } from '@angular/core';
import { formatDate } from '@angular/common';

@Pipe({
  name: 'thaiDate',
  standalone: true,
})

// export class ThaiDatePipe implements PipeTransform {
//   transform(
//     value: any,
//     format = 'dd MMMM yyyy',
//     locale = 'th-TH'
//   ): any {
//     const thaiYear = new Date(value).getFullYear() + 543;
//     const formattedDate = formatDate(value, format, locale);
//     return formattedDate.replace(/(\d{4})/, thaiYear.toString());
//   }
// }

// @Pipe({
//   name: 'thaiDateNoTime',
//   standalone: true,
// })
// export class ThaiDateNoTimePipe implements PipeTransform {
//   transform(value: any): string {
//     if (!value) return '';
//     // Only display the date without the time
//     const thaiDate = value.toLocaleDateString('th-TH', { year: 'numeric', month: 'long', day: 'numeric' });
//     return thaiDate;
//   }
// }
export class ThaiDatePipe implements PipeTransform {
  transform(value: any, format = 'dd MMMM yyyy', locale = 'th-TH'): any {
    if (!value) {
      return '-'; // Return a fallback string for undefined or null values
    }

    try {
      const date = new Date(value);
      if (isNaN(date.getTime())) {
        // Handle invalid dates
        return '-';
      }

      const thaiYear = date.getFullYear() + 543;
      const formattedDate = formatDate(date, format, locale);
      return formattedDate.replace(/(\d{4})/, thaiYear.toString());
    } catch (error) {
      console.error('ThaiDatePipe Error:', error);
      return '-'; // Fallback for unexpected errors
    }
  }
}

@Pipe({
  name: 'thaiDateNoTime',
  standalone: true,
})
export class ThaiDateNoTimePipe implements PipeTransform {
  transform(value: any): string {
    if (!value) return '-'; // Handle undefined or null values
    try {
      const date = new Date(value);
      if (isNaN(date.getTime())) {
        // Handle invalid dates
        return '-';
      }

      // Format the date to Thai without time
      return date.toLocaleDateString('th-TH', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
      });
    } catch (error) {
      console.error('ThaiDateNoTimePipe Error:', error);
      return '-'; // Fallback for unexpected errors
    }
  }
}
