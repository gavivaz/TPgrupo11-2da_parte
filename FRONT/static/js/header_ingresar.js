//Contenido del encabezado
let headerContent = `
<header id="header">
    <div>
            // <a href="http://127.0.0.1:5001/">
            <a href="https://com24167.pythonanywhere.com/">
    <img id="logo-header" src="static/img/logo.jpg" alt="logo">
</a>

    </div>

    <p id="nombre-web">Ratón Gamer</p>
    <p id="app-admin">App Admin</p>

    <nav class="menu">
            <a class="hipervinc-header" href="../tabla_usuarios.html">Tabla usuarios</a>
    </nav>
</header>
`


//Agregar el contenido del encabezado al principio del body
document.body.insertAdjacentHTML(`afterbegin`, headerContent);