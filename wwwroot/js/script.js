// wwwroot/js/script.js  

document.addEventListener("DOMContentLoaded", function () {  
    const downloadButton = document.querySelector("button[type='submit']");  
    
    if (downloadButton) {  
        downloadButton.addEventListener("click", function () {  
            downloadButton.innerHTML = "Baixando...";  
            downloadButton.disabled = true; // desabilita o botão enquanto faz o download  

            // Uma breve animação / feedback enquanto está aguardando a solicitação  
            setTimeout(() => {  
                downloadButton.innerHTML = "Fazer Download";  
                downloadButton.disabled = false; // reabilita o botão após o tempo  
            }, 2000); // espere 2 segundos (para simular o tempo de download)  
        });  
    }  
});