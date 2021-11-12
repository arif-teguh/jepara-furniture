$(document).ready(function() {
    $('.minus-counter').click(function () {
        var $input = $(this).parent().find('.input-counter');
        var count = parseInt($input.val()) - 1;
        count = count < 1 ? 1 : count;
        $input.val(count);
        $input.change();
        return false;
    });
    $('.plus-counter').click(function () {
        var $input = $(this).parent().find('.input-counter');
        $input.val(parseInt($input.val()) + 1);
        $input.change();
        return false;
    });
});
console.log($(this))