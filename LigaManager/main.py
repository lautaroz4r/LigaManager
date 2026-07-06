import os
import json

ARCHIVO_DATOS = "datos_liga.json"

equipos = []
partidos = []


def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")


def pausar():
    input("\nPresione Enter para volver al menú principal...")


def guardar_datos():
    datos = {
        "equipos": equipos,
        "partidos": partidos
    }

    with open(ARCHIVO_DATOS, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)


def cargar_datos():
    global equipos, partidos

    try:
        with open(ARCHIVO_DATOS, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
            equipos = datos.get("equipos", [])
            partidos = datos.get("partidos", [])
    except FileNotFoundError:
        equipos = []
        partidos = []


def mostrar_menu():
    limpiar_pantalla()
    print("=======================================")
    print("      🏆 LIGA MANAGER 2026 🏆")
    print("=======================================")
    print("1. Registrar equipo")
    print("2. Ver equipos registrados")
    print("3. Cargar resultado de partido")
    print("4. Ver tabla de posiciones")
    print("5. Ver estadísticas del torneo")
    print("6. Ver historial de partidos")
    print("7. Salir")
    print("=======================================")


def buscar_equipo(nombre):
    for equipo in equipos:
        if equipo["nombre"].lower() == nombre.lower():
            return equipo
    return None


def registrar_equipo():
    print("--- REGISTRAR NUEVO EQUIPO ---\n")
    nombre = input("Ingrese el nombre del equipo: ").strip()

    if nombre == "":
        print("\nError: el nombre del equipo no puede estar vacío.")
        return

    if buscar_equipo(nombre) is not None:
        print("\nError: ese equipo ya está registrado.")
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
    guardar_datos()
    print(f"\nEquipo '{nombre}' registrado correctamente.")


def ver_equipos():
    print("--- EQUIPOS REGISTRADOS ---\n")

    if len(equipos) == 0:
        print("No hay equipos registrados aún.")
        return

    for i, equipo in enumerate(equipos, start=1):
        print(f"{i}. {equipo['nombre']}")


def pedir_goles(mensaje):
    while True:
        try:
            goles = int(input(mensaje))

            if goles < 0:
                print("Error: los goles no pueden ser negativos.")
            else:
                return goles

        except ValueError:
            print("Error: debe ingresar un número entero.")


def cargar_resultado():
    print("--- CARGAR RESULTADO ---\n")

    if len(equipos) < 2:
        print("Debe haber al menos 2 equipos registrados para cargar un partido.")
        return

    ver_equipos()

    nombre_local = input("\nIngrese el nombre del equipo local: ").strip()
    nombre_visitante = input("Ingrese el nombre del equipo visitante: ").strip()

    equipo_local = buscar_equipo(nombre_local)
    equipo_visitante = buscar_equipo(nombre_visitante)

    if equipo_local is None or equipo_visitante is None:
        print("\nError: uno o ambos equipos no están registrados.")
        return

    if equipo_local["nombre"].lower() == equipo_visitante["nombre"].lower():
        print("\nError: un equipo no puede jugar contra sí mismo.")
        return

    goles_local = pedir_goles(f"Goles de {equipo_local['nombre']}: ")
    goles_visitante = pedir_goles(f"Goles de {equipo_visitante['nombre']}: ")

    equipo_local["partidos_jugados"] += 1
    equipo_visitante["partidos_jugados"] += 1

    equipo_local["goles_favor"] += goles_local
    equipo_local["goles_contra"] += goles_visitante

    equipo_visitante["goles_favor"] += goles_visitante
    equipo_visitante["goles_contra"] += goles_local

    if goles_local > goles_visitante:
        equipo_local["ganados"] += 1
        equipo_local["puntos"] += 3

        equipo_visitante["perdidos"] += 1

    elif goles_local < goles_visitante:
        equipo_visitante["ganados"] += 1
        equipo_visitante["puntos"] += 3

        equipo_local["perdidos"] += 1

    else:
        equipo_local["empatados"] += 1
        equipo_visitante["empatados"] += 1

        equipo_local["puntos"] += 1
        equipo_visitante["puntos"] += 1

    equipo_local["diferencia_goles"] = equipo_local["goles_favor"] - equipo_local["goles_contra"]
    equipo_visitante["diferencia_goles"] = equipo_visitante["goles_favor"] - equipo_visitante["goles_contra"]

    partido = {
        "local": equipo_local["nombre"],
        "visitante": equipo_visitante["nombre"],
        "goles_local": goles_local,
        "goles_visitante": goles_visitante
    }

    partidos.append(partido)
    guardar_datos()

    print("\nResultado cargado correctamente.")


def ver_tabla_posiciones():
    print("--- TABLA DE POSICIONES ---\n")

    if len(equipos) == 0:
        print("No hay equipos registrados aún.")
        return

    tabla = sorted(
        equipos,
        key=lambda equipo: (
            equipo["puntos"],
            equipo["diferencia_goles"],
            equipo["goles_favor"]
        ),
        reverse=True
    )

    print(f"{'Pos':<5}{'Equipo':<20}{'PJ':<5}{'G':<5}{'E':<5}{'P':<5}{'GF':<5}{'GC':<5}{'DG':<5}{'Pts':<5}")
    print("-" * 70)

    for i, equipo in enumerate(tabla, start=1):
        print(
            f"{i:<5}"
            f"{equipo['nombre']:<20}"
            f"{equipo['partidos_jugados']:<5}"
            f"{equipo['ganados']:<5}"
            f"{equipo['empatados']:<5}"
            f"{equipo['perdidos']:<5}"
            f"{equipo['goles_favor']:<5}"
            f"{equipo['goles_contra']:<5}"
            f"{equipo['diferencia_goles']:<5}"
            f"{equipo['puntos']:<5}"
        )


def ver_estadisticas():
    print("--- ESTADÍSTICAS DEL TORNEO ---\n")

    if len(equipos) == 0:
        print("No hay equipos registrados aún.")
        return

    total_partidos = len(partidos)
    total_goles = sum(equipo["goles_favor"] for equipo in equipos)

    mejor_equipo = max(equipos, key=lambda equipo: equipo["puntos"])
    mas_goles = max(equipos, key=lambda equipo: equipo["goles_favor"])
    menos_goles_contra = min(equipos, key=lambda equipo: equipo["goles_contra"])

    print(f"Total de equipos registrados: {len(equipos)}")
    print(f"Total de partidos jugados: {total_partidos}")
    print(f"Total de goles convertidos: {total_goles}")

    if total_partidos > 0:
        promedio = total_goles / total_partidos
        print(f"Promedio de goles por partido: {promedio:.2f}")
    else:
        print("Promedio de goles por partido: 0")

    print(f"\nEquipo con más puntos: {mejor_equipo['nombre']} ({mejor_equipo['puntos']} pts)")
    print(f"Equipo con más goles a favor: {mas_goles['nombre']} ({mas_goles['goles_favor']} goles)")
    print(f"Equipo con menos goles en contra: {menos_goles_contra['nombre']} ({menos_goles_contra['goles_contra']} goles)")


def ver_historial_partidos():
    print("--- HISTORIAL DE PARTIDOS ---\n")

    if len(partidos) == 0:
        print("No hay partidos cargados aún.")
        return

    for i, partido in enumerate(partidos, start=1):
        print(
            f"{i}. {partido['local']} {partido['goles_local']} - "
            f"{partido['goles_visitante']} {partido['visitante']}"
        )


def main():
    cargar_datos()

    opcion = ""

    while opcion != "7":
        mostrar_menu()
        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == "1":
            limpiar_pantalla()
            registrar_equipo()
            pausar()

        elif opcion == "2":
            limpiar_pantalla()
            ver_equipos()
            pausar()

        elif opcion == "3":
            limpiar_pantalla()
            cargar_resultado()
            pausar()

        elif opcion == "4":
            limpiar_pantalla()
            ver_tabla_posiciones()
            pausar()

        elif opcion == "5":
            limpiar_pantalla()
            ver_estadisticas()
            pausar()

        elif opcion == "6":
            limpiar_pantalla()
            ver_historial_partidos()
            pausar()

        elif opcion == "7":
            limpiar_pantalla()
            print("=======================================")
            print("   Saliendo del sistema. ¡Hasta luego!")
            print("=======================================")

        else:
            print("\nError: opción inválida. Intente nuevamente.")
            pausar()


if __name__ == "__main__":
    main()

