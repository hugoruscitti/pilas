export function initialize(container, application) {
  application.inject('component:img-wrap', 'manager', 'service:img-manager');
  application.inject('view', 'imgManagerService', 'service:img-manager');
}

export default {
  name:       'img-manager-service',
  initialize: initialize
};
