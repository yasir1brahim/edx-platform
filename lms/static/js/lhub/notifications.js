(function(define) {
    'use strict';
    define(['jquery',
        'underscore',
        'backbone',
        'moment',
        'text!templates/lhub/notification_block.underscore'],
        function($, _, Backbone, moment, notificationTemplate) {
            return function(mainOptions) {
                var LhubNotifications = Backbone.View.extend({
                    el: '.js-notifications',
                    template: _.template(notificationTemplate),
                    events: {
                        'click .js-mark-read': 'markRead',
                    },

                    initialize: function(options) {
                        var that = this;
                        this.url = options.url;
                        this.page = 1;
                        this.numPages = 1;
                        this.newCount = null;
                        this.blockShowNewCount = $('.js-new-notifications-count');
                        this.isOpen = false;
                        this.fetchData();

                        $('.js-user-notifications').on('click', this.slideToggle.bind(this));
                        $('.js-wrap-block-notifications').on('scroll', this.scroll.bind(this));
                        $('body').on('click', function(){
                            that.close();
                        });
                        $('.js-notifications').on('click', function(ev) {
                            ev.stopPropagation();
                        });

                        window.addEventListener('beforeunload', function() {
                            $('.js-user-notifications').off('click');
                            $('.js-block-notifications').off('scroll');
                            that.remove();
                        });
                    },

                    slideToggle: function(ev) {
                        ev.preventDefault();
                        ev.stopPropagation();
                        if (this.isOpen) {
                            this.close();
                        } else {
                            this.open();
                        }
                    },

                    open: function() {
                        this.isOpen = true;
                        this.fetchData();
                        this.$el.slideDown();
                    },

                    close: function() {
                        this.$el.slideUp();
                        this.page = 1;
                        this.numPages = 1
                        this.$('.js-block-notifications').empty();
                        this.isOpen = false;
                    },

                    fetchData: function() {
                        var that = this;
                        if (this.numPages >= this.page && !this.$('.loading').length) {
                            this.$('.js-block-notifications').append(
                              "<div class='loading'><i class='fa fa-spinner fa-spin fa-fw'></i></div>"
                            );

                            $.ajax({
                                url: this.url,
                                contentType: 'application/json',
                                dataType: 'json',
                                type: 'GET',
                                data: {page: this.page}
                            }).done(function(data) {
                                if (that.page === 1) {
                                    that.newCount = (data.results.length) ? data.results[0].num_new_notifications : 0;
                                    that.renderNewNotificationsCount();
                                }

                                if (that.isOpen) {
                                    that.renderNotifications(data.results);
                                    that.page += 1;
                                    that.numPages = data.num_pages;
                                }
                            }).always(function() {
                                that.$('.loading').remove();
                            });
                        }

                    },

                    renderNotifications: function(notifications) {
                        _.map(notifications, function (n) {
                            n.created = moment(n.created).format('L');
                        })
                        this.$('.js-block-notifications').append(
                          this.template({notifications: notifications})
                        );
                    },

                    renderNewNotificationsCount: function() {
                        this.blockShowNewCount.text(this.newCount || '');
                        if (this.newCount) {
                            this.blockShowNewCount.removeClass('hidden');
                        } else {
                            this.blockShowNewCount.addClass('hidden');
                        }
                    },

                    scroll: function (ev) {
                        var $ev = $(ev.currentTarget);
                        if ($ev.scrollTop() + $ev.height() >= this.$('.js-block-notifications').height()) {
                            this.fetchData();
                        }
                    },

                    markRead: function (ev) {
                        var $ev = $(ev.currentTarget);
                        var notificationID = $ev.data('id');
                        $.ajax({
                            url: `${this.url}${notificationID}/`,
                            type: 'PUT',
                            data: {is_read: true}
                        });
                    },
                });

                return new LhubNotifications(mainOptions);
            };
        });
}).call(this, define || RequireJS.define);
