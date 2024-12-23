import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FollowDiseaseComponent } from './follow-disease.component';

describe('FollowDiseaseComponent', () => {
  let component: FollowDiseaseComponent;
  let fixture: ComponentFixture<FollowDiseaseComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [FollowDiseaseComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(FollowDiseaseComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
