const getManagerPage = function (obj) {
    var id = $(obj).attr("id");
    $.ajax({
        url: "/res/" + id + ".html?t=1",
        type: "get",
        success: function (result) {
            $("#" + id + "_page").html(result)
        },
        error: function (xhr, status, error) {
            $("#" + id + "_page").html("身份验证失败，可能是你没有权限或登录信息失效")
        }
    });
}