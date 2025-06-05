from datetime import datetime

# Clase base Usuario
class Usuario:
    """Clase base que representa un usuario del sistema académico."""
    
    def __init__(self, id_usuario, nombre, email):
        """
        Constructor de la clase Usuario.
        
        Args:
            id_usuario (str): Identificador único del usuario
            nombre (str): Nombre completo del usuario
            email (str): Correo electrónico del usuario
        """
        self._id = id_usuario
        self._nombre = nombre
        self._email = email
    
    def mostrar_info(self):
        """Retorna la información básica del usuario."""
        return f"ID: {self._id}, Nombre: {self._nombre}, Email: {self._email}"

# Clase Estudiante hereda de Usuario
class Estudiante(Usuario):
    """Clase que representa un estudiante en el sistema académico."""
    
    def __init__(self, id_usuario, nombre, email, carrera, semestre):
        """
        Constructor de la clase Estudiante.
        
        Args:
            id_usuario (str): Identificador único del estudiante
            nombre (str): Nombre completo del estudiante
            email (str): Correo electrónico del estudiante
            carrera (str): Carrera que estudia
            semestre (int): Semestre actual
        """
        super().__init__(id_usuario, nombre, email)
        self._carrera = carrera
        self._semestre = semestre
        self._materias_matriculadas = []
        self._calificaciones = {}
    
    def matricular_materia(self, asignatura):
        """Matricula al estudiante en una asignatura."""
        if asignatura not in self._materias_matriculadas:
            self._materias_matriculadas.append(asignatura)
            return f"Materia {asignatura.nombre} matriculada exitosamente"
        return "Ya está matriculado en esta materia"
    
    def calcular_promedio(self):
        """Calcula el promedio general del estudiante."""
        if not self._calificaciones:
            return 0
        return sum(self._calificaciones.values()) / len(self._calificaciones)
    
    def consultar_horario(self):
        """Consulta el horario de clases del estudiante."""
        horarios = []
        for materia in self._materias_matriculadas:
            if hasattr(materia, 'horario') and materia.horario:
                horarios.append(f"{materia.nombre}: {materia.horario.obtener_info()}")
        return horarios if horarios else ["No tiene horarios asignados"]
    
    def mostrar_info(self):
        """Retorna la información completa del estudiante."""
        info_base = super().mostrar_info()
        return f"{info_base}, Carrera: {self._carrera}, Semestre: {self._semestre}"

# Clase Docente hereda de Usuario
class Docente(Usuario):
    """Clase que representa un docente en el sistema académico."""
    
    def __init__(self, id_usuario, nombre, email, departamento, salario):
        """
        Constructor de la clase Docente.
        
        Args:
            id_usuario (str): Identificador único del docente
            nombre (str): Nombre completo del docente
            email (str): Correo electrónico del docente
            departamento (str): Departamento al que pertenece
            salario (float): Salario del docente
        """
        super().__init__(id_usuario, nombre, email)
        self._departamento = departamento
        self._salario = salario
        self._materias_asignadas = []
    
    def asignar_materia(self, asignatura):
        """Asigna una materia al docente."""
        if asignatura not in self._materias_asignadas:
            self._materias_asignadas.append(asignatura)
            asignatura.asignar_docente(self)
            return f"Materia {asignatura.nombre} asignada al docente"
        return "Ya tiene asignada esta materia"
    
    def calificar_estudiante(self, estudiante, asignatura, nota):
        """Registra una calificación para un estudiante."""
        if 0 <= nota <= 20:
            estudiante._calificaciones[asignatura.codigo] = nota
            return f"Nota {nota} registrada para {estudiante._nombre}"
        return "Nota inválida (debe estar entre 0 y 20)"
    
    def consultar_horario(self):
        """Consulta el horario de clases del docente."""
        horarios = []
        for materia in self._materias_asignadas:
            if hasattr(materia, 'horario') and materia.horario:
                horarios.append(f"{materia.nombre}: {materia.horario.obtener_info()}")
        return horarios if horarios else ["No tiene horarios asignados"]
    
    def mostrar_info(self):
        """Retorna la información completa del docente."""
        info_base = super().mostrar_info()
        return f"{info_base}, Departamento: {self._departamento}"

# Clase Asignatura
class Asignatura:
    """Clase que representa una asignatura o materia."""
    
    def __init__(self, codigo, nombre, creditos):
        """
        Constructor de la clase Asignatura.
        
        Args:
            codigo (str): Código único de la asignatura
            nombre (str): Nombre de la asignatura
            creditos (int): Número de créditos
        """
        self.codigo = codigo
        self.nombre = nombre
        self.creditos = creditos
        self.docente_asignado = None
        self.estudiantes_matriculados = []
        self.horario = None
    
    def asignar_docente(self, docente):
        """Asigna un docente a la asignatura."""
        self.docente_asignado = docente
    
    def asignar_horario(self, horario):
        """Asigna un horario a la asignatura."""
        self.horario = horario
        horario.asignatura = self
    
    def obtener_estudiantes(self):
        """Retorna la lista de nombres de estudiantes matriculados."""
        return [est._nombre for est in self.estudiantes_matriculados]
    
    def __str__(self):
        return f"{self.codigo} - {self.nombre} ({self.creditos} créditos)"

# Clase Horario
class Horario:
    """Clase que representa un horario de clases."""
    
    def __init__(self, dia, hora_inicio, hora_fin, aula):
        """
        Constructor de la clase Horario.
        
        Args:
            dia (str): Día de la semana
            hora_inicio (str): Hora de inicio de la clase
            hora_fin (str): Hora de finalización de la clase
            aula (str): Aula donde se imparte la clase
        """
        self.dia = dia
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.aula = aula
        self.asignatura = None
    
    def obtener_info(self):
        """Retorna la información del horario."""
        return f"{self.dia} {self.hora_inicio}-{self.hora_fin} (Aula: {self.aula})"
    
    def consultar_horario_estudiante(self, estudiante):
        """Consulta si un estudiante tiene clase en este horario."""
        if self.asignatura and self.asignatura in estudiante._materias_matriculadas:
            return f"{estudiante._nombre} tiene clase de {self.asignatura.nombre} el {self.obtener_info()}"
        return f"{estudiante._nombre} no tiene clase en este horario"

# Clase Matricula
class Matricula:
    """Clase que gestiona la matrícula de estudiantes en asignaturas."""
    
    def __init__(self, estudiante, asignatura):
        """
        Constructor de la clase Matricula.
        
        Args:
            estudiante (Estudiante): El estudiante a matricular
            asignatura (Asignatura): La asignatura en la que se matricula
        """
        self.estudiante = estudiante
        self.asignatura = asignatura
        self.fecha_matricula = datetime.now()
    
    def registrar_matricula(self):
        """Registra la matrícula del estudiante en la asignatura."""
        resultado = self.estudiante.matricular_materia(self.asignatura)
        if "exitosamente" in resultado:
            self.asignatura.estudiantes_matriculados.append(self.estudiante)
        return resultado
    
    def cancelar_matricula(self):
        """Cancela la matrícula del estudiante en la asignatura."""
        if self.asignatura in self.estudiante._materias_matriculadas:
            self.estudiante._materias_matriculadas.remove(self.asignatura)
            self.asignatura.estudiantes_matriculados.remove(self.estudiante)
            return "Matrícula cancelada"
        return "No está matriculado en esta materia"

# Clase Evaluacion
class Evaluacion:
    """Clase que gestiona las evaluaciones y calificaciones."""
    
    def __init__(self, estudiante, asignatura, nota):
        """
        Constructor de la clase Evaluacion.
        
        Args:
            estudiante (Estudiante): El estudiante evaluado
            asignatura (Asignatura): La asignatura evaluada
            nota (float): La calificación obtenida
        """
        self.estudiante = estudiante
        self.asignatura = asignatura
        self.nota = nota
        self.fecha = datetime.now()
    
    def registrar_nota(self):
        """Registra la nota en el sistema."""
        if 0 <= self.nota <= 20:
            self.estudiante._calificaciones[self.asignatura.codigo] = self.nota
            return f"Nota {self.nota} registrada"
        return "Nota inválida"

# Ejemplo de uso del sistema
def demo_sistema():
    """Función de demostración del sistema académico."""
    print("=== DEMO SISTEMA DE GESTIÓN ACADÉMICA INTEGRAL ===\n")
    
    # Crear estudiantes
    est1 = Estudiante("E001", "Ana García", "ana@unemi.edu.ec", "Sistemas", 5)
    est2 = Estudiante("E002", "Carlos López", "carlos@unemi.edu.ec", "Sistemas", 5)
    
    # Crear docente
    doc1 = Docente("D001", "Dr. José Martínez", "jose@unemi.edu.ec", "Informática", 2500)
    
    # Crear asignaturas
    ing_soft = Asignatura("IS001", "Ingeniería de Software I", 4)
    prog_web = Asignatura("PW001", "Programación Web", 3)
    
    # Crear horarios
    horario1 = Horario("Lunes", "08:00", "10:00", "Lab-101")
    horario2 = Horario("Miércoles", "10:00", "12:00", "Aula-205")
    
    # Asignar horarios a materias
    ing_soft.asignar_horario(horario1)
    prog_web.asignar_horario(horario2)
    
    # Asignar docente a materias
    print(doc1.asignar_materia(ing_soft))
    print(doc1.asignar_materia(prog_web))
    
    # Matricular estudiantes
    mat1 = Matricula(est1, ing_soft)
    mat2 = Matricula(est2, ing_soft)
    mat3 = Matricula(est1, prog_web)
    
    print(mat1.registrar_matricula())
    print(mat2.registrar_matricula())
    print(mat3.registrar_matricula())
    
    # Registrar calificaciones
    print(doc1.calificar_estudiante(est1, ing_soft, 18))
    print(doc1.calificar_estudiante(est2, ing_soft, 16))
    print(doc1.calificar_estudiante(est1, prog_web, 19))
    
    # Mostrar información de estudiantes
    print(f"\n{est1.mostrar_info()}")
    print(f"Promedio: {est1.calcular_promedio():.2f}")
    print("Horario de clases:")
    for horario in est1.consultar_horario():
        print(f"  - {horario}")
    
    print(f"\n{est2.mostrar_info()}")
    print(f"Promedio: {est2.calcular_promedio():.2f}")
    print("Horario de clases:")
    for horario in est2.consultar_horario():
        print(f"  - {horario}")
    
    # Mostrar información del docente
    print(f"\n{doc1.mostrar_info()}")
    print("Horario de clases del docente:")
    for horario in doc1.consultar_horario():
        print(f"  - {horario}")
    
    # Mostrar estudiantes por materia
    print(f"\nEstudiantes en {ing_soft.nombre}: {ing_soft.obtener_estudiantes()}")
    print(f"Estudiantes en {prog_web.nombre}: {prog_web.obtener_estudiantes()}")
    
    # Consultar horario específico
    print(f"\n{horario1.consultar_horario_estudiante(est1)}")
    print(f"{horario2.consultar_horario_estudiante(est2)}")

if __name__ == "__main__":
    demo_sistema()