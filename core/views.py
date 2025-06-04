#from django.shortcuts import render

# core/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, action
from django.contrib.auth import get_user_model

from .models import *
from .serializers import *

from core.utils.ml.ml_model import predecir_rendimiento

from django.db.models.functions import Concat
from django.db.models import F, Value, Q, Avg, Count
from rest_framework.pagination import PageNumberPagination

from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import joblib
import os
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta
from collections import defaultdict

Usuario = get_user_model()

# Usuario actual //me
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def usuario_actual(request):
    usuario = request.user
    serializer = UsuarioSerializer(usuario)
    return Response(serializer.data)

class CustomPagination(PageNumberPagination):
    page_size = 7

# Registro
class RegistroUsuarioView(generics.CreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = RegistroUsuarioSerializer
    permission_classes = [IsAuthenticated]

#Usuarios
"""class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]"""

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        rol_param = self.request.query_params.get('rol')
        nombre_param = self.request.query_params.get('nombre')

        queryset = Usuario.objects.annotate(
            nombre_completo=Concat(F('first_name'), Value(' '), F('last_name'))
        )

        if rol_param:
            return queryset.filter(rol__iexact=rol_param).order_by('-nombre_completo')

        elif nombre_param:
            return queryset.filter(
                Q(first_name__icontains=nombre_param) |
                Q(last_name__icontains=nombre_param)
            ).order_by('-nombre_completo')

        else:
            return queryset.order_by('-id')


# Usuarios relacionados
class AlumnoViewSet(viewsets.ModelViewSet):
    queryset = Alumno.objects.all()
    serializer_class = AlumnoSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        nombre_param = self.request.query_params.get('nombre')

        queryset = Alumno.objects.annotate(
            nombre_completo=Concat(F('usuario__first_name'), Value(' '), F('usuario__last_name'))
        )

        if nombre_param:
            return queryset.filter(
                Q(first_name__icontains=nombre_param) |
                Q(last_name__icontains=nombre_param)
            ).order_by('-nombre_completo')
        return queryset.order_by('-usuario__id')

class ProfesorViewSet(viewsets.ModelViewSet):
    queryset = Profesor.objects.all()
    serializer_class = ProfesorSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        nombre_param = self.request.query_params.get('nombre')

        queryset = Profesor.objects.annotate(
            nombre_completo=Concat(F('usuario__first_name'), Value(' '), F('usuario__last_name'))
        )

        if nombre_param:
            return queryset.filter(
                Q(first_name__icontains=nombre_param) |
                Q(last_name__icontains=nombre_param)
            ).order_by('-nombre_completo')
        return queryset.order_by('-usuario__id')

class ApoderadoViewSet(viewsets.ModelViewSet):
    queryset = Apoderado.objects.all()
    serializer_class = ApoderadoSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        nombre_param = self.request.query_params.get('nombre')

        queryset = Apoderado.objects.annotate(
            nombre_completo=Concat(F('usuario__first_name'), Value(' '), F('usuario__last_name'))
        )

        if nombre_param:
            return queryset.filter(
                Q(first_name__icontains=nombre_param) |
                Q(last_name__icontains=nombre_param)
            ).order_by('-nombre_completo')
        return queryset.order_by('-usuario__id')

class AdministradorViewSet(viewsets.ModelViewSet):
    queryset = Administrador.objects.all()
    serializer_class = AdministradorSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        nombre_param = self.request.query_params.get('nombre')

        queryset = Administrador.objects.annotate(
            nombre_completo=Concat(F('usuario__first_name'), Value(' '), F('usuario__last_name'))
        )

        if nombre_param:
            return queryset.filter(
                Q(first_name__icontains=nombre_param) |
                Q(last_name__icontains=nombre_param)
            ).order_by('-nombre_completo')
        return queryset.order_by('-usuario__id')

# Relaciones
class AlumnoApoderadoViewSet(viewsets.ModelViewSet):
    queryset = AlumnoApoderado.objects.all()
    serializer_class = AlumnoApoderadoSerializer
    permission_classes = [IsAuthenticated]

# Gestión académica
class GestionViewSet(viewsets.ModelViewSet):
    queryset = Gestion.objects.all()
    serializer_class = GestionSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        nombre_param = self.request.query_params.get('nombre')
        queryset = Gestion.objects.all()

        if nombre_param:
            queryset = queryset.filter(
                Q(nombre__icontains=nombre_param)
            )

        return queryset.order_by('-id')

class PeriodoViewSet(viewsets.ModelViewSet):
    queryset = Periodo.objects.all()
    serializer_class = PeriodoSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        nombre_param = self.request.query_params.get('nombre')
        queryset = Periodo.objects.all()

        if nombre_param:
            queryset = queryset.filter(
                Q(nombre__icontains=nombre_param)
            )

        return queryset.order_by('-id')

class GestionPeriodoViewSet(viewsets.ModelViewSet):
    queryset = GestionPeriodo.objects.all()
    serializer_class = GestionPeriodoSerializer
    permission_classes = [IsAuthenticated]

class GradoViewSet(viewsets.ModelViewSet):
    queryset = Grado.objects.all()
    serializer_class = GradoSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        nombre_param = self.request.query_params.get('nombre')
        queryset = Grado.objects.all()

        if nombre_param:
            queryset = queryset.filter(
                Q(nombre__icontains=nombre_param)
            )

        return queryset.order_by('-id')

class GestionGradoViewSet(viewsets.ModelViewSet):
    queryset = GestionGrado.objects.all()
    serializer_class = GestionGradoSerializer
    permission_classes = [IsAuthenticated]

class GestionGradoMateriaViewSet(viewsets.ModelViewSet):
    queryset = GestionGradoMateria.objects.all()
    serializer_class = GestionGradoMateriaSerializer
    permission_classes = [IsAuthenticated]

# Academico
class MateriaViewSet(viewsets.ModelViewSet):
    queryset = Materia.objects.all()
    serializer_class = MateriaSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        nombre_param = self.request.query_params.get('nombre')
        queryset = Materia.objects.all()

        if nombre_param:
            queryset = queryset.filter(
                Q(nombre__icontains=nombre_param)
            )

        return queryset.order_by('-id')

class AulaViewSet(viewsets.ModelViewSet):
    queryset = Aula.objects.all()
    serializer_class = AulaSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        codigo_param = self.request.query_params.get('codigo')
        queryset = Aula.objects.all()

        if codigo_param:
            queryset = queryset.filter(
                Q(codigo__icontains=codigo_param)
            )

        return queryset.order_by('-id')

class HorarioViewSet(viewsets.ModelViewSet):
    queryset = Horario.objects.all()
    serializer_class = HorarioSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        try:
            alumno = Alumno.objects.get(usuario=user)
            inscripcion = Inscripcion.objects.filter(
                alumno=alumno,
                gestiongrado__gestion__estado='EN CURSO'
            ).first()
            if not inscripcion:
                return Horario.objects.none()
            
            return Horario.objects.filter(
                gestiongradomateria__gestiongrado=inscripcion.gestiongrado
            ).select_related(
                'aula',
                'gestiongradomateria__materia',
                'profesor__usuario'
            )
        except Alumno.DoesNotExist:
            return Horario.objects.none()

class HorarioAlumnoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        try:
            alumno = Alumno.objects.get(usuario=user)
        except Alumno.DoesNotExist:
            return Response({"detail": "Usuario no es alumno."}, status=400)

        inscripcion = Inscripcion.objects.filter(
            alumno=alumno,
            gestiongrado__gestion__estado='EN CURSO'
        ).select_related('gestiongrado').first()

        if not inscripcion:
            return Response({"detail": "No tiene inscripción activa."}, status=404)

        horarios = Horario.objects.filter(
            gestiongradomateria__gestiongrado=inscripcion.gestiongrado
        ).select_related(
            'aula',
            'gestiongradomateria__materia',
            'profesor__usuario'
        ).order_by('dia', 'hora_inicio')

        serializer = HorarioAlumnoSerializer(horarios, many=True)
        return Response(serializer.data)

class InscripcionViewSet(viewsets.ModelViewSet):
    queryset = Inscripcion.objects.all()
    serializer_class = InscripcionSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user

        try:
            alumno = Alumno.objects.get(usuario=user)
        except Alumno.DoesNotExist:
            return Inscripcion.objects.none()  # O puedes lanzar un error 403/404

        gestion_estado = self.request.query_params.get('gestion_estado', 'EN CURSO')
        return Inscripcion.objects.filter(
            alumno=alumno,
            gestiongrado__gestion__estado=gestion_estado
        ).prefetch_related('gestiongrado__gestiongradomateria_set__materia')

# Evaluaciones
class NotaViewSet(viewsets.ModelViewSet):
    queryset = Nota.objects.all()
    serializer_class = NotaSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['GET'])
    def progreso_academico(self, request):
        # Validar que el usuario es un ALUMNO
        if request.user.rol != 'ALUMNO':
            return Response({"error": "Acceso no autorizado"}, status=403)

        # Obtener el alumno y su inscripción activa
        try:
            alumno = Alumno.objects.get(usuario=request.user)
            inscripcion = Inscripcion.objects.filter(
                alumno=alumno,
                gestiongrado__gestion__estado='EN CURSO'
            ).first()
            if not inscripcion:
                return Response({"error": "No tienes una inscripción activa"}, status=400)
        except Alumno.DoesNotExist:
            return Response({"error": "Alumno no encontrado"}, status=404)

        # Obtener notas agrupadas por materia y período
        notas = Nota.objects.filter(
            inscripcion=inscripcion
        ).values(
            'materia__nombre',
            'gestionperiodo__periodo__nombre'
        ).annotate(
            promedio=Avg('valor'),
            cantidad=Count('id')
        ).order_by('materia__nombre')

        # Calcular promedio general por período
        promedios_periodo = defaultdict(list)
        for nota in notas:
            promedios_periodo[nota['gestionperiodo__periodo__nombre']].append(nota['promedio'])

        promedios_finales = {
            periodo: sum(valores) / len(valores)
            for periodo, valores in promedios_periodo.items()
        }

        return Response({
            "notas_por_materia": list(notas),
            "promedios_generales": promedios_finales,
        })
    
    @action(detail=False, methods=['GET'])
    def notas_por_periodo(self, request):
        # Validar que el usuario es un ALUMNO
        if request.user.rol != 'ALUMNO':
            return Response({"error": "Acceso no autorizado"}, status=403)

        # Obtener el alumno y su inscripción activa
        try:
            alumno = Alumno.objects.get(usuario=request.user)
            inscripcion = Inscripcion.objects.filter(
                alumno=alumno,
                gestiongrado__gestion__estado='EN CURSO'
            ).first()
            if not inscripcion:
                return Response({"error": "No tienes una inscripción activa"}, status=400)
        except Alumno.DoesNotExist:
            return Response({"error": "Alumno no encontrado"}, status=404)

        # Filtrar notas por período (query param opcional: ?periodo=Primer Trimestre)
        periodo = request.query_params.get('periodo')
        queryset = Nota.objects.filter(inscripcion=inscripcion)

        if periodo:
            queryset = queryset.filter(gestionperiodo__periodo__nombre=periodo)

        # Agrupar por materia y período
        notas_agrupadas = queryset.values(
            'materia__nombre',
            'gestionperiodo__periodo__nombre'
        ).annotate(
            promedio=Avg('valor'),
            cantidad=Count('id')
        ).order_by('materia__nombre')

        return Response({
            "notas": list(notas_agrupadas),
            "periodos_disponibles": ["Primer Trimestre", "Segundo Trimestre", "Tercer Trimestre"]
        })

class AsistenciaViewSet(viewsets.ModelViewSet):
    queryset = Asistencia.objects.all()
    serializer_class = AsistenciaSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['POST'])
    def registrar_asistencia_alumno(self, request):
        # Validar que el usuario es un ALUMNO
        if request.user.rol != 'ALUMNO':
            return Response({"error": "Solo los alumnos pueden registrar su propia asistencia"}, status=403)

        # Obtener la inscripción del alumno en la gestión "EN CURSO"
        try:
            alumno = Alumno.objects.get(usuario=request.user)
            inscripcion = Inscripcion.objects.filter(
                alumno=alumno,
                gestiongrado__gestion__estado='EN CURSO'
            ).first()
            if not inscripcion:
                return Response({"error": "No tienes una inscripción activa"}, status=400)
        except Alumno.DoesNotExist:
            return Response({"error": "Alumno no encontrado"}, status=404)

        # Validar que no exista ya un registro de asistencia para hoy
        hoy = timezone.now().date()
        if Asistencia.objects.filter(inscripcion=inscripcion, fecha=hoy).exists():
            return Response({"error": "Ya registraste tu asistencia hoy"}, status=400)

        # Crear registro de asistencia automático (siempre "PRESENTE")
        asistencia = Asistencia.objects.create(
            inscripcion=inscripcion,
            fecha=hoy,
            estado='PRESENTE',  # El alumno no puede cambiar su estado
            justificacion=request.data.get('justificacion', '')
        )

        return Response({
            "id": asistencia.id,
            "fecha": asistencia.fecha,
            "estado": asistencia.estado,
            "mensaje": "Asistencia registrada exitosamente"
        }, status=201)
    
    @action(detail=False, methods=['GET'])
    def historial_alumno(self, request):
        # Validar que el usuario es un ALUMNO
        if request.user.rol != 'ALUMNO':
            return Response({"error": "Acceso no autorizado"}, status=403)

        # Obtener el alumno autenticado y su inscripción activa
        try:
            alumno = Alumno.objects.get(usuario=request.user)
            inscripcion = Inscripcion.objects.filter(
                alumno=alumno,
                gestiongrado__gestion__estado='EN CURSO'
            ).first()
            if not inscripcion:
                return Response({"error": "No tienes una inscripción activa"}, status=400)
        except Alumno.DoesNotExist:
            return Response({"error": "Alumno no encontrado"}, status=404)

        # Filtrar asistencias (opcional: rango de fechas)
        fecha_inicio = request.query_params.get('fecha_inicio')
        fecha_fin = request.query_params.get('fecha_fin')

        queryset = Asistencia.objects.filter(inscripcion=inscripcion).order_by('-fecha')

        if fecha_inicio and fecha_fin:
            queryset = queryset.filter(fecha__range=[fecha_inicio, fecha_fin])

        # Serializar datos
        serializer = AsistenciaSerializer(queryset, many=True)
        return Response(serializer.data)

class ParticipacionViewSet(viewsets.ModelViewSet):
    queryset = Participacion.objects.all()
    serializer_class = ParticipacionSerializer
    permission_classes = [IsAuthenticated]

"""class PrediccionViewSet(viewsets.ModelViewSet):
    queryset = PrediccionRendimiento.objects.all()
    serializer_class = PrediccionRendimientoSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        valor_prediccion_param = self.request.query_params.get('valor_prediccion')
        queryset = PrediccionRendimiento.objects.all()

        if valor_prediccion_param:
            queryset = queryset.filter(
                Q(valor_prediccion__icontains=valor_prediccion_param)
            )

        return queryset.order_by('-id')"""

class PrediccionViewSet(viewsets.ModelViewSet):
    queryset = PrediccionRendimiento.objects.all()
    serializer_class = PrediccionRendimientoSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['POST'])
    def generar_prediccion(self, request):
        # 1. Obtener datos del alumno
        alumno_id = request.data.get('alumno_id')
        inscripcion = Inscripcion.objects.filter(alumno_id=alumno_id).first()
        
        if not inscripcion:
            return Response({"error": "Alumno no encontrado"}, status=404)

        # 2. Obtener datos para el modelo (notas, asistencia, participación)
        notas = Nota.objects.filter(inscripcion=inscripcion).aggregate(promedio=Avg('valor'))
        
        total_asistencias = Asistencia.objects.filter(inscripcion=inscripcion).count()
        asistencias_presentes = Asistencia.objects.filter(inscripcion=inscripcion, estado='PRESENTE').count()
        porcentaje_asistencia = (asistencias_presentes / total_asistencias * 100) if total_asistencias else 0

        participacion = Participacion.objects.filter(inscripcion=inscripcion).aggregate(promedio=Avg('valoracion'))

        # 3. Cargar modelo entrenado (o entrenar en tiempo real)
        modelo_path = 'modelo_rendimiento.pkl'
        if os.path.exists(modelo_path):
            modelo = joblib.load(modelo_path)
        else:
            modelo = self.entrenar_modelo()
            joblib.dump(modelo, modelo_path)

        # 4. Predecir
        datos_alumno = pd.DataFrame([[
            notas['promedio'] or 0,
            porcentaje_asistencia,
            participacion['promedio'] or 0
        ]], columns=['notas', 'asistencia', 'participacion'])

        prediccion = modelo.predict(datos_alumno)[0]
        categoria = "BAJO" if prediccion < 40 else "MEDIO" if prediccion < 70 else "ALTO"

        # Conversión explícita para evitar error con DecimalField
        valor_prediccion = Decimal(int(prediccion))  # si `valor_prediccion` es DecimalField
        # o solo:
        # valor_prediccion = int(prediccion)  # si es IntegerField

        # 5. Guardar predicción en la base de datos
        prediccion_obj = PrediccionRendimiento.objects.create(
            inscripcion=inscripcion,
            valor_prediccion=valor_prediccion,
            categoria_rendimiento=categoria,
            modelo_utilizado="RandomForest"
        )

        return Response({
            "valor_prediccion": prediccion,
            "categoria": categoria
        })

    def entrenar_modelo(self):
        # Simulación: Entrenar modelo con datos históricos (ajusta según tu dataset)
        from sklearn.datasets import make_classification
        #from sklearn.ensemble import RandomForestClassifier
        #import joblib

        # Simulación de entrenamiento de modelo
        X, y = make_classification(
            n_samples=100,
            n_features=3,
            n_informative=2,
            n_redundant=0,
            n_repeated=0,
            random_state=42
        )

        #X, y = make_classification(n_samples=100, n_features=3)
        modelo = RandomForestClassifier()
        modelo.fit(X, y)

        # Guarda el modelo entrenado
        joblib.dump(modelo, 'modelo_rendimiento.pkl')
        return modelo

class PrediccionRendimientoAPIView(APIView):
    def post(self, request):
        data = request.data

        try:
            promedio_notas = float(data.get("promedio_notas"))
            asistencia = float(data.get("asistencia"))
            participacion = float(data.get("participacion"))
        except (TypeError, ValueError):
            return Response({"error": "Datos inválidos."}, status=status.HTTP_400_BAD_REQUEST)

        prediccion, clasificacion = predecir_rendimiento(promedio_notas, asistencia, participacion)

        return Response({
            "prediccion": round(prediccion, 2),
            "clasificacion": clasificacion
        }, status=status.HTTP_200_OK)
