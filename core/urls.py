# core/urls.py
from rest_framework import routers
from django.urls import path, include
from .views import *

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = routers.DefaultRouter()

# Usuarios
router.register(r'usuarios', UsuarioViewSet)
#router.register(r'usuarios', UsuarioViewSet, basename='usuario')  # más explícito

router.register(r'administradores', AdministradorViewSet)
router.register(r'profesores', ProfesorViewSet)
router.register(r'alumnos', AlumnoViewSet)
router.register(r'apoderados', ApoderadoViewSet)

# Relaciones
router.register(r'alumno-apoderado', AlumnoApoderadoViewSet)

# Gestión académica
router.register(r'gestiones', GestionViewSet)
router.register(r'periodos', PeriodoViewSet)
router.register(r'gestion-periodo', GestionPeriodoViewSet)
router.register(r'grados', GradoViewSet)
router.register(r'gestion-grado', GestionGradoViewSet)
router.register(r'gestion-grado-materia', GestionGradoMateriaViewSet)

# Académico
router.register(r'materias', MateriaViewSet)
router.register(r'aulas', AulaViewSet)
router.register(r'horarios', HorarioViewSet)
router.register(r'inscripciones', InscripcionViewSet)

# Evaluaciones
router.register(r'notas', NotaViewSet)
router.register(r'asistencias', AsistenciaViewSet)
router.register(r'participaciones', ParticipacionViewSet)
router.register(r'predicciones', PrediccionViewSet)


urlpatterns = [
    path('', include(router.urls)),
    # JWT login
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Registro y perfil
    path('register/', RegistroUsuarioView.as_view(), name='registro_usuario'),
    path('auth/me/', usuario_actual, name='usuario-actual'),

    #Horario de Alumno
    path('mi-horario/', HorarioAlumnoView.as_view(), name='mi-horario'),

    path('prediccion-rendimiento/', PrediccionRendimientoAPIView.as_view(), name='prediccion-rendimiento'),
]
