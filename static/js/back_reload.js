$(function () //当网页回退时自动刷新一次
{
    window.onpageshow = function (event) {
        if (event.persisted) {
            window.location.reload();
        }
    }
});