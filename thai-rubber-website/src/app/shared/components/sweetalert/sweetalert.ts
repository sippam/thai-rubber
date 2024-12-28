import Swal from 'sweetalert2';

export const swalLoading = () => {
  Swal.fire({
    title: 'กำลังดำเนินการ...',
    html: 'กรุณารอสักครู่',
    allowOutsideClick: false,
    didOpen: () => {
      Swal.showLoading();
    },
  });
};

export const swalLoadingClose = () => {
  Swal.close();
};

export const swalSuccess = (title: string) => {
  return Swal.fire({
    title: title,
    icon: 'success',
    timer: 4000,
    confirmButtonText: 'ตกลง',
  });
};

export const swalError = (title: string) => {
  Swal.fire({
    title: title,
    icon: 'error',
    timer: 4000,
    confirmButtonText: 'ตกลง',
  });
};
