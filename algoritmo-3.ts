const pruebaVariables = () => {
    // Variables con tipos primitivos
    let nombre: string = "Juan Pérez";
    let edad: number = 25;
    let esEstudiante: boolean = true;
    
    // Constantes
    const PI: number = 3.1416;
    const SALUDO: string = "Hola mundo";
    
    // Arrays
    let numeros: number[] = [1, 2, 3, 4, 5];
    let mezclado: (string | number)[] = ["texto", 100, "otro texto", 200];
    
    // Objetos
    let persona: {nombre: string, edad: number} = {
        nombre: "María",
        edad: 30
    };
    
    console.log("Prueba de variables OK");
}

// 2. Operadores y signos
const pruebaOperadores = () => {
    // Operadores aritméticos
    let suma: number = 5 + 3;
    let resta: number = 10 - 4;
    let multiplicacion: number = 6 * 7;
    let division: number = 20 / 5;
    let modulo: number = 15 % 4;
    
    // Operadores de comparación
    let igual: boolean = (5 == 5);
    let mayorQue: boolean = (10 > 5);
    let menorQue: boolean = (3 < 8);
    
    // Operadores lógicos
    let andLogico: boolean = (true && false);
    let orLogico: boolean = (true || false);
    let notLogico: boolean = !true;
    
    console.log("Prueba de operadores OK");
}

// 3. Estructuras de control
const pruebaEstructuras = () => {
    // Condicional if
    let numero: number = 10;
    if (numero > 5) {
        console.log("Número es mayor que 5");
    } else {
        console.log("Número es 5 o menor");
    }
    
    // Bucle for
    for (let i = 0; i < 5; i++) {
        console.log(`Iteración ${i}`);
    }
    
    // Bucle while
    let contador: number = 3;
    while (contador > 0) {
        console.log(`Contador: ${contador}`);
        contador--;
    }
    
    console.log("Prueba de estructuras OK");
}

// 4. Funciones
const pruebaFunciones = (a: number, b: number): number => {
    return a + b;
}

// 5. Signos de puntuación
const pruebaSignos = () => {
    let puntos: string[] = ["Hola", "mundo", "!"];
    let comas: number[] = [1, 2, 3, 4];
    let puntoComa: string = "texto; más texto";
    let dosPuntos: {clave: string} = {clave: "valor"};
    let interrogacion: boolean = (5 > 3) ? true : false;
    
    console.log("Prueba de signos OK");
}

// Función para generar logs (simplificada)
const generarLog = (nombrePrueba: string, desarrollador: string) => {
    const ahora = new Date();
    const fecha = `${ahora.getDate()}-${ahora.getMonth()+1}-${ahora.getFullYear()}-${ahora.getHours()}:${ahora.getMinutes()}`;
    const nombreArchivo = `${nombrePrueba}-${desarrollador}-${fecha}.txt`;
    
    console.log(`Log generado: ${nombreArchivo}`);
    return nombreArchivo;
}