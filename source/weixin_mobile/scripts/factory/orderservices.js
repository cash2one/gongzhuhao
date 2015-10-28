'use strict';

angular.module('zenmezApp')
  .factory("Order", function($http) {
    var serviceBase = '/mobile/merchant/orders/add/0/'
    var order = {};
    order.getOrders = function() {
      return $http.get(serviceBase);
    };

    order.getOrder = function(orderID) {
      return $http.get(serviceBase  + orderID);
    };

    order.insertOrder = function(order) {
      return $http.post(serviceBase  + order.schedule_category_id , order);
    };

    order.updateOrder = function(id, order) {
      return $http.post(serviceBase , {
        id: id,
        order: order
      }).then(function(status) {
        return status.data;
      });
    };

    order.deleteOrder = function(id) {
      return $http.delete(serviceBase + '?id=' + id).then(function(status) {
        return status.data;
      });
    };

    return order;
  });