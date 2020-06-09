const botonesBorrar = document.querySelectorAll('.btn-delete') /*obtiene una lista de nodos html con los botones */

if (botonesBorrar) {
    const listaBotones = Array.from(botonesBorrar)   /*trnsforma la lista de nodos en un array para poder recorrerlo*/ 
    listaBotones.forEach((boton) =>{        /*recorre los botones*/
        boton.addEventListener('click', (eventoClick)=>{  /*añade un evento click a cada boton*/ 
            if(!confirm('Estas seguro de eliminar el registro?')){  /*saca una ventana de confirmación */
                eventoClick.preventDefault();   /*en caso de darle a cancelar -> cancela el evento y no ejecuta la peticion DELETE al servidor */
            }
        });
    });
}