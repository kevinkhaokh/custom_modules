/*

openerp.project = function (instance){       

  var self = this;
  openerp.web.ListView.include({       

    load_list: function(data) {
     if (this.$buttons) {               

      this.$buttons.find('.oe_new_button').click(this.proxy('do_the_job')) ;
    }       

  },       

  do_the_job: function () {

  	        instance.web.Model('account.move')
            .call('confirm_reconciles', [[]]);
    
 } });
}

*/

/*
openerp.dih_test_js = function(instance) {
    var _t = instance.web._t,
        QWeb = instance.web.qweb;

    instance.web.ListView.include({

        load_list: function(data) {
     if (this.$buttons) {               

      this.$buttons.find('.oe_new_button').click(this.proxy('do_the_job')) ;
    }       

  },    

  */
/*
  do_the_job: function () {

  	        instance.web.Model('account.move')
            .call('confirm_reconciles', [[]]);
    
 }   
*/
//    });

//};

openerp.dih_test_js = function(instance){

	var module = instance.dih_test_js = {};
  var QWeb = openerp.web.qweb;
  _t = instance.web._t;
  var self = this;

/*
	instance.web.dih_test_js.DihCustomView = instance.web.ListView.extend({
        init: function() {
            this._super.apply(this, arguments);
        },

        start:function(){
            var tmp = this._super.apply(this, arguments);
            var self = this;
            var defs = [];
            this.$el.parent().prepend(QWeb.render("ButtonWidget", {widget: this}));
            return $.when(tmp);
        },

	});
*/
/*
	var ButtonWidget = instance.web.Widget.extend({
	    template: 'ButtonWidget', //the name of the HTML template that will be used to display the widget
	    init: function(parent, label, action){
	        // the constructor. Widgets always have the parent widget as
	        // first constructor parameter
	    this._super(parent);
	        this.label = label || 'Button';
	        this.action = action || function(){};
          this.$el.parent().prepend(QWeb.render("ButtonWidget", {widget: this}));
	    },
	    start: function(){
	        // start() is called when the DOM has been rendered. This
	        // is where we can register callbacks. And we do just that
	        // by registering the provided action to the click event on
	        // the root DOM element of the widget (this.$el)
	        this.$el.click(this.action);

	    },
	});
*/
  openerp.web.ListView.include({
    load_list: function(data){
      this._super(data);
      if(this.$buttons){
        this.$buttons.find('.oe_new_button').off().click(this.proxy('do_the_job'));
      }
    },

    do_the_job: function(){
      var self = this;
      var model = new instance.web.Model("account.move");
      model.call("confirm_reconciles", {context: new instance.web.CompoundContext()});
      /*
      this.do_action({
        type:"ir.actions.act_window",
        name: "Custom create button",
        res_model:"project.project",
        views: "[[false, 'form']]",
        target: "current",
        view_type: "form",
        view_mode: "form",
      })
      return {
        'type': 'ir.actions.client',
      }
*/
    }
  })
};
