// Código de prueba de Emily Valarezo Plaza
// Lenguajes de Programación
// Gestión básica de estudiantes

// Clase para representar a un estudiante
class Student {
    // Propiedades de la clase Student
    name: string;     // Nombre del estudiante
    age: number;      // Edad del estudiante
    grades: number[]; // Arreglo de calificaciones del estudiante

    // Constructor de la clase Student para inicializar las propiedades
    constructor(name: string, age: number, grades: number[]) {
        this.name = name;   // Asignar el nombre del estudiante
        this.age = age;     // Asignar la edad del estudiante
        this.grades = grades; // Asignar las calificaciones del estudiante
    }

    // Método para calcular el promedio de las calificaciones
    calculateAverage(): number {
        let sum: number = 0; // Variable para almacenar la suma de las calificaciones
        // Recorremos las calificaciones y las sumamos
        for (let grade of this.grades) {
            sum += grade;
        }
        // Devolvemos el promedio dividiendo la suma entre el número de calificaciones
        return sum / this.grades.length;
    }

    // Método para verificar si el estudiante aprobó
    isPassing(): boolean {
        // El estudiante aprueba si el promedio es mayor o igual a 7.0
        return this.calculateAverage() >= 7.0;
    }
}

// Función principal que se ejecuta al correr el programa
function main(): void {
    // Creamos un objeto de tipo Student con nombre, edad y un arreglo de calificaciones
    let student1: Student = new Student("Alice", 20, [8, 9, 7, 10]);
    
    // Mostramos el nombre del estudiante
    console.log(`Estudiante: ${student1.name}`);
    // Calculamos y mostramos el promedio de las calificaciones
    console.log("Promedio:", student1.calculateAverage());
    
    // Verificamos si el estudiante aprobó y mostramos el estado
    if (student1.isPassing()) {
        console.log("Estado: Aprobado");
    } else {
        console.log("Estado: Reprobado");
    }
}

// Llamamos a la función main para que se ejecute el programa
main();
