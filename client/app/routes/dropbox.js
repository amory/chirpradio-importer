App.DropboxRoute = Em.Route.extend({
  model: function() {
    
    // periodic import
    return Em.$.getJSON('/scan_dropbox');
  },
  beforeModel: function(transition) {
    
    // set loading status to true before data is ready
    this.controllerFor('dropbox').set('working', true);

  },
  afterModel: function() {
  
    // set loading status to false after data is ready
    this.controllerFor('dropbox').set('working', false);

  },
  setupController: function(controller, model) {
     
    var self = this;
       
    // load whitelist
    Em.$.getJSON('/whitelist', function(response) {
      self.controllerFor('whitelist').set('model', response);
      self.controllerFor('application').set('showWhitelist', true);
    });

    // no albums in dropbox
    if (model.length === 0) {
      controller.set('working', null);
    }

    controller.set('model', model);
  }
});
