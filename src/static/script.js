$(document).ready(function() {
    $('form').on('submit', function(event) {
        $.ajax({
            data: {
                search_term: $('search_term').val()
            },
            type: 'POST',
            url: '/results'
        })
    });
});