openerp.dih_accounting_manual_reconcile_reports = function(instance) {
    instance.web.dih_accounting_manual_reconcile_reports = instance.web.dih_accounting_manual_reconcile_reports || {};
    var QWeb = openerp.web.qweb;
    _t = instance.web._t;
    var self = this;
    instance.web.dih_accounting_manual_reconcile_reports.ListViewWithReconcile = instance.web.ListView.extend({

        init: function() {
            this._super.apply(this, arguments);
        },
        start: function() {
            var self = this;
            var tmp = this._super.apply(this, arguments);
            var defs = [];
            console.log('ONE');
            this.$el.parents().find('.oe_view_manager_buttons').append(QWeb.render("TempManualReconcileButton", {
                widget: this
            }));
            this.$el.parents().find('.oe_view_manager_buttons').append(QWeb.render("ManualReconcileButton", {
                widget: this
            }));
            this.$el.parent().prepend(QWeb.render("ReconcileHeaderValues", {
                widget: this
            }));
            self.compute_header_values();
            return $.when(tmp, defs);
        },

        compute_header_values: function(){
            var self = this;
            var model = new instance.web.Model('account.move');
            model.call("get_reconcile_display_values", {
                context: new instance.web.CompoundContext()
            }).then(function(result){
                self.$el.parent().find('.dih_reconcile_header_values').replaceWith(
                    "<div class=\"dih_reconcile_header_values\">" +
                    "<table>" +

                    "<tr><td>Previous end of month balance : </td><td>" + result["prev_eomb_balance"] + "</td></tr>" +
                    "<tr><td>Current end of month balance : </td><td>" + result["current_eomb_balance"] + "</td></tr>" +
                    "<tr><td>Difference between current and previous end of month balances : </td><td>" + result["difference_current_last_balances"] + "</td></tr>" +
                    "<tr><td>Reconciled : </td><td>" + result["this_month_reconciled"] + "</td></tr>" +
                    "<tr><td>Difference : </td><td>" + result["left_to_reconcile_this_month"] + "</td></tr>" +
                    "</table></div>"
                    );
            });
        },

        compute_aggregates: function (records) {
        var columns = _(this.aggregate_columns).filter(function (column) {
            return column['function']; });
        if (_.isEmpty(columns)) { return; }

        if (_.isEmpty(records)) {
            records = this.groups.get_records();
        }
        records = _(records).compact();

        var count = 0, sums = {};
        _(columns).each(function (column) {
            switch (column['function']) {
                case 'max':
                    sums[column.id] = -Infinity;
                    break;
                case 'min':
                    sums[column.id] = Infinity;
                    break;
                default:
                    sums[column.id] = 0;
            }
        });
        _(records).each(function (record) {
            count += record.count || 1;
            _(columns).each(function (column) {
                var field = column.id,
                    value = record.values[field];
                switch (column['function']) {
                    case 'sum':
                        sums[field] += value;
                        break;
                    case 'avg':
                        sums[field] += record.count * value;
                        break;
                    case 'min':
                        if (sums[field] > value) {
                            sums[field] = value;
                        }
                        break;
                    case 'max':
                        if (sums[field] < value) {
                            sums[field] = value;
                        }
                        break;
                }
            });
        });

        var aggregates = {};
        _(columns).each(function (column) {
            var field = column.id;
            switch (column['function']) {
                case 'avg':
                    aggregates[field] = {value: sums[field] / count};
                    break;
                default:
                    aggregates[field] = {value: sums[field]};
            }
        });

        this.display_aggregates(aggregates);
        this.compute_header_values();
        },

        load_list: function() {
            this._super.apply(this, arguments);
            if (this.$buttons) {
                this.$el.parents().find('.dih_reconcile_button').off().click(this.proxy(function (event) {
                    event.stopPropagation();
                    var action = {
                        type: 'ir.actions.act_window',
                        res_model: 'dih.confirm.reconciles.temp.screen.wizard',
                        views: [[false, 'form']],
                        target: 'new',
                    };
                    this.do_action(action);
                }));

                this.$el.parents().find('.dih_temp_reconcile_button').off().click(this.proxy(function (event) {
                    event.stopPropagation();
                    var action2 = {
                        type: 'ir.actions.act_window',
                        res_model: 'dih.temp.reconcile.report.temp.screen.wizard',
                        views: [[false, 'form']],
                        target: 'new',
                    };
                    this.do_action(action2);
                }));

            }
        },

        do_the_job: function(event) {
            
            var self = this
            var model = new instance.web.Model('account.move');
            model.call("get_confirm_reconciles_confirm_screen", {
                context: new instance.web.CompoundContext()
            });
        },


        reload_content: function () {
            var self = this;
            self.compute_header_values();
            this._super.apply(this, arguments);
        },
    });
    instance.web.views.add('dih_reconcile_tree_with_header', 'instance.web.dih_accounting_manual_reconcile_reports.ListViewWithReconcile');

    instance.web.dih_accounting_manual_reconcile_reports.PNLView = instance.web.View.extend({
        template: "PNLView",
        display_name: _lt('pnlview'),
        default_nr_columns: 3,
        view_type: "pnlview",
        searchable: false,
        init: function (parent, dataset, view_id, options) {
            this._super(parent, dataset, view_id, options);
            var self = this;
            this.fields_view = {};
            this.fields_keys = [];
            this.qweb = new QWeb2.Engine();
            this.qweb.debug = instance.session.debug;
            this.qweb.default_dict = _.clone(QWeb.default_dict);
            this.has_been_loaded = $.Deferred();
            this.currently_dragging = {};
            this.limit = options.limit || 40;
            this.add_group_mutex = new $.Mutex();
        },
        view_loading: function(r) {
            return this.load_pnlview(r);
        },
        load_pnlview: function(data) {
            this.fields_view = data;

            // use default order if defined in xml description
            var default_order = this.fields_view.arch.attrs.default_order,
                unsorted = !this.dataset._sort.length;
            if (unsorted && default_order) {
                this.dataset.set_sort(default_order.split(','));
            }

            this.$el.addClass(this.fields_view.arch.attrs['class']);
            this.$buttons = $(QWeb.render("DummyView.buttons", {'widget': this}));
            this.$cont = data.arch.children;

            if (this.options.$buttons) {
                this.$buttons.appendTo(this.options.$buttons);
            } else {
                this.$el.find('.oe_dummyview_buttons').replaceWith(this.$buttons);
            }
            this.$el.find('.oe_dummyview_content').append(this.$cont);
            this.$groups = this.$el.find('.oe_dummyview_groups tr');
            this.fields_keys = _.keys(this.fields_view.fields);
            this.add_qweb_template();
            
            this.$cont=this.qweb.render('dummy-content', this.qweb_context);
            this.$el.find('.oe_dummyview_content').replaceWith(this.$cont);
            

            this.has_been_loaded.resolve();
            this.trigger('dummyview_view_loaded', data);
            return $.when();
        },
    });
    instance.web.views.add('dih_reconcile_tree_with_header', 'instance.web.dih_accounting_manual_reconcile_reports.PNLView');
};