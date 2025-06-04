# core/management/commands/poblar.py
from django.utils.crypto import get_random_string
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import *

from faker import Faker
import random
from django.utils.timezone import make_aware
from datetime import date, timedelta, datetime, time
from random import choice, randint, uniform, sample
from decimal import Decimal
from django.utils import timezone

from collections import defaultdict
import re

class Command(BaseCommand):
    help = 'Pobla la base de datos con datos de prueba'

    def handle(self, *args, **kwargs):
        fake = Faker()
        
        #Creando administradores
        self.stdout.write("Creando administradores...")

        cantidad_admins = randint(3, 5)
        for i in range(cantidad_admins):
            username = f'admin{i}'
            user = Usuario.objects.filter(username=username).first()
            if not user:
                user = Usuario(
                    username=username,
                    email=f'{username}@google.com',
                    rol='ADMINISTRADOR',
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    is_active=True
                )
                user.set_password('admin12345')
                user.save()

                Administrador.objects.create(
                    usuario=user,
                    telefono = f"+591 {randint(60000000, 79999999)}"
                )

                self.stdout.write(self.style.SUCCESS(f"Administrador creado: {username}"))
            else:
                self.stdout.write(self.style.WARNING(f"Usuario {username} ya existe, omitiendo."))

        #Creando profesores
        self.stdout.write("Creando profesores por materia...")

        materias = [
            "Lengua castellana y originaria",
            "Lengua extranjera",
            "Ciencias sociales",
            "Educación física y deportes",
            "Educación musical",
            "Artes plásticas y visuales",
            "Matemática",
            "Contaduría general",
            "Biología - Geografía",
            "Física",
            "Química",
            "Cosmovisiones, Filosofía y Psicología",
            "Valores, Espiritualidad y Religiones"
        ]

        profesores = []
        contador = 0

        for materia in materias:
            nombre_corto = materia.split()[0].lower()
            for i in range(1, 4):
                contador += 1
                username = f'{nombre_corto}{i}'
                user = Usuario.objects.filter(username=username).first()
                if not user:
                    user = Usuario(
                        username=username,
                        email=f'{username}@test.com',
                        first_name=fake.first_name(),
                        last_name=fake.last_name(),
                        rol='PROFESOR',
                        is_active=True
                    )
                    user.set_password('12345678')
                    user.save()

                    profesor = Profesor.objects.create(
                        usuario=user,
                        especialidad=materia,
                        titulo=fake.job(),
                        fecha_contratacion=fake.date_between(start_date='-10y', end_date='today')
                    )
                    profesores.append(profesor)
                    self.stdout.write(f"Profesor creado: {username} - {materia}")
                else:
                    self.stdout.write(f"Usuario {username} ya existe, omitiendo.")

        # Creando alumnos
        self.stdout.write("Creando alumnos por edad...")

        alumnos = []
        contador_global = 1

        for edad in range(12, 18+1):
            cantidad = random.randint(50, 60)
            self.stdout.write(f"Creando {cantidad} alumnos de {edad} años...")

            for i in range(cantidad):
                username = f'alumno{contador_global}'
                user = Usuario.objects.filter(username=username).first()
                if not user:
                    # Calcular fecha de nacimiento aproximada para la edad
                    nacimiento = date.today().replace(year=date.today().year - edad)
                    nacimiento += timedelta(days=random.randint(-180, 180))  # +/- 6 meses

                    user = Usuario(
                        username=username,
                        email=f'{username}@test.com',
                        first_name=fake.first_name(),
                        last_name=fake.last_name(),
                        rol='ALUMNO',
                        is_active=True
                    )
                    user.set_password('12345678')
                    user.save()

                    alumno = Alumno.objects.create(
                        usuario=user,
                        fecha_nacimiento=nacimiento,
                        genero=random.choice(['M', 'F']),
                        direccion=fake.address(),
                        telefono_emergencia = f"+591 {randint(60000000, 79999999)}"
                    )
                    alumnos.append(alumno)
                    self.stdout.write(f"Alumno creado: {username}")
                else:
                    self.stdout.write(f"Usuario {username} ya existe, omitiendo.")
                
                contador_global += 1

        # apoderados por alumno
        self.stdout.write("Creando apoderados por alumno...")
        apoderado_count = 0
        genero_choices = ['M', 'F']

        for alumno in Alumno.objects.all():
            for j in range(2):  # 2 apoderados por alumno
                username = f'apoderado_{alumno.usuario.username}_{j}'

                if Usuario.objects.filter(username=username).exists():
                    continue

                genero = genero_choices[j % 2]  # Alternar M y F

                user = Usuario(
                    username=username,
                    email=f'{username}@test.com',
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    rol='APODERADO',
                    is_active=True
                )
                user.set_password('12345678')
                user.save()

                apoderado = Apoderado.objects.create(
                    usuario=user,
                    parentesco='Padre' if genero == 'M' else 'Madre',
                    ocupacion=fake.job(),
                    direccion_trabajo=fake.address(),
                    telefono = f"+591 {randint(60000000, 79999999)}",
                    genero=genero
                )

                # Relación en tabla intermedia
                AlumnoApoderado.objects.create(
                    alumno=alumno,
                    apoderado=apoderado,
                    parentesco='Padre' if genero == 'M' else 'Madre',
                    es_principal=(j == 0)  # El primero será principal
                )

                apoderado_count += 1
                self.stdout.write(f"Apoderado creado: {username} para alumno {alumno.usuario.username}")

        self.stdout.write(self.style.SUCCESS(f"Total apoderados creados: {apoderado_count}"))

        # Creando gestiones
        self.stdout.write("Creando gestiones académicas...")

        estados = ['FINALIZADO', 'FINALIZADO', 'FINALIZADO', 'FINALIZADO', 'FINALIZADO', 'EN CURSO']  # Puedes ajustar según tu lógica

        gestiones = []
        for i, anio in enumerate(range(2020, 2026)):
            nombre = f"Gestión {anio}"
            fecha_inicio = date(anio, 2, 10)
            fecha_fin = date(anio, 11, 28)
    
            gestion, created = Gestion.objects.get_or_create(
                nombre=nombre,
                defaults={
                    'fecha_inicio': fecha_inicio,
                    'fecha_fin': fecha_fin,
                    'estado': estados[i] if i < len(estados) else 'PLANIFICADO'
                }
            )
            gestiones.append(gestion)
            if created:
                self.stdout.write(f"{nombre} creada.")
            else:
                self.stdout.write(f"{nombre} ya existía.")
        
        # Crear periodos base (si aún no existen)
        self.stdout.write("Creando periodos base...")

        nombres_periodo = ['Primer Trimestre', 'Segundo Trimestre', 'Tercer Trimestre']
        tipo_periodo = 'Trimestral'

        # Creamos los 3 periodos únicos
        periodos_dict = {}  # para evitar consultas repetidas
        for nombre in nombres_periodo:
            periodo, _ = Periodo.objects.get_or_create(
                nombre=nombre,
                tipo=tipo_periodo
            )
            periodos_dict[nombre] = periodo

        # Crear relación GestionPeriodo
        self.stdout.write("Creando relaciones GestionPeriodo...")

        for gestion in Gestion.objects.all():
            for i, nombre_periodo in enumerate(nombres_periodo):
                fecha_inicio = gestion.fecha_inicio + timedelta(days=i * 90)
                fecha_fin = fecha_inicio + timedelta(days=89)

                periodo = periodos_dict[nombre_periodo]

                gp, created = GestionPeriodo.objects.get_or_create(
                    gestion=gestion,
                    periodo=periodo,
                    defaults={
                        'fechaini_periodo': fecha_inicio,
                        'fechafin_periodo': fecha_fin
                    }
                )

                if created:
                    self.stdout.write(f"Relacion {gestion.nombre} - {nombre_periodo} creada.")
                else:
                    self.stdout.write(f"Relacion {gestion.nombre} - {nombre_periodo} ya existía.")

        # Poblar Grados
        self.stdout.write("Creando grados...")

        nombres_grado = [
            "Primero - A",
            "Primero - B",
            "Segundo - A",
            "Segundo - B",
            "Tercero - A",
            "Tercero - B",
            "Cuarto - A",
            "Cuarto - B",
            "Quinto - A",
            "Quinto - B",
            "Sexto - A",
            "Sexto - B"
        ]

        grados = []  # Guardamos referencias para usarlas luego

        for nombre in nombres_grado:
            grado, created = Grado.objects.get_or_create(nombre=nombre)
            grados.append(grado)
            if created:
                self.stdout.write(f"Grado '{nombre}' creado.")
            else:
                self.stdout.write(f"Grado '{nombre}' ya existía.")

        # Poblar GestionGrado teniendo en cuenta los grados ya con paralelos
        self.stdout.write("Creando combinaciones Gestion-Grado con paralelos...")

        for gestion in Gestion.objects.all():
            for grado in Grado.objects.all():
                gg, created = GestionGrado.objects.get_or_create(gestion=gestion, grado=grado)
                if created:
                    self.stdout.write(f"GestionGrado creado: {gestion.nombre} - {grado.nombre}")
                else:
                    self.stdout.write(f"GestionGrado ya existía: {gestion.nombre} - {grado.nombre}")

        # Creando materias
        self.stdout.write("Creando materias...")

        materias_secundarias = [
            "Lengua castellana y originaria",
            "Lengua extranjera",
            "Ciencias sociales",
            "Educación física y deportes",
            "Educación musical",
            "Artes plásticas y visuales",
            "Matemática",
            "Contaduría general",
            "Biología - Geografía",
            "Física",
            "Química",
            "Cosmovisiones, Filosofía y Psicología",
            "Valores, Espiritualidad y Religiones"
        ]

        for nombre in materias_secundarias:
            materia, created = Materia.objects.get_or_create(
                nombre=nombre,
                defaults={
                    'descripcion': f'Materia de {nombre.lower()} para nivel secundario.',
                    'nivel': 'Secundario'
                }
            )
            if created:
                self.stdout.write(f"Materia creada: {nombre}")
            else:
                self.stdout.write(f"Materia ya existe: {nombre}")

        # Creando combinaciones de GestionGrado y Materia
        self.stdout.write("Creando combinaciones GestionGrado-Materia...")

        materias = Materia.objects.all()
        gestiongrados = GestionGrado.objects.all()

        for gg in gestiongrados:
            for materia in materias:
                ggm, created = GestionGradoMateria.objects.get_or_create(
                    gestiongrado=gg,
                    materia=materia
                )
                if created:
                    self.stdout.write(f"Asignada materia '{materia.nombre}' a {gg.gestion.nombre} - {gg.grado.nombre}")
                else:
                    self.stdout.write(f"Ya existía asignación de '{materia.nombre}' a {gg.gestion.nombre} - {gg.grado.nombre}")

        # Creando aulas
        self.stdout.write("Creando aulas...")

        # 12 Aulas normales
        for i in range(1, 13):
            codigo = f'A-{100 + i}'
            Aula.objects.get_or_create(
                codigo=codigo,
                defaults={
                    'edificio': 'Principal',
                    'piso': (i - 1) // 4 + 1,
                    'capacidad': 30,
                    'tipo': 'Teoría',
                    'equipamiento': 'Pizarra, proyector'
                }
            )
            self.stdout.write(f"Aula normal creada: {codigo}")

        # 6 Aulas especiales
        aulas_especiales = [
            {
                'codigo': 'LAB-FISICA',
                'tipo': 'Laboratorio',
                'equipamiento': 'Mesas de laboratorio, materiales de física'
            },
            {
                'codigo': 'LAB-QUIMICA',
                'tipo': 'Laboratorio',
                'equipamiento': 'Mesas de laboratorio, materiales de química'
            },
            {
                'codigo': 'LAB-BIOLOGIA',
                'tipo': 'Laboratorio',
                'equipamiento': 'Microscopios, muestras biológicas'
            },
            {
                'codigo': 'AULA-MUSICA',
                'tipo': 'Especial',
                'equipamiento': 'Instrumentos musicales, acústica acondicionada'
            },
            {
                'codigo': 'AULA-ARTE',
                'tipo': 'Especial',
                'equipamiento': 'Caballetes, materiales de pintura y dibujo'
            },
            {
                'codigo': 'CANCHA',
                'tipo': 'Deportes',
                'equipamiento': 'Balones, colchonetas, cancha múltiple'
            }
        ]

        for aula_data in aulas_especiales:
            Aula.objects.get_or_create(
                codigo=aula_data['codigo'],
                defaults={
                    'edificio': 'Anexo',
                    'piso': 1,
                    'capacidad': 30,
                    'tipo': aula_data['tipo'],
                    'equipamiento': aula_data['equipamiento']
                }
            )
            self.stdout.write(f"Aula especial creada: {aula_data['codigo']}")

        # Días y horas disponibles (turno mañana)
        DAYS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
        HORAS = [
            (time(7, 0), time(8, 0)),
            (time(8, 0), time(9, 0)),
            (time(9, 0), time(10, 0)),
            (time(10, 0), time(11, 0)),
            (time(11, 0), time(12, 0))
        ]

        self.stdout.write("Generando horarios...")

        # Obtener datos existentes
        aulas = list(Aula.objects.all())
        gestion_grado_materias = GestionGradoMateria.objects.select_related("materia").all()
        profesores = Profesor.objects.select_related("usuario").all()

        # Indexar profesores por especialidad
        profesores_por_materia = {}
        for prof in profesores:
            prof_materia = prof.especialidad.strip().lower()
            profesores_por_materia.setdefault(prof_materia, []).append(prof)

        # Generar horarios
        usados = set()

        for ggm in gestion_grado_materias:
            nombre_materia = ggm.materia.nombre.strip().lower()
            posibles_profesores = profesores_por_materia.get(nombre_materia)

            if not posibles_profesores:
                self.stdout.write(f"No hay profesores para la materia '{ggm.materia.nombre}', omitiendo.")
                continue

            profesor = random.choice(posibles_profesores)
            
            horarios_creados = 0
            intentos_totales = 0

            while horarios_creados < 3 and intentos_totales < 50:  # 3 horarios por materia, 50 intentos máx.
                aula = random.choice(aulas)
                dia = random.choice(DAYS)
                hora_inicio, hora_fin = random.choice(HORAS)

                clave_aula = (aula.id, dia, hora_inicio, hora_fin)
                clave_profesor = (profesor.pk, dia, hora_inicio, hora_fin)

                if clave_aula not in usados and clave_profesor not in usados:
                    Horario.objects.create(
                        aula=aula,
                        gestiongradomateria=ggm,
                        profesor=profesor,
                        dia=dia,
                        hora_inicio=hora_inicio,
                        hora_fin=hora_fin
                    )
                    usados.add(clave_aula)
                    usados.add(clave_profesor)
                    self.stdout.write(f"Horario asignado: {ggm.materia.nombre} en {aula.codigo} con {profesor.usuario.get_full_name()} ({dia} {hora_inicio}-{hora_fin})")
                    horarios_creados += 1
                else:
                    intentos_totales += 1

            if horarios_creados < 3:
                self.stdout.write(f"Solo se pudieron asignar {horarios_creados}/3 horarios para {ggm.materia.nombre}")

        # Poblando inscripciones para la gestión 2025
        self.stdout.write("Poblando inscripciones para la gestión 2025...")

        ##gestion_2025 = Gestion.objects.filter(anio=2025).first()
        gestion_2025 = Gestion.objects.filter(fecha_inicio__year=2025).first()

        if not gestion_2025:
            self.stdout.write("Gestión 2025 no encontrada. Abortando inscripción.")
            return

        gestion_grados = GestionGrado.objects.filter(gestion=gestion_2025).select_related('grado')
        alumnos_disponibles = list(Alumno.objects.all())
        random.shuffle(alumnos_disponibles)

        edad_a_grupo = {
            12: "Primero",
            13: "Segundo",
            14: "Tercero",
            15: "Cuarto",
            16: "Quinto",
            17: "Sexto",
            18: "Sexto",
        }

        # Agrupar GestionGrado por clave ("Primero", "Segundo", etc.)
        grupos_grado = defaultdict(list)
        for gg in gestion_grados:
            match = re.match(r"(\w+)", gg.grado.nombre.strip())  # "Primero" de "Primero - A"
            if match:
                clave = match.group(1)
                grupos_grado[clave].append(gg)

        # Fase 1: Asegurar al menos 30 alumnos por cada grado
        inscripciones_creadas = 0
        for gg in gestion_grados:
            inscritos_actuales = Inscripcion.objects.filter(gestiongrado=gg).count()
            necesarios = max(0, 30 - inscritos_actuales)

            self.stdout.write(f"{gg.grado.nombre}: {inscritos_actuales} inscritos, necesitan {necesarios} más.")

            while necesarios > 0 and alumnos_disponibles:
                alumno = alumnos_disponibles.pop()

                edad = date.today().year - alumno.fecha_nacimiento.year
                if alumno.fecha_nacimiento > date.today().replace(year=date.today().year - edad):
                    edad -= 1

                grupo = edad_a_grupo.get(edad)
                if not grupo:
                    continue

                if not gg.grado.nombre.startswith(grupo):
                    continue  # No corresponde a este grado

                # Verifica si ya está inscrito en esa gestión
                if not Inscripcion.objects.filter(alumno=alumno, gestiongrado__gestion=gestion_2025).exists():
                    Inscripcion.objects.create(
                        alumno=alumno,
                        gestiongrado=gg,
                        estado='ACTIVA'
                    )
                    inscripciones_creadas += 1
                    necesarios -= 1
                    self.stdout.write(f"  - {alumno.usuario.username} inscrito en {gg.grado.nombre}")

        # Fase 2: Inscribir el resto de alumnos donde corresponda
        for alumno in alumnos_disponibles:
            edad = date.today().year - alumno.fecha_nacimiento.year
            if alumno.fecha_nacimiento > date.today().replace(year=date.today().year - edad):
                edad -= 1

            grupo = edad_a_grupo.get(edad)
            if not grupo:
                continue

            posibles_gg = grupos_grado.get(grupo)
            if not posibles_gg:
                continue

            if Inscripcion.objects.filter(alumno=alumno, gestiongrado__gestion=gestion_2025).exists():
                continue

            gestion_grado = random.choice(posibles_gg)
            Inscripcion.objects.create(
                alumno=alumno,
                gestiongrado=gestion_grado,
                estado='ACTIVA'
            )
            inscripciones_creadas += 1
            self.stdout.write(f"{alumno.usuario.username} inscrito en {gestion_grado.grado.nombre} (extra)")

        self.stdout.write(f"Total inscripciones creadas: {inscripciones_creadas}")
        # Resumen por grado
        self.stdout.write("\nResumen final de inscripciones por grado (Gestión 2025):")

        for gg in gestion_grados.order_by('grado__nombre'):
            cantidad = Inscripcion.objects.filter(gestiongrado=gg).count()
            self.stdout.write(f" - {gg.grado.nombre}: {cantidad} inscritos")

        # Generando Notas
        self.stdout.write("Generando notas para el 1er Trimestre de la gestión 2025...")

        # Obtener gestión 2025 y su 1er Trimestre
        gestion_2025 = Gestion.objects.get(fecha_inicio__year=2025)
        primer_trimestre = GestionPeriodo.objects.get(gestion=gestion_2025, periodo__nombre__icontains="Primer Trimestre")

        # Obtener inscripciones de la gestión 2025
        inscripciones = Inscripcion.objects.filter(gestiongrado__gestion=gestion_2025)

        # Tipos de evaluación definidos
        tipos_evaluacion = ["Examen", "Tarea", "Proyecto"]

        total_notas = 0

        for inscripcion in inscripciones:
            grado = inscripcion.gestiongrado.grado
            materias = GestionGradoMateria.objects.filter(gestiongrado__grado=grado, gestiongrado__gestion=gestion_2025).select_related('materia')

            for ggm in materias:
                for tipo in tipos_evaluacion:
                    cantidad = randint(2, 3)
                    for _ in range(cantidad):
                        valor = round(uniform(30, 100), 2)

                        Nota.objects.create(
                            inscripcion=inscripcion,
                            gestionperiodo=primer_trimestre,
                            materia=ggm.materia,
                            tipo_evaluacion=tipo,
                            valor=Decimal(valor)
                        )
                        total_notas += 1

        self.stdout.write(f"Notas generadas para el 1er Trimestre: {total_notas}")

        # Generando Asistencia
        self.stdout.write("Generando asistencias para el 1er Trimestre de la gestión 2025...")

        # Definimos el rango de fechas (1er trimestre aproximado)
        fecha_inicio = date(2025, 2, 1)
        fecha_fin = date(2025, 4, 30)

        # Generamos todas las fechas hábiles (lunes a viernes)
        fechas_habiles = []
        fecha_actual = fecha_inicio
        while fecha_actual <= fecha_fin:
            if fecha_actual.weekday() < 5:  # lunes a viernes
                fechas_habiles.append(fecha_actual)
            fecha_actual += timedelta(days=1)

        # Obtener todas las inscripciones activas de 2025
        gestion_2025 = Gestion.objects.get(fecha_inicio__year=2025)
        inscripciones = Inscripcion.objects.filter(gestiongrado__gestion=gestion_2025, estado='ACTIVA')

        # Estados posibles
        estados = ['PRESENTE', 'AUSENTE', 'TARDE']

        total_registros = 0

        for inscripcion in inscripciones:
            # Para cada alumno, generamos asistencia aleatoria para ciertas fechas
            fechas_asistencia = random.sample(fechas_habiles, k=min(20, len(fechas_habiles)))  # 20 días aleatorios

            for fecha in fechas_asistencia:
                estado = random.choices(estados, weights=[0.85, 0.10, 0.05])[0]  # Mayor probabilidad de presente
                justificacion = None

                if estado == 'AUSENTE' and random.random() < 0.5:
                    justificacion = "Falta justificada por motivo de salud."

                Asistencia.objects.create(
                    inscripcion=inscripcion,
                    fecha=fecha,
                    estado=estado,
                    justificacion=justificacion
                )
                total_registros += 1

        self.stdout.write(f"Total de registros de asistencia generados: {total_registros}")

        # Generando participacion
        self.stdout.write("Generando participaciones para el 1er Trimestre de la gestión 2025...")

        # Rango de fechas del 1er trimestre
        fecha_inicio = date(2025, 2, 1)
        fecha_fin = date(2025, 4, 30)

        # Fechas hábiles (lunes a viernes)
        fechas_habiles = []
        fecha_actual = fecha_inicio
        while fecha_actual <= fecha_fin:
            if fecha_actual.weekday() < 5:
                fechas_habiles.append(fecha_actual)
            fecha_actual += timedelta(days=1)

        # Tipos de participación
        tipos_participacion = ['ORAL', 'PROYECTO', 'GRUPAL', 'INDIVIDUAL']

        # Inscripciones activas en la gestión 2025
        gestion_2025 = Gestion.objects.get(fecha_inicio__year=2025)
        inscripciones = Inscripcion.objects.filter(gestiongrado__gestion=gestion_2025, estado='ACTIVA')

        total = 0

        for inscripcion in inscripciones:
            # Cada alumno tendrá entre 3 y 5 participaciones
            cantidad = random.randint(3, 5)
            fechas_participacion = random.sample(fechas_habiles, k=cantidad)

            for fecha in fechas_participacion:
                tipo = random.choice(tipos_participacion)
                valoracion = random.randint(1, 10)  # nota de 1 a 10
                comentario = ""
                if valoracion <= 4:
                    comentario = "Participación deficiente, debe mejorar."
                elif valoracion >= 9:
                    comentario = "Excelente participación."
                elif valoracion >= 7:
                    comentario = "Buena participación."

                Participacion.objects.create(
                    inscripcion=inscripcion,
                    fecha=fecha,
                    tipo=tipo,
                    valoracion=valoracion,
                    comentarios=comentario
                )
                total += 1

        self.stdout.write(f"Participaciones generadas: {total}")

        #Prediccion Rendimiento
        # Obtener todas las inscripciones de la gestión 2025
        gestion_2025 = Gestion.objects.get(fecha_inicio__year=2025)
        inscripciones_2025 = list(Inscripcion.objects.filter(gestiongrado__gestion=gestion_2025))

        # Seleccionar 50 al azar (si hay al menos 50)
        inscripciones_aleatorias = sample(inscripciones_2025, min(len(inscripciones_2025), 50))

        # Simular predicciones
        for inscripcion in inscripciones_aleatorias:
            valor = round(random.uniform(30, 100), 2)
            
            if valor < 50:
                categoria = "BAJO"
            elif valor < 75:
                categoria = "MEDIO"
            else:
                categoria = "ALTO"

            modelo = random.choice(["Modelo A", "Modelo B", "Regresión XGBoost", "Random Forest"])

            PrediccionRendimiento.objects.create(
                inscripcion=inscripcion,
                valor_prediccion=valor,
                categoria_rendimiento=categoria,
                modelo_utilizado=modelo
            )

            self.stdout.write(f"Predicción para {inscripcion.alumno.usuario.username}: {categoria} ({valor})")

        self.stdout.write("Datos académicos creados correctamente.")
