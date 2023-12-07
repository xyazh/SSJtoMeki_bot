$(document).ready(function () {
    var url_args = JSON.parse("{\"" + window.location.search.split("?")[1].replaceAll("=", "\":\"").replaceAll("&", "\",\"") + "\"}");
    var file_name = url_args.filename;
    var data = {__ROOT__:{}};
    $.ajax({
        url: "/api/data_manager/file",
        type: "post",
        data: JSON.stringify({file_name:file_name}),
        async: false,
        success: function (result) {
            data.__ROOT__ = result;
        },
        error: function (result) {

        }
    });
    layui.use('code', function () {
        $("#json_code").text(formatJsonForNotes(JSON.stringify(data.__ROOT__)));
        layui.code();
    });
    var $tree = $('#tree');
    $tree.html('<ul t="object"></ul>');
    var $root = $tree.find('ul');
    var createNode = function (key, value) {
        var $node = $('<li></li>');
        $node.append('<span class="key">' + key + '</span>');
        $node.append(': ');
        if (Array.isArray(value)) {
            $node.append('<span class="value">' + "[Array]" + '</span>');
        } else if (typeof value === 'object') {
            $node.append('<span class="value">' + "{Object}" + '</span>');
        } else {
            $node.append('<span class="value">' + value + '</span>');
        }
        $node.append('<span class="add">+</span>');
        $node.append('<span class="delete">-</span>');
        return $node;
    };
    var traverse = function (data, $parent) {
        for (var key in data) {
            var value = data[key];
            var $node = createNode(key, value);
            if (Array.isArray(value)) {
                $node.append('<ul t="array"></ul>');
                traverse(value, $node.find('ul'));
            } else if (typeof value === 'object') {
                $node.append('<ul t="object"></ul>');
                traverse(value, $node.find('ul'));
            }
            $parent.append($node);
        }
    };
    traverse(data, $root);
    var autoType = function (v) {
        if (/^-?\d+$/.test(v)) {
            return parseInt(v);
        } else if (/^(-?\d+)(\.\d+)?$/.test(v)) {
            return parseFloat(v);
        } else if (v === "null") {
            return null;
        } else if (v === "true") {
            return true;
        } else if (v === "false") {
            return false;
        } else {
            return v
        }
    }
    var reloadjson = function () {
        var json = {};
        var $root = $tree.children('ul');
        var traverse = function ($parent, obj, t) {
            $parent.children('li').each(function () {
                var $node = $(this);
                var key = $node.children('.key').text();
                var value = $node.children('.value').text();
                if ($node.children('ul').length > 0) {
                    var t1 = $node.children('ul').attr("t");
                    if (t1 == "array") {
                        obj[key] = [];
                        traverse($node.children('ul'), obj[key], "array");
                    } else {
                        obj[key] = {};
                        traverse($node.children('ul'), obj[key], "object");
                    }
                } else if (t == "object") {
                    obj[key] = autoType(value);
                } else {
                    obj.push(autoType(value));
                }
            });
        };
        traverse($root, json, "object");
        var jsonString = JSON.stringify(json.__ROOT__);
        $('#export-text').val(jsonString);
        $("#json_code").html(null);
        $("#json_code").attr("class", "layui-code");
        $("#json_code").text(formatJsonForNotes(jsonString));
        layui.use('code', function () {
            layui.code();
        });
    }
    $tree.on('click', '.add', function () {
        var $parent = $(this).parent();
        var t1 = $parent.children("ul").attr("t");
        var is_array = false;
        if (t1 == "array") {
            key = $parent.children("ul").children().length;
            var is_array = true;
        } else {
            var key = prompt('输入键(留空表示添加一个数组):');
            if (!key) {
                is_array = true;
                key = "0";
            }
        }
        var value = prompt('输入值:');
        if (value === null) {
            return;
        }
        var $node = createNode(key, value);
        if ($parent.is('ul')) {
            $parent.append($node);
        } else {
            if ($parent.children('ul').length === 0) {
                if (is_array) {
                    $parent.append('<ul t="array"></ul>');
                } else {
                    $parent.append('<ul t="object"></ul>');
                }
            }
            $parent.children('ul').append($node);
        }
        if (is_array) {
            $parent.children('.value').text("[Array]");
        } else {
            $parent.children('.value').text("{Object}");
        }
        reloadjson();
    });

    $tree.on('click', '.delete', function () {
        var $parent = $(this).parent();
        var $grandparent = $parent.parent();
        var $grandgrandparent = $grandparent.parent();
        $parent.remove();
        if ($grandparent.children().length === 0) {
            $grandparent.remove();
            $grandgrandparent.children('.value').text("null");
        } else if($grandparent.attr("t") === "array"){
            var i = 0;
            $grandparent.children("li").each(function () {
                var $node = $(this);
                $node.children(".key").text(i);
                i++;
            });
        }
        reloadjson();
    });

    $tree.on('click', '.value', function () {
        var $value = $(this);
        var value = $value.text();
        var newValue = prompt('输入新的值:', value);
        if (newValue === null) {
            return;
        }
        $value.text(newValue);
        var $parent = $value.parent();
        $parent.children('ul').remove();
        reloadjson();
    });
    $('#export-btn').on('click', reloadjson);
});
