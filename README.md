# pysoundofinterrupts

[![PyPI version](https://badge.fury.io/py/pysoundofinterrupts.svg)](https://pypi.org/project/pysoundofinterrupts/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Sonifica y visualiza las interrupciones del kernel Linux leyendo `/proc/interrupts`: escucha el sistema como un estetoscopio o dibuja su actividad en tiempo real.

Basado en la idea de [Nicolás Wolovick](https://github.com/nwolovick): cada interrupción impulsa el altavoz en modo 1-bit PCM (estilo ZX-Spectrum). Si hay unas 100 interrupciones por segundo, oirás algo parecido a un tono de 100 Hz.

**Solo Linux** — el programa lee `/proc/interrupts`. En otros sistemas termina con un mensaje claro.

**Enlaces:** [PyPI](https://pypi.org/project/pysoundofinterrupts/) · [Repositorio](https://github.com/pablogventura/pysoundofinterrupts)

---

## Instalación

### Con pipx (recomendado)

Instala y ejecuta en un entorno aislado, sin tocar tu Python global:

```bash
pipx install pysoundofinterrupts
```

Quedan disponibles los comandos `interrupts-sound` (sonido) e `interrupts-plot` (gráfico).

Para instalar desde el código fuente (por ejemplo, en desarrollo):

```bash
pipx install .
```

### Con pip

```bash
pip install pysoundofinterrupts
```

Requisitos: **Python 3.8+**, Linux.

---

## Uso

| Comando           | Descripción                                      |
|-------------------|--------------------------------------------------|
| `interrupts-sound`| Escucha las interrupciones del kernel en tiempo real (audio). |
| `interrupts-plot` | Gráfico en tiempo real por tipo (LOC, RES, CAL, TLB). |

### Sonido en tiempo real

```bash
interrupts-sound
```

Pulsa Enter para salir. Para calibrar el nivel:

| Opción          | Variable de entorno      | Descripción                          |
|-----------------|--------------------------|--------------------------------------|
| `--subtractor`  | `INTERRUPTS_SUBTRACTOR`  | Resta un piso a la tasa (default 1000) |
| `--divider`     | `INTERRUPTS_DIVIDER`    | Divide la tasa (default 25)          |
| `--amplitude`   | `INTERRUPTS_AMPLITUDE`  | Volumen 0–1 (default 0.2)            |

Ejemplo:

```bash
interrupts-sound --subtractor 800 --divider 20
```

### Gráfico en tiempo real

```bash
interrupts-plot
```

Muestra interrupciones por tipo (LOC, RES, CAL, TLB). Opciones:

| Opción        | Variable de entorno         | Descripción                    |
|---------------|-----------------------------|--------------------------------|
| `--x-max`     | `INTERRUPTS_PLOT_X_MAX`     | Puntos en el eje X (default 100) |
| `--y-max`     | `INTERRUPTS_PLOT_Y_MAX`     | Límite del eje Y (default 5000)  |
| `--interval`   | `INTERRUPTS_PLOT_INTERVAL`  | Actualización en ms (default 50)  |

---

## Desarrollo y tests

Clonar el repo, crear un entorno y instalar en modo editable con extras de test:

```bash
git clone https://github.com/pablogventura/pysoundofinterrupts.git
cd pysoundofinterrupts
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[test]"
pytest tests/ -v
```

---

## Publicar en PyPI

Desde el directorio del proyecto, con [build](https://pypi.org/project/build/) y [twine](https://pypi.org/project/twine/) instalados:

```bash
pip install build twine
./scripts/publish_to_pypi.sh
```

La primera vez configura las credenciales de PyPI (token en `~/.pypirc` o variables `TWINE_USERNAME` y `TWINE_PASSWORD`). Ver [Twine: Configuration](https://twine.readthedocs.io/en/stable/#configuration).

---

## Problemas frecuentes

- **Sin audio:** Comprueba el dispositivo de salida por defecto. El programa usa el dispositivo por defecto del sistema o el primer dispositivo de salida disponible.
- **Solo en Linux:** En Windows o macOS el programa termina indicando que necesita Linux.
- **Permisos:** Leer `/proc/interrupts` no suele requerir root. Si falla, comprueba que exista: `ls /proc/interrupts`.

---

## Licencia

MIT. Ver [LICENSE](LICENSE) en el repositorio.
