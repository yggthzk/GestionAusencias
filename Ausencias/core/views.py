from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import SolicitudAusencia
from django.utils import timezone
from datetime import datetime
from django.core.validators import validate_email#validadores de campos
from django.core.exceptions import ValidationError

def es_admin(user):
    return user.is_superuser

@login_required
def dashboard(request):
    if request.user.is_superuser:
        return redirect('panel_admin')
    
    solicitudes = SolicitudAusencia.objects.filter(usuario=request.user).order_by('-fecha_solicitud')
    dias_totales = 4
    
    dias_tomados = 0
    for sol in solicitudes:
        if sol.estado == 'aprobada' and sol.fecha_inicio and sol.fecha_fin:
            delta = sol.fecha_fin - sol.fecha_inicio
            dias_tomados += delta.days + 1
            
    dias_disponibles = dias_totales - dias_tomados
    
    context = {
        'solicitudes': solicitudes,
        'dias_disponibles': dias_disponibles,
        'dias_tomados': dias_tomados,
        'dias_totales': dias_totales
    }
    return render(request, 'core/menu.html', context)

@login_required
def crear_solicitud(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre_completo')
        correo = request.POST.get('correo_contacto')        
        emergencia = request.POST.get('contacto_emergencia')
        tipo = request.POST.get('tipo')
        fecha_inicio_str = request.POST.get('fecha_inicio')
        fecha_fin_str = request.POST.get('fecha_fin')
        motivo = request.POST.get('motivo')
        url_doc = request.POST.get('url_justificativo')
        if not nombre or not fecha_inicio_str or not fecha_fin_str or not motivo or not correo or not emergencia:
            messages.error(request, 'Error: Todos los campos obligatorios deben llenarse, incluyendo contactos.')
            return render(request, 'core/crudsolicitudes.html')

        # Manejo de Excepcione
        try:
            validate_email(correo)
        except ValidationError:
            messages.error(request, 'Error: El formato del correo de contacto no es válido.')
            return render(request, 'core/crudsolicitudes.html')

        # Logica de fechas y campos seleccionables
        try:
            fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date()
            fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, 'Error: Formato de fecha inválido.')
            return render(request, 'core/crudsolicitudes.html')

        if fecha_fin < fecha_inicio:
            messages.error(request, 'Error: La fecha de término no puede ser anterior a la de inicio.')
            return render(request, 'core/crudsolicitudes.html')
            
        dias_solicitados = (fecha_fin - fecha_inicio).days + 1
        
        # Logica de Ausencia de los dias.
        solicitudes_aprobadas = SolicitudAusencia.objects.filter(usuario=request.user, estado='aprobada')
        dias_usados = 0
        for sol in solicitudes_aprobadas:
            if sol.fecha_inicio and sol.fecha_fin:
                delta = sol.fecha_fin - sol.fecha_inicio
                dias_usados += delta.days + 1
        
        if (dias_usados + dias_solicitados) > 4:
             messages.error(request, f'Error: Excede el límite. Días solicitados: {dias_solicitados}. Disponibles: {4 - dias_usados}.')
             return render(request, 'core/crudsolicitudes.html')
        try:
            SolicitudAusencia.objects.create(
                usuario=request.user,
                nombre_completo=nombre,
                correo_contacto=correo,       
                contacto_emergencia=emergencia,  # CAMPOS DE CONTACTO DE EMERGENCIA
                tipo_ausencia=tipo,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                motivo_detallado=motivo,
                url_justificativo=url_doc,
                codigo_empleado=f"EMP-{request.user.id}",
                estado='pendiente'
            )
            messages.success(request, 'Solicitud enviada correctamente.')
            return redirect('dashboard')
        except Exception as e:
            # Capturamos cualquier error de base de datos
            messages.error(request, f'Ocurrió un error interno al guardar la solicitud: {str(e)}')
            
    return render(request, 'core/crudsolicitudes.html')

@login_required
@user_passes_test(es_admin)
def panel_admin(request):
    solicitudes_pendientes = SolicitudAusencia.objects.filter(estado='pendiente').order_by('fecha_solicitud')
    return render(request, 'core/panel_admin.html', {'solicitudes': solicitudes_pendientes})

@login_required
@user_passes_test(es_admin)
def gestionar_solicitud(request, solicitud_id, accion):
    solicitud = get_object_or_404(SolicitudAusencia, id=solicitud_id)
    if accion == 'aprobar':
        dias_solicitud = (solicitud.fecha_fin - solicitud.fecha_inicio).days + 1
        
        solicitudes_aprobadas = SolicitudAusencia.objects.filter(usuario=solicitud.usuario, estado='aprobada')
        dias_usados = sum([(s.fecha_fin - s.fecha_inicio).days + 1 for s in solicitudes_aprobadas])
        
        if (dias_usados + dias_solicitud) > 4:
            messages.error(request, f'No se puede aprobar. El empleado excedería su límite de 4 días.')
            return redirect('panel_admin')

        solicitud.estado = 'aprobada'
        messages.success(request, f'Solicitud de {solicitud.nombre_completo} Aprobada.')
        
    elif accion == 'rechazar':
        solicitud.estado = 'rechazada'
        messages.warning(request, f'Solicitud de {solicitud.nombre_completo} Rechazada.')
    solicitud.save()
    return redirect('panel_admin')