$(document).ready(function () {
    var selects = $('select[multiple]');

    selects.each(function () {
        var select = $(this);
        var options = select.find('option');
        var div = $('<div />').addClass('selectMultiple');
        div.attr('style', 'display: inline-block; padding: 5px; margin: auto;');
        var active = $('<div />');
        var list = $('<ul />');
        var placeholder = select.data('placeholder');
        var span = $('<span />').text(placeholder).appendTo(active);

        options.each(function () {
            var text = $(this).text();
            if ($(this).prop('selected')) {
                active.append($('<a/>').html('<em>' + text + '</em><i></i>'));
                span.addClass('hide');
                select.find('option:contains(' + text + ')').prop('selected', true);
            } else {
                list.append($('<li/>').html(text));
            }
        });


        active.append($('<div />').addClass('arrow'));
        div.append(active).append(list);

        select.wrap(div);
    });

    $(document).on('click', '.selectMultiple ul li', function (e) {
        var select = $(this).parent().parent();
        var li = $(this);
        if (!select.hasClass('clicked')) {
            select.addClass('clicked');
            li.prev().addClass('beforeRemove');
            li.next().addClass('afterRemove');
            li.addClass('remove');
            var a = $('<a />').addClass('notShown').html('<em>' + li.text() + '</em><i></i>').hide().appendTo(select.children('div'));
            a.slideDown(100, function () {
                setTimeout(function () {
                    a.addClass('shown');
                    select.children('div').children('span').addClass('hide');
                    select.find('option:contains(' + li.text() + ')').prop('selected', true);
                }, 125);
            });
            setTimeout(function () {
                if (li.prev().is(':last-child')) {
                    li.prev().removeClass('beforeRemove');
                }
                if (li.next().is(':first-child')) {
                    li.next().removeClass('afterRemove');
                }
                setTimeout(function () {
                    li.prev().removeClass('beforeRemove');
                    li.next().removeClass('afterRemove');
                }, 50);

                li.slideUp(100, function () {
                    li.remove();
                    select.removeClass('clicked');
                });
            }, 150);
        }
    });

    $(document).on('click', '.selectMultiple > div a', function (e) {
        var select = $(this).parent().parent();
        var self = $(this);
        self.removeClass().addClass('remove');
        select.addClass('open');
        setTimeout(function () {
            self.addClass('disappear');
            setTimeout(function () {
                self.animate({
                    width: 0,
                    height: 0,
                    padding: 0,
                    margin: 0
                }, 75, function () {
                    var li = $('<li />').text(self.children('em').text()).addClass('notShown').appendTo(select.find('ul'));
                    li.slideDown(100, function () {
                        li.addClass('show');
                        setTimeout(function () {
                            select.find('option:contains(' + self.children('em').text() + ')').prop('selected', false);
                            if (!select.find('option:selected').length) {
                                select.children('div').children('span').removeClass('hide');
                            }
                            li.removeClass();
                        }, 100);
                    });
                    self.remove();
                })
            }, 75);
        }, 100);
    });

    $(document).on('click', '.selectMultiple > div .arrow, .selectMultiple > div span', function (e) {
        $(this).parent().parent().toggleClass('open');
    });
});