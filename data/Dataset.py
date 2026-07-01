#Data in spanish 
dataset = [
    # work_assignment 
    {"text": "Anota que tengo que entregar el laboratorio de redes el martes", "label": "work_assignment"},
    {"text": "Recordarme subir la asignación de base de datos antes de medianoche", "label": "work_assignment"},
    {"text": "Agrega estudiar para el quiz de cálculo mañana a las 7 AM", "label": "work_assignment"},
    {"text": "Crear recordatorio para reunirme con el grupo del proyecto final el jueves", "label": "work_assignment"},
    {"text": "Anota repasar los conceptos de inteligencia artificial hoy en la tarde", "label": "work_assignment"},
    {"text": "Hola, necesito programar una nueva asignación", "label": "work_assignment"},
    {"text": "Hola, ayúdame a organizar mis tareas de la universidad", "label": "work_assignment"},
    # Date
    {"text": "¿Qué entregas o evaluaciones tengo programadas para esta semana?", "label": "date"},
    {"text": "¿A qué hora era la entrega del proyecto de sistemas operativos hoy?", "label": "date"},
    {"text": "¿Hay alguna tarea pendiente para la clase de mañana?", "label": "date"},
    {"text": "Muéstrame el horario de los exámenes parciales de este mes", "label": "date"},
    {"text": "¿Qué pendientes universitarios tengo registrados para el viernes?", "label": "date"},
    {"text": "Hola, necesito revisar mis pendientes de la u", "label": "date"},
    {"text": "Buenas, ¿qué hay en el calendario académico para hoy?", "label": "date"},
    {"text": "Qué tal, ¿me muestras mis entregas pendientes?", "label": "date"},
    #Conflict
    {"text": "El examen de compiladores se cruza con el horario de alguna otra materia?", "label": "conflict"},
    {"text": "¿Tengo alguna entrega asignada a la misma hora de la tutoría?", "label": "conflict"},
    {"text": "¿Hay algún otro proyecto que deba entregar ese mismo día?", "label": "conflict"},
    {"text": "Revisa si tengo libre el bloque de las 2 PM para avanzar la tesis", "label": "conflict"},
    {"text": "¿Esa entrega interfiere con la clase de arquitectura de computadoras?", "label": "conflict"},
    #Priority
    {"text": "El proyecto de estructura de datos es lo más crítico de la semana", "label": "priority"},
    {"text": "Pon la entrega de ingeniería de software como prioridad máxima", "label": "priority"},
    {"text": "Esa tarea de investigación no urge, tiene ponderación baja", "label": "priority"},
    {"text": "Lo primero que debo terminar hoy es la práctica del laboratorio", "label": "priority"},
    {"text": "Marca la lectura obligatoria de ética como prioridad media", "label": "priority"},
    #Greeting
    {"text": "Buenos dias?", "label": "greeting"},
    {"text": "Hola", "label": "greeting"},
    {"text": "Buenas noches", "label": "greeting"},
    {"text": "Hey", "label": "greeting"},
    {"text": "Como va todo?", "label": "greeting"}
]

label2id = {"work_assignment": 0,
            "date": 1,
            "conflict": 2,
            "priority" : 3,
            "greeting": 4}
            
id2label = {0 :"work_assignment",
            1 :"date",
            2 :"conflict",
            3 :"priority",
            4 :"greeting",
}
            
