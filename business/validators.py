from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from PIL import Image
import os

def validate_image_file(value):
    """
    Validator untuk memastikan file yang diupload adalah gambar yang valid
    """
    if not value:
        return
    
    # Cek ekstensi file
    allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp']
    ext = os.path.splitext(value.name)[1].lower()
    
    if ext not in allowed_extensions:
        raise ValidationError(
            _('Format file tidak didukung. Gunakan format: %(extensions)s'),
            params={'extensions': ', '.join(allowed_extensions)}
        )
    
    # Cek ukuran file (max 5MB)
    max_size = 5 * 1024 * 1024  # 5MB
    if value.size > max_size:
        raise ValidationError(
            _('Ukuran file terlalu besar. Maksimal %(max_size)s MB'),
            params={'max_size': 5}
        )
    
    # Cek apakah file adalah gambar yang valid
    try:
        # Reset file pointer
        value.seek(0)
        
        # Coba buka gambar dengan PIL
        image = Image.open(value)
        image.verify()  # Verify image integrity
        
        # Reset file pointer lagi
        value.seek(0)
        
    except Exception as e:
        raise ValidationError(
            _('File bukan gambar yang valid atau gambar rusak. Error: %(error)s'),
            params={'error': str(e)}
        )

def validate_logo_file(value):
    """
    Validator khusus untuk logo dengan persyaratan tambahan
    """
    if not value:
        return
    
    # Gunakan validator dasar
    validate_image_file(value)
    
    # Cek ukuran file untuk logo (max 2MB)
    max_size = 2 * 1024 * 1024  # 2MB
    if value.size > max_size:
        raise ValidationError(
            _('Ukuran logo terlalu besar. Maksimal %(max_size)s MB'),
            params={'max_size': 2}
        )
    
    # Cek dimensi gambar
    try:
        value.seek(0)
        image = Image.open(value)
        width, height = image.size
        
        # Logo sebaiknya tidak terlalu kecil atau terlalu besar
        if width < 50 or height < 50:
            raise ValidationError(
                _('Logo terlalu kecil. Minimal %(min_size)sx%(min_size)s pixel'),
                params={'min_size': 50}
            )
        
        if width > 2000 or height > 2000:
            raise ValidationError(
                _('Logo terlalu besar. Maksimal %(max_size)sx%(max_size)s pixel'),
                params={'max_size': 2000}
            )
        
        value.seek(0)
        
    except Exception as e:
        if "Logo terlalu" in str(e):
            raise
        raise ValidationError(
            _('Logo bukan gambar yang valid. Error: %(error)s'),
            params={'error': str(e)}
        )

