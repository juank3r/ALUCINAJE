Instrucciones para revisar y subir a `ALUCINAJE` remoto

1. Revisar archivos creados en `ALUCINAJE/`.
2. Inicializar repo local o añadir cambios en tu repo existente:

```bash
cd path/to/ALUCINAJE
git init  # si no existe
git add .
git commit -m "Add methodology and safe corpus generator"
git remote add origin git@github.com:juank3r/ALUCINAJE.git
git push -u origin main
```

Si usas HTTPS, reemplaza la URL remota por la adecuada. Si ya existe el repo local, crea una rama y abre un PR.
