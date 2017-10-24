$(document).ready(function(){

    function showError(error){
        $('#error').html(error)
    }

    $('#submit_create').click(function(){
        var name = $('#name').val();
        if(name){
            $.post({
                url: '/admin/',
                data: {'name': name},
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
