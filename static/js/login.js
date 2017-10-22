$(document).ready(function(){

    $('#signin').click(function(){
        window.location.href = "/signin/"
    });

    function showError(error){
        $('#error').html(error)
    }

    $('#submit').click(function(){
        var login = $('#login').val(),
            password = $('#password').val();
        console.log('Login:' + login + ' | Password:' + password);
        if(login && password){
            $.post({
                url: '/login/',
                data: {'login': login, 'password': password},
                success: function(data) {
                    if (data.error){
                        showError(data.error)
                    }else{
                        if (data.result){
                            window.location.href = data.redirect;
                        }
                    }
                },
                dataType:'json'});
            return false;
        }else{
            showError('Please fill all fields')
        }
    });
});
