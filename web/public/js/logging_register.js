const logging_layer = function () {
    layer.open({
        type: 1,
        resize: false,
        shadeClose: true,
        area: '350px',
        title: '登录',
        content: template("logging_layer_temp", {}),
        success: function (layero, index) {
            layero.find('.layui-layer-content').css('overflow', 'visible');
            layui.form.render().on('submit(logging_b)', function (data) {
                var r_data = JSON.stringify(data.field);
                $.ajax({
                    url: "/api/logging",
                    type: "post",
                    data: r_data,
                    async: false,
                    success: function (result) {
                        var l_data = JSON.parse(result)
                        $.cookie("token", l_data["token"], {});
                        $.cookie("uid", l_data["uid"], {});
                        $.cookie("user_name", l_data["user_name"], {});
                        $.cookie("level", l_data["level"], {});
                        c_token = l_data["token"];
                        c_uid = l_data["uid"];
                        c_user_name = l_data["user_name"];
                        c_level = l_data["level"];
                        $("#user_name").text(l_data["user_name"]);
                        $("#uid").text(l_data["uid"]);
                        $("#logging1").attr("style", "display: none;");
                        $("#logging2").attr("style", "display: none;");
                        $("#register1").attr("style", "display: none;");
                        $("#register2").attr("style", "display: none;");
                        layer.close(index);
                    },
                    error: function (xhr, status, error) {
                        var m = "错误"
                        switch (xhr.status) {
                            case 400:
                                m = "数据字段错误，必填项不能为空";
                                break;
                            case 404:
                                m = "用户不存在";
                                break;
                            case 401:
                                m = "密码错误";
                                break;
                        }
                        layer.msg(m, { icon: 0 });
                    }
                });
            });
        }
    });
}