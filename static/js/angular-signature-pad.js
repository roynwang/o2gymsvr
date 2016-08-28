/*! angular-signature-pad - v0.0.3 - 14 giugno 2015
* Copyright (c) G. Tomaselli <girotomaselli@gmail.com> 2015; Licensed  
*/

angular.module('ByGiro.signaturePad',[])
.directive('signaturePad', ['$window','$parse','$compile', function ($window, $parse, $compile) {
	
	contrFunction = ['$scope', '$timeout', '$element', '$attrs', '$parse', function($scope, $timeout, $element, $attrs, $parse){
			var defaultOpts = {
				height: 220,
				width: 568,
				clearBtn: 'Cancel'
			},
			canvas,signaturePad;
			
			$scope.opts = angular.extend({},defaultOpts,$scope.opts);
			
			canvas = $element.find('canvas');
			signaturePad = new SignaturePad(canvas[0]);
			
			if ($scope.signature && !$scope.signature.$isEmpty && $scope.signature.dataUrl) {
			  signaturePad.fromDataURL($scope.signature.dataUrl);
			}
			
			canvas.on('mouseup',function(){				
				$scope.dataVal = !signaturePad.isEmpty() ? signaturePad.toDataURL() : '';
				setModel($scope.dataVal);
			});
			
			$scope.clear = function () {
				signaturePad.clear();
				$scope.dataVal = '';
				setModel();
			};
			
			function setModel(v){
				$scope.ngModel = v
			}
			
		}];
	
	return({
		scope: {
			opts: "=signaturePadOptions",
			ngModel: '='
		},
		restrict: "A",
		replace: true,
		template:'<div class=signature-container><canvas class=signature-pad height={{opts.height}} width={{opts.width}}></canvas><span class=\"btn btn-default btn-clear-sign\" ng-click=clear()>{{opts.clearBtn}}</span></div>',
		controller: contrFunction
	});
}]);
