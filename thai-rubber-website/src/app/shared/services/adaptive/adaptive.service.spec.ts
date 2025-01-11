import { TestBed } from '@angular/core/testing';

import { AdaptiveService } from './adaptive.service';

describe('AdaptiveService', () => {
  let service: AdaptiveService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(AdaptiveService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
