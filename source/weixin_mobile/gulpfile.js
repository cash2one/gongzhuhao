var gulp        = require('gulp');
var templateCache = require('gulp-angular-templateCache');
var browserSync = require('browser-sync').create();
var useref = require('gulp-useref');
var csso = require('gulp-csso');
var uglify = require('gulp-uglify');
var minifyHtml = require('gulp-minify-html');
var gulpif = require('gulp-if');


var TEMPLATE_HEADER = 'angular.module("<%= module %>" , ["ngResource"]).run(["$templateCache", function($templateCache) {';
var TEMPLATE_FOOTER = '}]);';


// Static server
gulp.task('browser-sync', function() {
    browserSync.init({
        server: {
            baseDir: "./"
        }
    });
    gulp.watch("*.html").on("change", browserSync.reload);

});


// template combine cache
gulp.task('template' , function(){
	gulp.src('views/*/*.html')
	.pipe(templateCache({root : 'views' , templateHeader : TEMPLATE_HEADER , templateFooter : TEMPLATE_FOOTER}))
	.pipe(gulp.dest('scripts/templates/'));
});

gulp.task('html', ['clean', 'template'],  function () {
  var assets = useref.assets({searchPath: ['.tmp', 'vendor', '.' , 'views' , 'scripts' , 'dist']});
  return gulp.src('*.html')
    .pipe(assets)
    .pipe(gulpif('*.js', uglify()))
    .pipe(gulpif('*.css', csso()))
    .pipe(assets.restore())
    .pipe(useref())
    .pipe(gulpif('*.html', minifyHtml({conditionals: true, loose: true})))
    .pipe(gulp.dest('dist'));
});

// clean task
gulp.task('clean', require('del').bind(null, ['.tmp', 'dist']));

