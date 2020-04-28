$(document).ready(function () {
    // tab切换
    function changeTab(index) {
        $(".tab>.tab-item.active").removeClass("active");
        $(".content-list>.content.active").removeClass("active");
        $(".tab>.tab-item").eq(index).addClass("active");
        $(".content-list>.content").eq(index).addClass("active")
    }

    // 删除
    function deleteTab(index) {
        console.log($(".tab>.tab-item").eq(index).hasClass('active'));
        if ($(".tab>.tab-item").eq(index).hasClass('active')) {
            $(".tab>.tab-item").eq(index).remove();
            $(".content-list>.content").eq(index).remove();
            $(".tab>.tab-item:last-child").addClass("active");
            $(".content-list>.content:last-child").addClass("active")
        } else {
            $(".tab>.tab-item").eq(index).remove();
            $(".content-list>.content").eq(index).remove()
        }
    }

    // tab切换
    $('.tab').on('click', '.tab-item .title', function () {
        var index = $(this).parent('.tab-item').index();
        changeTab(index)
    });
    // 删除
    $('.tab').on('click', '.tab-item .js-close', function () {
        console.log(ws_list);
        var index = $(this).parent('.tab-item').index();
        // 断开ws连接
        for (let i = 0; i < ws_list.length; i++) {
            if (i === index) {
                try {
                    let sc = ws_list[i].sc;
                    ws_list.splice(i, i + 1);
                    sc.close();
                } catch (e) {
                    console.log("ws关闭失败");
                }
            }
        }
        deleteTab(index);
        layer.closeAll()
    })
});