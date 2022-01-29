jQuery(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});

function errorMessage(jqXhr) {
    html = '<ul style="list-style-type: none;">';
    if (jqXhr.status === 401){
        html += '<li>Authentication Error</li>';
    }else if (jqXhr.status === 403) {
        html += '<li>Access Denied</li>';
    }else if (jqXhr.status === 422) {
        if(typeof jqXhr.responseJSON != 'undefined'){
            if (typeof jqXhr.responseJSON.errors != 'undefined') {
                //Errors list
                $errors = jqXhr.responseJSON.errors;
                $.each($errors, function (key, value) {
                    html += '<li>' + value[0] + '</li>';
                });
            }else if (typeof jqXhr.responseJSON.message != 'undefined') {
                //Message
                html += '<li>' + jqXhr.responseJSON.message + '</li>';
            }
        }else{
            html += '<li>Validation error</li>';
        }
    }else{
        if(typeof jqXhr.responseJSON != 'undefined'){
            if (typeof jqXhr.responseJSON.message != 'undefined') {
                //Message
                html += '<li>' + jqXhr.responseJSON.message + '</li>';
            }
        }else{
            html += '<li>Internal server error</li>';
        }
    }
    html += '</ul>';
    return html;
}

function errorTitle(jqXhr) {
    var err = 'Something went wrong';

    if(jqXhr.status == 422){
        err = 'The given data was invalid';
    }

    return err;
}

function swalError(jqXhr) {
    swal({
        title: errorTitle(jqXhr),
        text: errorMessage(jqXhr),
        html: true,
        type: 'error'
    });
}

$(document).ready(function () {
    $('body').on('click', '.sign_out_btn', function (e) {
        e.preventDefault();
        Swal.fire({
            title: 'Do you want to sign out?',
            showCancelButton: true,
            confirmButtonText: 'Yes',
        }).then((result) => {
            if (result.isConfirmed) {
                window.location.replace('/logout');
            }
        })
    });

    $('body').on('click', '.delete-btn', function (e) {
        e.preventDefault();
        let $this = $(this);
        Swal.fire({
            title: 'Do you want to sign out?',
            icon: "info",
            showCancelButton: true,
            confirmButtonText: 'Yes',
        }).then((result) => {
            if (result.isConfirmed) {
                $.ajax({
                    type: "DELETE",
                    url: 'delete/'+$this.data('model_id'),
                    success: function (response) {
                        $('.dataTable').DataTable().draw(false);
                    },
                    error : function (jqXHR) {
                        swalError(jqXhr)
                    }
                });
            }
        })
    });

});