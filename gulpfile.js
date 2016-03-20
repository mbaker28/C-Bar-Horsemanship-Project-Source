var gulp = require('gulp');
var less = require('gulp-less');
var watch = require('gulp-watch');
var uglify = require('gulp-uglify');
var cssNano = require('gulp-cssnano');
var del = require('del');

// Clean JS output folders
gulp.task('clean:js', function () {
    return del([
        'public/static/cbar_db/js/**/*'
    ]);
});

// Clean CSS output folders
gulp.task('clean:css', function () {
    return del([
        'public/static/cbar_db/css/**/*'
    ]);
});

// Default build
gulp.task('default', function() {
    gulp.start(['clean:css', 'clean:js', 'scripts', 'LESS', 'watch']);
});

// Minify all JavaScript files into one file
gulp.task('scripts', function(){
    return gulp.src('static_source/js/**/*.js')
    .pipe(uglify())
    .pipe(gulp.dest('public/static/cbar_db/js'));
});

// Process LESS files into CSS and minify into one file
gulp.task('LESS', function(){
    return gulp.src('static_source/less/**/*.less')
    .pipe(less())
    .pipe(cssNano())
    .pipe(gulp.dest('public/static/cbar_db/css'));
});

// Watch so we auto run when files are updated.
gulp.task('watch', function(){
    gulp.watch('static_source/js/**/*.js', ['clean:js', 'scripts']);

    gulp.watch('static_source/less/**/*.less', ['clean:css', 'LESS']);
});
