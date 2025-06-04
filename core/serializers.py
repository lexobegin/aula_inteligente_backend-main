# core/serializers.py
from rest_framework import serializers
from .models import *

from django.contrib.auth import get_user_model

Usuario = get_user_model()


# Usuario (para login, perfil, etc.)
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'rol', 'estado', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = Usuario(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

class RegistroUsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'password', 'rol']  # o los campos que usas

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = Usuario(**validated_data)
        user.set_password(password)
        user.save()
        return user

# Administrador
class AdministradorSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer()

    class Meta:
        model = Administrador
        fields = ['usuario', 'telefono']

    def create(self, validated_data):
        usuario_data = validated_data.pop('usuario')
        usuario_data['rol'] = 'ADMINISTRADOR'
        usuario = UsuarioSerializer().create(usuario_data)
        return Administrador.objects.create(usuario=usuario, **validated_data)

    def update(self, instance, validated_data):
        usuario_data = validated_data.pop('usuario', None)
        if usuario_data:
            UsuarioSerializer().update(instance.usuario, usuario_data)
        instance.telefono = validated_data.get('telefono', instance.telefono)
        instance.save()
        return instance

# Profesor
class ProfesorSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer()

    class Meta:
        model = Profesor
        fields = ['usuario', 'especialidad', 'titulo', 'fecha_contratacion']

    def create(self, validated_data):
        usuario_data = validated_data.pop('usuario')
        usuario_data['rol'] = 'PROFESOR'
        usuario = UsuarioSerializer().create(usuario_data)
        return Profesor.objects.create(usuario=usuario, **validated_data)

    def update(self, instance, validated_data):
        usuario_data = validated_data.pop('usuario', None)
        if usuario_data:
            UsuarioSerializer().update(instance.usuario, usuario_data)
        for attr in ['especialidad', 'titulo', 'fecha_contratacion']:
            if attr in validated_data:
                setattr(instance, attr, validated_data[attr])
        instance.save()
        return instance

# Alumno
class AlumnoSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer()

    class Meta:
        model = Alumno
        fields = ['usuario', 'fecha_nacimiento', 'genero', 'direccion', 'telefono_emergencia']

    def create(self, validated_data):
        usuario_data = validated_data.pop('usuario')
        usuario_data['rol'] = 'ALUMNO'
        usuario = UsuarioSerializer().create(usuario_data)
        return Alumno.objects.create(usuario=usuario, **validated_data)

    def update(self, instance, validated_data):
        usuario_data = validated_data.pop('usuario', None)
        if usuario_data:
            UsuarioSerializer().update(instance.usuario, usuario_data)
        for attr in ['fecha_nacimiento', 'genero', 'direccion', 'telefono_emergencia']:
            if attr in validated_data:
                setattr(instance, attr, validated_data[attr])
        instance.save()
        return instance

# Apoderado
class ApoderadoSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer()

    class Meta:
        model = Apoderado
        fields = ['usuario', 'parentesco', 'ocupacion', 'direccion_trabajo', 'telefono']

    def create(self, validated_data):
        usuario_data = validated_data.pop('usuario')
        usuario_data['rol'] = 'APODERADO'
        usuario = UsuarioSerializer().create(usuario_data)
        return Apoderado.objects.create(usuario=usuario, **validated_data)

    def update(self, instance, validated_data):
        usuario_data = validated_data.pop('usuario', None)
        if usuario_data:
            UsuarioSerializer().update(instance.usuario, usuario_data)
        for attr in ['parentesco', 'ocupacion', 'direccion_trabajo', 'telefono']:
            if attr in validated_data:
                setattr(instance, attr, validated_data[attr])
        instance.save()
        return instance

# Horario
class HorarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Horario
        fields = '__all__'

class HorarioAlumnoSerializer(serializers.ModelSerializer):
    materia = serializers.CharField(source='gestiongradomateria.materia.nombre')
    aula = serializers.SerializerMethodField()
    profesor = serializers.SerializerMethodField()
    dia = serializers.CharField()
    hora_inicio = serializers.TimeField(format='%H:%M')
    hora_fin = serializers.TimeField(format='%H:%M')

    class Meta:
        model = Horario
        fields = ['materia', 'dia', 'hora_inicio', 'hora_fin', 'aula', 'profesor']

    def get_aula(self, obj):
        return f"{obj.aula.codigo} - Piso {obj.aula.piso} ({obj.aula.edificio})"

    def get_profesor(self, obj):
        return obj.profesor.usuario.get_full_name()

# Inscripción
class InscripcionSerializer(serializers.ModelSerializer):
    materias = serializers.SerializerMethodField()

    class Meta:
        model = Inscripcion
        fields = ['id', 'fecha_inscripcion', 'estado', 'alumno', 'gestiongrado', 'materias']

    def get_materias(self, obj):
        materias = Materia.objects.filter(
            gestiongradomateria__gestiongrado=obj.gestiongrado
        ).distinct()
        return [
            {
                "id": materia.id,
                "nombre": materia.nombre,
                "nivel": materia.nivel,
                "descripcion": materia.descripcion
            }
            for materia in materias
        ]

# Nota
class NotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nota
        fields = '__all__'

# Asistencia
class AsistenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asistencia
        fields = '__all__'

# Participación
class ParticipacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participacion
        fields = '__all__'

# Predicción de rendimiento
class PrediccionRendimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrediccionRendimiento
        fields = '__all__'

# Gestion Academica
class GestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gestion
        fields = '__all__'

# Periodo Academico
class PeriodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Periodo
        fields = '__all__'

# Materia
class MateriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Materia
        fields = '__all__'

# Aula
class AulaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aula
        fields = '__all__'

# AlumnoApoderado
class AlumnoApoderadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlumnoApoderado
        fields = '__all__'

# GestionPeriodo
"""class GestionPeriodoSerializer(serializers.ModelSerializer):
    gestion = serializers.StringRelatedField()
    periodo = serializers.StringRelatedField()

    class Meta:
        model = GestionPeriodo
        fields = ['id', 'gestion', 'periodo', 'fechaini_periodo', 'fechafin_periodo']
"""
class GestionPeriodoSerializer(serializers.ModelSerializer):
    gestion = serializers.PrimaryKeyRelatedField(queryset=Gestion.objects.all())
    periodo = serializers.PrimaryKeyRelatedField(queryset=Periodo.objects.all())

    class Meta:
        model = GestionPeriodo
        fields = '__all__'

# Grado
"""class GradoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grado
        fields = ['id', 'nombre', 'estado']
"""

class GradoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grado
        fields = '__all__'

# GestionGrado
"""class GestionGradoSerializer(serializers.ModelSerializer):
    gestion = serializers.StringRelatedField()
    grado = serializers.StringRelatedField()

    class Meta:
        model = GestionGrado
        fields = ['id', 'gestion', 'grado']
"""
class GestionGradoSerializer(serializers.ModelSerializer):
    gestion = serializers.PrimaryKeyRelatedField(queryset=Gestion.objects.all())
    grado = serializers.PrimaryKeyRelatedField(queryset=Grado.objects.all())

    class Meta:
        model = GestionGrado
        fields = '__all__'

# GestionGradoMateria
"""class GestionGradoMateriaSerializer(serializers.ModelSerializer):
    gestiongrado = serializers.StringRelatedField()
    materia = serializers.StringRelatedField()

    class Meta:
        model = GestionGradoMateria
        fields = ['id', 'gestiongrado', 'materia']
"""

class GestionGradoMateriaSerializer(serializers.ModelSerializer):
    gestiongrado = serializers.PrimaryKeyRelatedField(queryset=GestionGrado.objects.all())
    materia = serializers.PrimaryKeyRelatedField(queryset=Materia.objects.all())

    class Meta:
        model = GestionGradoMateria
        fields = '__all__'
