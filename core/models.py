"""from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    estado = models.CharField(max_length=20, default='ACTIVO')

    ROL_CHOICES = [
        ('ADMINISTRADOR', 'Administrador'),
        ('PROFESOR', 'Profesor'),
        ('ALUMNO', 'Alumno'),
        ('APODERADO', 'Apoderado'),
    ]
    rol = models.CharField(max_length=30, choices=ROL_CHOICES, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.username} ({self.rol})"
    
class Administrador(models.Model):
    usuario = models.OneToOneField('Usuario', on_delete=models.CASCADE, primary_key=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)

class Profesor(models.Model):
    usuario = models.OneToOneField('Usuario', on_delete=models.CASCADE, primary_key=True)
    especialidad = models.CharField(max_length=100)
    titulo = models.CharField(max_length=100)
    fecha_contratacion = models.DateField()

class Alumno(models.Model):
    usuario = models.OneToOneField('Usuario', on_delete=models.CASCADE, primary_key=True)
    fecha_nacimiento = models.DateField()
    genero = models.CharField(max_length=1, choices=[('M', 'Masculino'), ('F', 'Femenino')])
    direccion = models.TextField()
    telefono_emergencia = models.CharField(max_length=20, null=True, blank=True)

class Apoderado(models.Model):
    usuario = models.OneToOneField('Usuario', on_delete=models.CASCADE, primary_key=True)
    parentesco = models.CharField(max_length=50)
    ocupacion = models.CharField(max_length=100)
    genero = models.CharField(max_length=1, choices=[('M', 'Masculino'), ('F', 'Femenino')])
    direccion_trabajo = models.TextField()
    telefono = models.CharField(max_length=20)

class AlumnoApoderado(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    apoderado = models.ForeignKey(Apoderado, on_delete=models.CASCADE)
    parentesco = models.CharField(max_length=50)
    es_principal = models.BooleanField(default=False)

    class Meta:
        constraints = [
        models.UniqueConstraint(fields=['alumno', 'apoderado'], name='unique_alumno_apoderado')
    ]

class GestionAcademica(models.Model):
    nombre = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    estado = models.CharField(max_length=20, default='PLANIFICADA')

    def __str__(self):
        return self.nombre

class PeriodoAcademico(models.Model):
    gestion = models.ForeignKey(GestionAcademica, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    tipo = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nombre} ({self.tipo})"

class Materia(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    creditos = models.IntegerField()
    nivel = models.CharField(max_length=50)

class Aula(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    edificio = models.CharField(max_length=50)
    piso = models.IntegerField()
    capacidad = models.IntegerField()
    tipo = models.CharField(max_length=50)
    equipamiento = models.TextField(blank=True)

class Clase(models.Model):
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE)
    periodo = models.ForeignKey(PeriodoAcademico, on_delete=models.CASCADE)
    aula = models.ForeignKey(Aula, on_delete=models.CASCADE)
    horario = models.CharField(max_length=100)

class Inscripcion(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    clase = models.ForeignKey(Clase, on_delete=models.CASCADE)
    fecha_inscripcion = models.DateField(auto_now_add=True)
    estado = models.CharField(max_length=20, default='ACTIVA')

class Nota(models.Model):
    inscripcion = models.ForeignKey(Inscripcion, on_delete=models.CASCADE)
    periodo = models.ForeignKey(PeriodoAcademico, on_delete=models.CASCADE)
    tipo_evaluacion = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=5, decimal_places=2)
    fecha_registro = models.DateField(auto_now_add=True)

class Asistencia(models.Model):
    inscripcion = models.ForeignKey(Inscripcion, on_delete=models.CASCADE)
    fecha = models.DateField()
    estado = models.CharField(max_length=20)  # 'PRESENTE', 'AUSENTE', etc.
    justificacion = models.TextField(blank=True, null=True)

class Participacion(models.Model):
    inscripcion = models.ForeignKey(Inscripcion, on_delete=models.CASCADE)
    fecha = models.DateField()
    tipo = models.CharField(max_length=50)  # 'ORAL', 'PROYECTO', etc.
    valoracion = models.IntegerField()
    comentarios = models.TextField(blank=True)

class PrediccionRendimiento(models.Model):
    inscripcion = models.ForeignKey(Inscripcion, on_delete=models.CASCADE)
    fecha_prediccion = models.DateTimeField(auto_now_add=True)
    valor_prediccion = models.DecimalField(max_digits=5, decimal_places=2)
    categoria_rendimiento = models.CharField(max_length=20)  # 'BAJO', 'MEDIO', 'ALTO'
    modelo_utilizado = models.CharField(max_length=100)"""

from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class Usuario(AbstractUser):
    estado = models.CharField(max_length=20, default='ACTIVO')

    ROL_CHOICES = [
        ('ADMINISTRADOR', 'Administrador'),
        ('PROFESOR', 'Profesor'),
        ('ALUMNO', 'Alumno'),
        ('APODERADO', 'Apoderado'),
    ]
    rol = models.CharField(max_length=30, choices=ROL_CHOICES, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.username} ({self.rol})"
    
class Administrador(models.Model):
    usuario = models.OneToOneField('Usuario', on_delete=models.CASCADE, primary_key=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)

class Profesor(models.Model):
    usuario = models.OneToOneField('Usuario', on_delete=models.CASCADE, primary_key=True)
    especialidad = models.CharField(max_length=100)
    titulo = models.CharField(max_length=100)
    fecha_contratacion = models.DateField()

class Alumno(models.Model):
    usuario = models.OneToOneField('Usuario', on_delete=models.CASCADE, primary_key=True)
    fecha_nacimiento = models.DateField()
    genero = models.CharField(max_length=1, choices=[('M', 'Masculino'), ('F', 'Femenino')])
    direccion = models.TextField()
    telefono_emergencia = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"{self.usuario.get_full_name()}"

class Apoderado(models.Model):
    usuario = models.OneToOneField('Usuario', on_delete=models.CASCADE, primary_key=True)
    parentesco = models.CharField(max_length=50)
    ocupacion = models.CharField(max_length=100)
    genero = models.CharField(max_length=1, choices=[('M', 'Masculino'), ('F', 'Femenino')])
    direccion_trabajo = models.TextField()
    telefono = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.usuario.get_full_name()} ({self.parentesco})"

# Alumno_Apoderado
class AlumnoApoderado(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    apoderado = models.ForeignKey(Apoderado, on_delete=models.CASCADE)
    parentesco = models.CharField(max_length=50)
    es_principal = models.BooleanField(default=False)

    class Meta:
        constraints = [
        models.UniqueConstraint(fields=['alumno', 'apoderado'], name='unique_alumno_apoderado')
    ]

# Gestion Academica
class Gestion(models.Model):
    nombre = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    estado = models.CharField(max_length=20, default='PLANIFICADA')

    def __str__(self):
        return self.nombre

# Periodo Academico
class Periodo(models.Model):
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nombre} ({self.tipo})"

# Gestion_Periodo
class GestionPeriodo(models.Model):
    gestion = models.ForeignKey(Gestion, on_delete=models.CASCADE)
    periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE)
    fechaini_periodo = models.DateField()
    fechafin_periodo = models.DateField()

    def __str__(self):
        return f"{self.gestion.nombre} - {self.periodo.nombre}"

    class Meta:
        constraints = [
        models.UniqueConstraint(fields=['gestion', 'periodo'], name='unique_gestion_periodo')
    ]

# Grado (Curso)
class Grado(models.Model):
    nombre = models.CharField(max_length=100)
    estado = models.CharField(max_length=20, default='ACTIVA')

    def __str__(self):
        return self.nombre

#GestionGrado
class GestionGrado(models.Model):
    gestion = models.ForeignKey(Gestion, on_delete=models.CASCADE)
    grado = models.ForeignKey(Grado, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.gestion.nombre} - {self.grado.nombre}"

    class Meta:
        constraints = [
        models.UniqueConstraint(fields=['gestion', 'grado'], name='unique_gestion_grado')
    ]

# Materia
class Materia(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    nivel = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

#GestionGrado_Materia
class GestionGradoMateria(models.Model):
    gestiongrado = models.ForeignKey(GestionGrado, on_delete=models.CASCADE)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)

    class Meta:
        constraints = [
        models.UniqueConstraint(fields=['gestiongrado', 'materia'], name='unique_gestiongrado_materia')
    ]

class Aula(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    edificio = models.CharField(max_length=50)
    piso = models.IntegerField()
    capacidad = models.IntegerField()
    tipo = models.CharField(max_length=50)
    equipamiento = models.TextField(blank=True)

    def __str__(self):
        return f"Aula {self.codigo} - {self.edificio} Piso {self.piso}"

class Horario(models.Model):
    aula = models.ForeignKey(Aula, on_delete=models.CASCADE)
    gestiongradomateria = models.ForeignKey(GestionGradoMateria, on_delete=models.CASCADE)
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE)
    dia = models.CharField(max_length=20)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    def __str__(self):
        return f"{self.dia} {self.hora_inicio}-{self.hora_fin} - {self.gestiongradomateria.materia.nombre}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['aula', 'dia', 'hora_inicio', 'hora_fin'],
                name='unique_horario_aula_dia_hora'
            )
        ]

class Inscripcion(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    gestiongrado = models.ForeignKey(GestionGrado, on_delete=models.CASCADE, null=True, blank=True)
    fecha_inscripcion = models.DateField(auto_now_add=True)
    estado = models.CharField(max_length=20, default='ACTIVA')

    def __str__(self):
        return f"{self.alumno.usuario.username} - {self.gestiongrado.grado.nombre} ({self.estado})"

class Nota(models.Model):
    inscripcion = models.ForeignKey(Inscripcion, on_delete=models.CASCADE)
    gestionperiodo = models.ForeignKey(GestionPeriodo, on_delete=models.CASCADE, null=True, blank=True)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, null=True, blank=True)
    tipo_evaluacion = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=5, decimal_places=2)
    fecha_registro = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.inscripcion.alumno.usuario.username} - {self.materia.nombre} - {self.valor}"

class Asistencia(models.Model):
    inscripcion = models.ForeignKey(Inscripcion, on_delete=models.CASCADE)
    fecha = models.DateField()
    estado = models.CharField(max_length=20)  # 'PRESENTE', 'AUSENTE', etc.
    justificacion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.inscripcion.alumno.usuario.username} - {self.fecha} - {self.estado}"

class Participacion(models.Model):
    inscripcion = models.ForeignKey(Inscripcion, on_delete=models.CASCADE)
    fecha = models.DateField()
    tipo = models.CharField(max_length=50)  # 'ORAL', 'PROYECTO', etc.
    valoracion = models.IntegerField()
    comentarios = models.TextField(blank=True)

    def __str__(self):
        return f"{self.inscripcion.alumno.usuario.username} - {self.tipo} ({self.valoracion})"

class PrediccionRendimiento(models.Model):
    inscripcion = models.ForeignKey(Inscripcion, on_delete=models.CASCADE)
    fecha_prediccion = models.DateTimeField(auto_now_add=True)
    valor_prediccion = models.DecimalField(max_digits=5, decimal_places=2)
    categoria_rendimiento = models.CharField(max_length=20)  # 'BAJO', 'MEDIO', 'ALTO'
    modelo_utilizado = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.inscripcion.alumno.usuario.username} - {self.categoria_rendimiento}"
