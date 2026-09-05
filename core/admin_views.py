"""
Custom admin views for admin panel
"""
import os
import json
import subprocess
from datetime import datetime
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.conf import settings
from django.core.management import call_command
from django.db import transaction
from core.models import DatabaseResetConfig, CustomUser
from core.forms import DatabaseResetConfigForm


def custom_admin_login(request):
    """
    Custom login view for admin panel
    """
    if request.user.is_authenticated:
        return redirect('/admin-panel/')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    next_url = request.GET.get('next', '/admin-panel/')
                    return redirect(next_url)
                else:
                    messages.error(request, 'Akun tidak aktif.')
            else:
                messages.error(request, 'Username atau password salah.')
        else:
            messages.error(request, 'Username dan password harus diisi.')
    
    return render(request, 'admin_panel/login.html')


@login_required
def custom_admin_logout(request):
    """
    Custom logout view for admin panel
    """
    logout(request)
    messages.success(request, 'Anda telah berhasil logout.')
    return redirect('/admin-panel/login/')


@login_required
def admin_dashboard(request):
    """
    Admin dashboard view
    """
    # Get recent reset configurations
    recent_configs = DatabaseResetConfig.objects.all()[:5]
    
    # Get backup files
    backup_dir = os.path.join(settings.BASE_DIR, 'backups')
    backup_files = []
    if os.path.exists(backup_dir):
        for root, dirs, files in os.walk(backup_dir):
            for file in files:
                if file.startswith('backup_'):
                    file_path = os.path.join(root, file)
                    file_size = os.path.getsize(file_path)
                    file_time = os.path.getmtime(file_path)
                    backup_files.append({
                        'name': file,
                        'path': file_path,
                        'size': file_size,
                        'created': datetime.fromtimestamp(file_time),
                    })
    
    # Sort by creation time (newest first)
    backup_files.sort(key=lambda x: x['created'], reverse=True)
    backup_files = backup_files[:5]  # Show only 5 most recent
    
    context = {
        'user': request.user,
        'page_title': 'Dashboard Admin Panel',
        'recent_configs': recent_configs,
        'backup_files': backup_files,
    }
    return render(request, 'admin_panel/dashboard.html', context)


@login_required
def database_reset_list(request):
    """
    List all database reset configurations
    """
    configs = DatabaseResetConfig.objects.all().order_by('-created_at')
    
    context = {
        'page_title': 'Database Reset Configurations',
        'configs': configs,
        'active_menu': 'database_reset',
        'active_submenu': 'database_reset_list',
    }
    return render(request, 'admin_panel/database_reset_list.html', context)


@login_required
def database_reset_create(request):
    """
    Create new database reset configuration
    """
    if request.method == 'POST':
        form = DatabaseResetConfigForm(request.POST)
        if form.is_valid():
            config = form.save(commit=False)
            config.created_by = request.user
            config.save()
            messages.success(request, 'Konfigurasi reset database berhasil dibuat!')
            return redirect('core:database_reset_list')
    else:
        form = DatabaseResetConfigForm()
    
    context = {
        'page_title': 'Buat Konfigurasi Reset Database',
        'form': form,
        'active_menu': 'database_reset',
        'active_submenu': 'database_reset_create',
    }
    return render(request, 'admin_panel/database_reset_form.html', context)


@login_required
def database_reset_edit(request, config_id):
    """
    Edit database reset configuration
    """
    config = get_object_or_404(DatabaseResetConfig, id=config_id)
    
    if request.method == 'POST':
        form = DatabaseResetConfigForm(request.POST, instance=config)
        if form.is_valid():
            form.save()
            messages.success(request, 'Konfigurasi reset database berhasil diperbarui!')
            return redirect('core:database_reset_list')
    else:
        form = DatabaseResetConfigForm(instance=config)
    
    context = {
        'page_title': 'Edit Konfigurasi Reset Database',
        'form': form,
        'config': config,
        'active_menu': 'database_reset',
        'active_submenu': 'database_reset_edit',
    }
    return render(request, 'admin_panel/database_reset_form.html', context)


@login_required
def database_reset_detail(request, config_id):
    """
    Detail database reset configuration
    """
    config = get_object_or_404(DatabaseResetConfig, id=config_id)
    
    context = {
        'page_title': f'Detail Konfigurasi: {config.name}',
        'config': config,
        'active_menu': 'database_reset',
        'active_submenu': 'database_reset_detail',
    }
    return render(request, 'admin_panel/database_reset_detail.html', context)


@login_required
def database_reset_execute(request, config_id):
    """
    Execute database reset configuration
    """
    config = get_object_or_404(DatabaseResetConfig, id=config_id)
    
    if request.method == 'POST':
        try:
            # Update config status
            config.status = 'running'
            config.executed_by = request.user
            config.executed_at = timezone.now()
            config.save()
            
            # Execute reset command
            result = execute_reset_command(config)
            
            if result['success']:
                config.status = 'completed'
                config.completed_at = timezone.now()
                config.execution_log = result['log']
                config.records_deleted = result['records_deleted']
                messages.success(request, 'Reset database berhasil dieksekusi!')
            else:
                config.status = 'failed'
                config.error_log = result['error']
                messages.error(request, f'Reset database gagal: {result["error"]}')
            
            config.save()
            
        except Exception as e:
            config.status = 'failed'
            config.error_log = str(e)
            config.save()
            messages.error(request, f'Error saat eksekusi reset: {str(e)}')
        
        return redirect('core:database_reset_detail', config_id=config_id)
    
    context = {
        'page_title': f'Eksekusi Reset: {config.name}',
        'config': config,
        'active_menu': 'database_reset',
        'active_submenu': 'database_reset_execute',
    }
    return render(request, 'admin_panel/database_reset_execute.html', context)


def execute_reset_command(config):
    """
    Execute reset command and return result
    """
    try:
        # Prepare command arguments
        cmd_args = ['python', 'manage.py', 'reset_database']
        
        # Add config-specific arguments
        if config.reset_type == 'full':
            cmd_args.extend(['--type', 'full'])
        elif config.reset_type == 'selective':
            cmd_args.extend(['--type', 'selective'])
        else:
            # Default to selective if no type specified
            cmd_args.extend(['--type', 'selective'])
        
        # Add module arguments
        modules = []
        if config.reset_penduduk:
            modules.append('penduduk')
        if config.reset_dusun:
            modules.append('dusun')
        if config.reset_lorong:
            modules.append('lorong')
        if config.reset_rt_rw:
            modules.append('rt_rw')
        if config.reset_keluarga:
            modules.append('keluarga')
        if config.reset_pelajar:
            modules.append('pelajar')
        if config.reset_disabilitas:
            modules.append('disabilitas')
        if config.reset_beneficiaries:
            modules.append('beneficiaries')
        if config.reset_business:
            modules.append('business')
        if config.reset_complaints:
            modules.append('complaints')
        if config.reset_documents:
            modules.append('documents')
        if config.reset_tourism:
            modules.append('tourism')
        if config.reset_posyandu:
            modules.append('posyandu')
        if config.reset_news:
            modules.append('news')
        if config.reset_organization:
            modules.append('organization')
        if config.reset_layanan:
            modules.append('layanan')
        if config.reset_letters:
            modules.append('letters')
        
        # If no modules selected, default to penduduk for selective reset
        if not modules and config.reset_type == 'selective':
            modules.append('penduduk')
        
        if modules:
            cmd_args.extend(['--modules'] + modules)
        
        # Add other options
        if config.backup_before_reset:
            cmd_args.append('--backup')
        # Note: No --no-backup argument exists, so we just don't add --backup
        
        if config.keep_users:
            cmd_args.append('--keep-users')
        
        if config.keep_settings:
            cmd_args.append('--keep-settings')
        
        if config.keep_media:
            cmd_args.append('--keep-media')
        
        cmd_args.append('--force')  # Skip confirmation
        
        # Execute command
        result = subprocess.run(
            cmd_args,
            capture_output=True,
            text=True,
            cwd=settings.BASE_DIR
        )
        
        if result.returncode == 0:
            return {
                'success': True,
                'log': result.stdout,
                'records_deleted': {}  # This would need to be parsed from output
            }
        else:
            return {
                'success': False,
                'error': result.stderr
            }
            
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


@login_required
def database_backup_list(request):
    """
    List all database backups
    """
    backup_dir = os.path.join(settings.BASE_DIR, 'backups')
    backup_files = []
    
    if os.path.exists(backup_dir):
        for root, dirs, files in os.walk(backup_dir):
            for file in files:
                if file.startswith('backup_'):
                    file_path = os.path.join(root, file)
                    file_size = os.path.getsize(file_path)
                    file_time = os.path.getmtime(file_path)
                    backup_files.append({
                        'name': file,
                        'path': file_path,
                        'size': file_size,
                        'created': datetime.fromtimestamp(file_time),
                        'relative_path': os.path.relpath(file_path, settings.BASE_DIR),
                    })
    
    # Sort by creation time (newest first)
    backup_files.sort(key=lambda x: x['created'], reverse=True)
    
    context = {
        'page_title': 'Database Backups',
        'backup_files': backup_files,
        'active_menu': 'database_reset',
        'active_submenu': 'database_backup_list',
    }
    return render(request, 'admin_panel/database_backup_list.html', context)


@login_required
def database_backup_create(request):
    """
    Create new database backup
    """
    if request.method == 'POST':
        try:
            # Get form data
            format_type = request.POST.get('format', 'json')
            compress = request.POST.get('compress') == 'on'
            include_media = request.POST.get('include_media') == 'on'
            cleanup_old = request.POST.get('cleanup_old') == 'on'
            include_apps = request.POST.getlist('include_apps')
            
            # SQL-specific options
            sql_data_only = request.POST.get('sql_data_only') == 'on'
            sql_structure_only = request.POST.get('sql_structure_only') == 'on'
            sql_options = request.POST.get('sql_options', '')
            
            # Prepare command arguments
            cmd_args = ['python', 'manage.py', 'backup_database']
            
            # Add format
            cmd_args.extend(['--format', format_type])
            
            if compress:
                cmd_args.append('--compress')
            
            if include_media:
                cmd_args.append('--media')
            
            if cleanup_old:
                cmd_args.extend(['--keep', '10'])  # Keep only 10 recent backups
            
            # Handle SQL-specific options
            if format_type == 'sql':
                if sql_data_only:
                    cmd_args.append('--sql-data-only')
                if sql_structure_only:
                    cmd_args.append('--sql-structure-only')
                if sql_options:
                    cmd_args.extend(['--sql-options', sql_options])
            
            # Handle app selection (only for non-SQL formats)
            if format_type != 'sql' and include_apps:
                # Get all available apps
                from django.apps import apps
                all_apps = [app.label for app in apps.get_app_configs()]
                exclude_apps = [app for app in all_apps if app not in include_apps]
                
                if exclude_apps:
                    cmd_args.extend(['--exclude'] + exclude_apps)
            
            # Execute backup command
            result = subprocess.run(
                cmd_args,
                capture_output=True,
                text=True,
                cwd=settings.BASE_DIR
            )
            
            if result.returncode == 0:
                messages.success(request, 'Backup database berhasil dibuat!')
            else:
                error_msg = f'Gagal membuat backup: {result.stderr}'
                if result.stdout:
                    error_msg += f'\nOutput: {result.stdout}'
                messages.error(request, error_msg)
                
        except Exception as e:
            messages.error(request, f'Error saat membuat backup: {str(e)}')
        
        return redirect('core:database_backup_list')
    
    # For GET request, show the form
    context = {
        'page_title': 'Buat Backup Database',
        'active_menu': 'database_reset',
        'active_submenu': 'database_backup_create',
    }
    return render(request, 'admin_panel/database_backup_create.html', context)


@login_required
def database_backup_download(request, backup_name):
    """
    Download backup file
    """
    backup_dir = os.path.join(settings.BASE_DIR, 'backups')
    backup_path = None
    
    # Find the backup file
    for root, dirs, files in os.walk(backup_dir):
        if backup_name in files:
            backup_path = os.path.join(root, backup_name)
            break
    
    if not backup_path or not os.path.exists(backup_path):
        messages.error(request, 'File backup tidak ditemukan!')
        return redirect('core:database_backup_list')
    
    # Create response
    with open(backup_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{backup_name}"'
        return response


@login_required
def database_backup_restore(request, backup_name):
    """
    Restore database from backup
    """
    if request.method == 'POST':
        backup_dir = os.path.join(settings.BASE_DIR, 'backups')
        backup_path = None
        
        # Find the backup file
        for root, dirs, files in os.walk(backup_dir):
            if backup_name in files:
                backup_path = os.path.join(root, backup_name)
                break
        
        if not backup_path or not os.path.exists(backup_path):
            messages.error(request, 'File backup tidak ditemukan!')
            return redirect('core:database_backup_list')
        
        try:
            # Execute restore command
            result = subprocess.run(
                ['python', 'manage.py', 'restore_database', '--file', backup_path, '--force'],
                capture_output=True,
                text=True,
                cwd=settings.BASE_DIR
            )
            
            if result.returncode == 0:
                messages.success(request, 'Database berhasil di-restore dari backup!')
            else:
                messages.error(request, f'Gagal restore: {result.stderr}')
                
        except Exception as e:
            messages.error(request, f'Error saat restore: {str(e)}')
        
        return redirect('core:database_backup_list')
    
    context = {
        'page_title': f'Restore dari Backup: {backup_name}',
        'backup_name': backup_name,
    }
    return render(request, 'admin_panel/database_backup_restore.html', context)


@login_required
def database_backup_delete(request, backup_name):
    """
    Delete database backup file
    """
    if request.method == 'POST':
        try:
            backup_dir = os.path.join(settings.BASE_DIR, 'backups')
            backup_path = None
            
            # Find the backup file
            for root, dirs, files in os.walk(backup_dir):
                if backup_name in files:
                    backup_path = os.path.join(root, backup_name)
                    break
            
            if not backup_path or not os.path.exists(backup_path):
                messages.error(request, 'File backup tidak ditemukan!')
                return redirect('core:database_backup_list')
            
            # Delete the file
            os.remove(backup_path)
            messages.success(request, f'Backup "{backup_name}" berhasil dihapus!')
                
        except Exception as e:
            messages.error(request, f'Error saat menghapus backup: {str(e)}')
    
    return redirect('core:database_backup_list')


@login_required
@csrf_exempt
def database_reset_ajax(request):
    """
    AJAX endpoint for database reset operations
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            action = data.get('action')
            
            if action == 'execute_reset':
                config_id = data.get('config_id')
                config = get_object_or_404(DatabaseResetConfig, id=config_id)
                
                # Update config status
                config.status = 'running'
                config.executed_by = request.user
                config.executed_at = timezone.now()
                config.save()
                
                # Execute reset command
                result = execute_reset_command(config)
                
                if result['success']:
                    config.status = 'completed'
                    config.completed_at = timezone.now()
                    config.execution_log = result['log']
                    config.records_deleted = result['records_deleted']
                else:
                    config.status = 'failed'
                    config.error_log = result['error']
                
                config.save()
                
                return JsonResponse({
                    'success': result['success'],
                    'message': 'Reset berhasil dieksekusi' if result['success'] else f'Reset gagal: {result["error"]}',
                    'status': config.status
                })
            
            elif action == 'get_status':
                config_id = data.get('config_id')
                config = get_object_or_404(DatabaseResetConfig, id=config_id)
                
                return JsonResponse({
                    'status': config.status,
                    'executed_at': config.executed_at.isoformat() if config.executed_at else None,
                    'completed_at': config.completed_at.isoformat() if config.completed_at else None,
                })
            
            elif action == 'delete_config':
                config_id = data.get('config_id')
                config = get_object_or_404(DatabaseResetConfig, id=config_id)
                
                # Check if config can be deleted (only pending configs)
                if config.status == 'running':
                    return JsonResponse({
                        'success': False, 
                        'message': 'Tidak dapat menghapus konfigurasi yang sedang berjalan'
                    })
                
                # Delete the config
                config_name = config.name
                config.delete()
                
                return JsonResponse({
                    'success': True,
                    'message': f'Konfigurasi "{config_name}" berhasil dihapus'
                })
            
            elif action == 'quick_reset':
                # Handle quick reset from modal
                form_data = data.get('data', {})
                
                # Create new config
                config = DatabaseResetConfig(
                    name=form_data.get('name', f'Quick Reset - {timezone.now().strftime("%Y-%m-%d %H:%M")}'),
                    reset_type=form_data.get('reset_type', 'selective'),
                    reset_penduduk=form_data.get('reset_penduduk') == 'on',
                    reset_dusun=form_data.get('reset_dusun') == 'on',
                    reset_lorong=form_data.get('reset_lorong') == 'on',
                    reset_rt_rw=form_data.get('reset_rt_rw') == 'on',
                    reset_keluarga=form_data.get('reset_keluarga') == 'on',
                    reset_pelajar=form_data.get('reset_pelajar') == 'on',
                    reset_disabilitas=form_data.get('reset_disabilitas') == 'on',
                    reset_beneficiaries=form_data.get('reset_beneficiaries') == 'on',
                    reset_business=form_data.get('reset_business') == 'on',
                    reset_complaints=form_data.get('reset_complaints') == 'on',
                    reset_documents=form_data.get('reset_documents') == 'on',
                    reset_tourism=form_data.get('reset_tourism') == 'on',
                    reset_posyandu=form_data.get('reset_posyandu') == 'on',
                    reset_news=form_data.get('reset_news') == 'on',
                    reset_organization=form_data.get('reset_organization') == 'on',
                    reset_layanan=form_data.get('reset_layanan') == 'on',
                    reset_letters=form_data.get('reset_letters') == 'on',
                    backup_before_reset=form_data.get('backup_before_reset') == 'on',
                    keep_users=form_data.get('keep_users') == 'on',
                    keep_settings=form_data.get('keep_settings') == 'on',
                    keep_media=form_data.get('keep_media') == 'on',
                    created_by=request.user,
                    status='running'
                )
                config.save()
                
                # Execute reset command
                result = execute_reset_command(config)
                
                if result['success']:
                    config.status = 'completed'
                    config.completed_at = timezone.now()
                    config.execution_log = result['log']
                    config.records_deleted = result['records_deleted']
                else:
                    config.status = 'failed'
                    config.error_log = result['error']
                
                config.save()
                
                return JsonResponse({
                    'success': result['success'],
                    'message': 'Quick reset berhasil dieksekusi' if result['success'] else f'Quick reset gagal: {result["error"]}',
                    'config_id': config.id
                })
            
            else:
                return JsonResponse({'success': False, 'message': 'Action tidak valid'})
                
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    return JsonResponse({'success': False, 'message': 'Method tidak diizinkan'})
