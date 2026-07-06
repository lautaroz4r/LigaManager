import os

equipos = []

def limpiar_pantalla():
    # Detecta el sistema operativo y limpia la consola (Windows usa 'cls', Mac/Linux usan 'clear')
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_menu():
    limpiar_pantalla()
    print("=======================================")
    print("      🏆 LIGA MANAGER 2026 🏆        ")
    print("=======================================")
    print("1. Registrar equipo")
    print("2. Ver equipos registrados")
    print("3. Cargar resultado de partido")
    print("4. Ver tabla de posiciones")
    print("5. Ver estadísticas del torneo")
    print("6. Salir")
    print("=======================================")

def registrar_equipo():
    print("--- REGISTRAR NUEVO EQUIPO ---\n")
    nombre = input("Ingrese el nombre del equipo: ").strip()

    if nombre == "":
        print("\nError: el nombre del equipo no puede estar vacío.")
        return

    for equipo in equipos:
        if equipo["nombre"].lower() == nombre.lower():
            print("\n Error: ese equipo ya está registrado.")
            return

    equipo = {
        "nombre": nombre,
        "partidos_jugados": 0,
        "ganados": 0,
        "empatados": 0,
        "perdidos": 0,
        "goles_favor": 0,
        "goles_contra": 0,
        "diferencia_goles": 0,
        "puntos": 0
    }

    equipos.append(equipo)
    print(f"\n✅ Equipo '{nombre}' registrado correctamente.")

def ver_equipos():
    print("--- EQUIPOS REGISTRADOS ---\n")
    if len(equipos) == 0:
        print("⚠️ No hay equipos registrados aún.⚠️")
        return

    for i, equipo in enumerate(equipos, start=1):
        print(f"{i}. {equipo['nombre']}")

def cargar_resultado():
    print("--- CARGAR RESULTADO ---\n")
    print(" Función en desarrollo: cargar resultado de partido.")

def ver_tabla_posiciones():
    print("--- TABLA DE POSICIONES ---\n")
    print(" Función en desarrollo: tabla de posiciones.")

def ver_estadisticas():
    print("--- ESTADÍSTICAS DEL TORNEO ---\n")
    print(" Función en desarrollo: estadísticas del torneo.")

def main():
    opcion = ""

    while opcion != "6":
        mostrar_menu()
        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == "1":
            limpiar_pantalla()
            registrar_equipo()
            input("\nPresione Enter para volver al menú principal...")
            
        elif opcion == "2":
            limpiar_pantalla()
            ver_equipos()
            input("\nPresione Enter para volver al menú principal...")
            
        elif opcion == "3":
            limpiar_pantalla()
            cargar_resultado()
            input("\nPresione Enter para volver al menú principal...")
            
        elif opcion == "4":
            limpiar_pantalla()
            ver_tabla_posiciones()
            input("\nPresione Enter para volver al menú principal...")
            
        elif opcion == "5":
            limpiar_pantalla()
            ver_estadisticas()
            input("\nPresione Enter para volver al menú principal...")
            
        elif opcion == "6":
            limpiar_pantalla()
            print("=======================================")
            print("   Saliendo del sistema. ¡Hasta luego! ")
            print("=======================================")
            
        else:
            print("\n❌ Error: opción inválida. Intente nuevamente.")
            input("\nPresione Enter para continuar...")

if __name__ == "__main__":
    main()

