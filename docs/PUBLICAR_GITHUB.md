# Publicar el proyecto en GitHub

## Situación encontrada

La carpeta `GemeloDigitalSCADA` está dentro de un repositorio cuyo directorio raíz es `repos`. En la revisión, los archivos de este proyecto estaban sin seguimiento. No se modificó el Git padre ni se creó un remoto.

Para tener un repositorio independiente, conviene copiar los archivos del proyecto a una carpeta fuera de ese repositorio padre, excluyendo `.venv`, cachés y datos generados. Otra opción es crear deliberadamente un repositorio anidado en esta carpeta; el Git padre no incorporará sus archivos como archivos ordinarios. Los siguientes comandos corresponden a un repositorio independiente y deben ejecutarse desde su raíz, nunca desde `repos`.

## Antes de publicar

- Ejecutar las pruebas indicadas en el README y revisar el contenido de `git status`.
- Incorporar la escena si se puede compartir; de lo contrario, mantener explícita su ausencia.
- Elegir licencia y atribuciones según titularidad del código y modelos. No se incluyó una licencia por defecto.
- No subir `.venv`, credenciales ni datasets sin autorización. `.gitignore` excluye el entorno local y los datos generados.

## Crear el repositorio local

Solo en la carpeta destinada a este proyecto, si aún no tiene su propio `.git`:

```powershell
git init -b main
git add .
git status --short
git diff --cached --stat
git commit -m "Organiza prototipo SCADA y documenta estado del proyecto"
```

Revisar la lista antes del commit. Debe incluir código, documentación y pruebas; no `.venv` ni datos de experimentos.

## Publicar

Crear en GitHub un repositorio vacío llamado `GemeloDigitalSCADA`, sin inicializarlo con otro README. Sustituir `TU_USUARIO` por la cuenta real:

```powershell
git remote add origin https://github.com/TU_USUARIO/GemeloDigitalSCADA.git
git push -u origin main
```

Descripción sugerida: `Prototipo académico SCADA en Python y CoppeliaSim para una faja transportadora; investigación en calidad y mantenimiento predictivo.`

La publicación y el primer resultado de GitHub Actions quedan pendientes de crear el repositorio remoto. El workflow no requiere credenciales de CoppeliaSim ni acceso a una planta.
