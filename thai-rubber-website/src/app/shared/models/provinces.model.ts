export interface Provinces {
  id: number;
  name_en: string;
  name_th: string;
  geography_id: number;
  amphure: District[];
  created_at: string | null;
  updated_at: string | null;
  deleted_at: string | null;
}

export interface District {
  id: number;
  name_en: string;
  name_th: string;
  province_id: number;
  tambon: Tambon[];
  created_at: string | null;
  updated_at: string | null;
  deleted_at: string | null;
}

export interface Tambon {
  id: number;
  name_en: string;
  name_th: string;
  amphure_id: number;
  zip_code: number;
  created_at: string | null;
  updated_at: string | null;
  deleted_at: string | null;
}
