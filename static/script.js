const socket = io();  

$(document).ready(function () {  
    $('#download-form').submit(function (e) {  
        e.preventDefault();  
        
        const link = $('#url').val();  
        const formato = $('#formato').val();  
        const pasta = $('#pasta').val();  
        
        socket.emit('start_download', { link: link, formato: formato, pasta: pasta });  
        
        $('#output').text('Iniciando download...');  
    });  
});  

socket.on('download_status', function (msg) {  
    $('#output').append(msg.data + '\n');  
});  

socket.on('download_completed', function (msg) {  
    $('#output').append(msg.data + '\n');  
    alert(msg.data); // Aviso de sucesso  
});  

socket.on('download_failed', function (msg) {  
    $('#output').append(msg.data + '\n');  
    alert(msg.data); // Aviso de falha  
});  