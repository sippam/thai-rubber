import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [RouterLink],
  templateUrl: './home.component.html',
  styleUrl: './home.component.scss'
})
export class HomeComponent {
  redirect = [
    {
      "text": "ติดตามสถานการณ์โรค",
      "redirect": "/follow-disease",
      "bg": "#A9E7C9"
    },
    {
      "text": "ฐานข้อมูลโรคในยางพารา",
      "redirect": "/database",
      "bg": "#F4D9A9"
    },
    {
      "text": "การทำงานของ Adaptive Model",
      "redirect": "/adaptive-model",
      "bg": "#E49F26"
    }
  ]
}
