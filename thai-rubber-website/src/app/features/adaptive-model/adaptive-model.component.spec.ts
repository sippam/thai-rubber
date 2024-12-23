import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AdaptiveModelComponent } from './adaptive-model.component';

describe('AdaptiveModelComponent', () => {
  let component: AdaptiveModelComponent;
  let fixture: ComponentFixture<AdaptiveModelComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AdaptiveModelComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(AdaptiveModelComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
