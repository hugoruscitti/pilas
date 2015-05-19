function SimpleMap() {
  this.keys = [];
  this.values = [];
}

(function (proto) {

  proto.set = function (key, value) {
    var index = this.indexOfKey(key);
    if (index === -1) {
      this.keys.push(key);
      this.values.push(value);
    }
    else {
      this.values[index] = value;
    }
  };

  proto.get = function (key) {
    var index = this.indexOfKey(key);
    if (index !== -1) {
      return this.values[index];
    }
  };

  proto.unset = function (key) {
    var index = this.indexOfKey(key);
    if (index !== -1) {
      this.keys.splice(index, 1);
      return this.values.splice(index, 1)[0];
    }
  };

  proto.has = function (key) {
    return this.indexOfKey(key) !== -1;
  };

  proto.indexOfKey = function (key) {
    return this.keys.indexOf(key);
  };

  proto.indexOfValue = function (value) {
    return this.values.indexOf(value);
  };

  proto.size = function () {
    return this.keys.length;
  };

})(SimpleMap.prototype);

export default SimpleMap;
