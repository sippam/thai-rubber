import { MatDateFormats } from '@angular/material/core';

export const THAI_DATE_FORMATS: MatDateFormats = {
  parse: {
    dateInput: 'DD/MM/YYYY',
  },
  display: {
    dateInput: 'd MMMM yyyy',
    monthYearLabel: 'MMM yyyy',
    dateA11yLabel: 'DD/MM/YYYY',
    monthYearA11yLabel: 'MMM yyyy',
  }
};
