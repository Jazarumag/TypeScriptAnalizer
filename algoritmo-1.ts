
// Codigo de prueba de Raul Laurido
// Declaración de Variables y Tipos
let edad: number = 25;
const nombre: string = "Ana";
var activo: boolean = true;
let precio: number = 10.50;

// Arreglo y Objeto (interfaz implícita)
let numeros: number[] = [1, 2, 3];
let usuario: { id: number; nombre: string } = { id: 1, nombre: "Pedro" };

// Expresiones Aritméticas y Asignaciones
let resultado: number = (edad + precio) * 2 - 5 / 2;
resultado += 1;

// Expresiones Booleanas y Lógicas
let esMayor: boolean = (edad > 18) && activo;
let esValido: boolean = (numeros.length !== 0) || !esMayor;

// Estructuras de Control
if (esMayor) { // Condición booleana
    console.log("Acceso permitido.");
} else {
    for (let i: number = 0; i < numeros.length; i++) {
        if (numeros[i] === 2) {
            console.log(`Número ${numeros[i]} encontrado.`);
            break; // Break en bucle
        }
    }
}

let opcion: number = 1;
switch (opcion) {
    case 1:
        console.log("Opción uno.");
        break;
    default:
        console.log("Opción no reconocida.");
}

// Declaración y Uso de Funciones
function sumar(a: number, b: number): number {
    return a + b; // Retorno compatible
}

const mostrarInfo = (dato: string | number): void => { // Unión de tipos, void
    if (typeof dato === "string") {
        console.log(`Cadena: ${dato.toUpperCase()}`);
    } else {
        console.log(`Número: ${dato * 10}`);
    }
};

// Clases y Objetos
class Producto {
    nombre: string;
    private _stock: number; // Propiedad privada

    constructor(nombre: string, stockInicial: number) {
        this.nombre = nombre;
        this._stock = stockInicial;
    }

    obtenerStock(): number {
        return this._stock;
    }

    vender(cantidad: number): void { // Método void
        if (this._stock >= cantidad) {
            this._stock -= cantidad;
        } else {
            console.log("Stock insuficiente.");
        }
    }
}

let miProducto = new Producto("Libro", 100);
miProducto.vender(5); // Llamada a método void
console.log(`Stock restante de ${miProducto.nombre}: ${miProducto.obtenerStock()}`); // Acceso a propiedades y métodos

