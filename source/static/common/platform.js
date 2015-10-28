(function(window, document) {

  function getParameterByName(name) {
    name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
    results = regex.exec(location.search);
    return results === null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
  }

  window._rAF = (function() {
    return window.requestAnimationFrame       ||
           window.webkitRequestAnimationFrame ||
           window.mozRequestAnimationFrame    ||
           function(callback) {
             window.setTimeout(callback, 16);
           };
  })();

  var cancelAnimationFrame = window.cancelAnimationFrame ||
    window.webkitCancelAnimationFrame ||
    window.mozCancelAnimationFrame ||
    window.webkitCancelRequestAnimationFrame;

  var IOS = 'ios';
  var ANDROID = 'android';
  var WINDOWS_PHONE = 'windowsphone';
  var requestAnimationFrame = window._rAF;

  var self = window.Platform = {

    // Put navigator on platform so it can be mocked and set
    // the browser does not allow window.navigator to be set
    navigator: window.navigator,

    /**
     * @ngdoc property
     * @name ionic.Platform#isReady
     * @returns {boolean} Whether the device is ready.
     */
    isReady: false,
    /**
     * @ngdoc property
     * @name ionic.Platform#isFullScreen
     * @returns {boolean} Whether the device is fullscreen.
     */
    isFullScreen: false,
    /**
     * @ngdoc property
     * @name ionic.Platform#platforms
     * @returns {Array(string)} An array of all platforms found.
     */
    platforms: null,
    /**
     * @ngdoc property
     * @name ionic.Platform#grade
     * @returns {string} What grade the current platform is.
     */
    grade: null,
    ua: navigator.userAgent,

    /**
     * @private
     */
    detect: function() {
      self._checkPlatforms();

      requestAnimationFrame(function() {
        // only add to the body class if we got platform info
        for (var i = 0; i < self.platforms.length; i++) {
          document.body.classList.add('platform-' + self.platforms[i]);
        }
      });
    },

    /**
     * @ngdoc method
     * @name ionic.Platform#setGrade
     * @description Set the grade of the device: 'a', 'b', or 'c'. 'a' is the best
     * (most css features enabled), 'c' is the worst.  By default, sets the grade
     * depending on the current device.
     * @param {string} grade The new grade to set.
     */
    setGrade: function(grade) {
      var oldGrade = self.grade;
      self.grade = grade;
      requestAnimationFrame(function() {
        if (oldGrade) {
          document.body.classList.remove('grade-' + oldGrade);
        }
        document.body.classList.add('grade-' + grade);
      });
    },

    /**
     * @ngdoc method
     * @name ionic.Platform#device
     * @description Return the current device (given by cordova).
     * @returns {object} The device object.
     */
    device: function() {
      return window.device || {};
    },

    _checkPlatforms: function() {
      self.platforms = [];
      var grade = 'a';

      if (self.isWebView()) {
        self.platforms.push('webview');
        if(!(!window.cordova && !window.PhoneGap && !window.phonegap)) {
          self.platforms.push('cordova');
        } else if(!!window.forge) {
          self.platforms.push('trigger');
        }
      } else {
        self.platforms.push('browser');
      }
      if (self.isIPad()) self.platforms.push('ipad');

      var platform = self.platform();
      if (platform) {
        self.platforms.push(platform);

        var version = self.version();
        if (version) {
          var v = version.toString();
          if (v.indexOf('.') > 0) {
            v = v.replace('.', '_');
          } else {
            v += '_0';
          }
          self.platforms.push(platform + v.split('_')[0]);
          self.platforms.push(platform + v);

          if (self.isAndroid() && version < 4.4) {
            grade = (version < 4 ? 'c' : 'b');
          } else if (self.isWindowsPhone()) {
            grade = 'b';
          }
        }
      }

      self.setGrade(grade);
    },

    /**
     * @ngdoc method
     * @name ionic.Platform#isWebView
     * @returns {boolean} Check if we are running within a WebView (such as Cordova).
     */
    isWebView: function() {
      return !(!window.cordova && !window.PhoneGap && !window.phonegap && !window.forge);
    },
    /**
     * @ngdoc method
     * @name ionic.Platform#isIPad
     * @returns {boolean} Whether we are running on iPad.
     */
    isIPad: function() {
      if (/iPad/i.test(self.navigator.platform)) {
        return true;
      }
      return /iPad/i.test(self.ua);
    },
    /**
     * @ngdoc method
     * @name ionic.Platform#isIOS
     * @returns {boolean} Whether we are running on iOS.
     */
    isIOS: function() {
      return self.is(IOS);
    },
    /**
     * @ngdoc method
     * @name ionic.Platform#isAndroid
     * @returns {boolean} Whether we are running on Android.
     */
    isAndroid: function() {
      return self.is(ANDROID);
    },
    /**
     * @ngdoc method
     * @name ionic.Platform#isWindowsPhone
     * @returns {boolean} Whether we are running on Windows Phone.
     */
    isWindowsPhone: function() {
      return self.is(WINDOWS_PHONE);
    },

    /**
     * @ngdoc method
     * @name ionic.Platform#platform
     * @returns {string} The name of the current platform.
     */
    platform: function() {
      // singleton to get the platform name
      if (platformName === null) self.setPlatform(self.device().platform);
      return platformName;
    },

    /**
     * @private
     */
    setPlatform: function(n) {
      if (typeof n != 'undefined' && n !== null && n.length) {
        platformName = n.toLowerCase();
      } else if (getParameterByName('ionicplatform')) {
        platformName = getParameterByName('ionicplatform');
      } else if (self.ua.indexOf('Android') > 0) {
        platformName = ANDROID;
      } else if (/iPhone|iPad|iPod/.test(self.ua)) {
        platformName = IOS;
      } else if (self.ua.indexOf('Windows Phone') > -1) {
        platformName = WINDOWS_PHONE;
      } else {
        platformName = self.navigator.platform && navigator.platform.toLowerCase().split(' ')[0] || '';
      }
    },

    /**
     * @ngdoc method
     * @name ionic.Platform#version
     * @returns {number} The version of the current device platform.
     */
    version: function() {
      // singleton to get the platform version
      if (platformVersion === null) self.setVersion(self.device().version);
      return platformVersion;
    },

    /**
     * @private
     */
    setVersion: function(v) {
      if (typeof v != 'undefined' && v !== null) {
        v = v.split('.');
        v = parseFloat(v[0] + '.' + (v.length > 1 ? v[1] : 0));
        if (!isNaN(v)) {
          platformVersion = v;
          return;
        }
      }

      platformVersion = 0;

      // fallback to user-agent checking
      var pName = self.platform();
      var versionMatch = {
        'android': /Android (\d+).(\d+)?/,
        'ios': /OS (\d+)_(\d+)?/,
        'windowsphone': /Windows Phone (\d+).(\d+)?/
      };
      if (versionMatch[pName]) {
        v = self.ua.match(versionMatch[pName]);
        if (v &&  v.length > 2) {
          platformVersion = parseFloat(v[1] + '.' + v[2]);
        }
      }
    },

    // Check if the platform is the one detected by cordova
    is: function(type) {
      type = type.toLowerCase();
      // check if it has an array of platforms
      if (self.platforms) {
        for (var x = 0; x < self.platforms.length; x++) {
          if (self.platforms[x] === type) return true;
        }
      }
      // exact match
      var pName = self.platform();
      if (pName) {
        return pName === type.toLowerCase();
      }

      // A quick hack for to check userAgent
      return self.ua.toLowerCase().indexOf(type) >= 0;
    },


  };

  var platformName = null, // just the name, like iOS or Android
  platformVersion = null;// a float of the major and minor, like 7.1

})(this, document);
