openerp.dih_interactive_reports = function(instance) {
    instance.web.dih_interactive_reports = instance.web.dih_interactive_reports || {};
    var QWeb = openerp.web.qweb,
    _t = instance.web._t,
    _lt = instance.web._lt;
    instance.web.views.add('balancesheet', 'instance.web.dih_interactive_reports.BalanceSheetView');
    instance.web.dih_interactive_reports.BalanceSheetView = instance.web.View.extend({

        template: "BalanceSheet",
        display_name : _lt('balancesheet'),
        view_type : 'balancesheet',
        searchable : false,

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
    });
};