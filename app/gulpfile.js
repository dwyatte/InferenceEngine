var gulp = require('gulp'); 

//plugins
var jshint  = require('gulp-jshint');
var uglify  = require('gulp-uglify');
var rename  = require('gulp-rename');
var concat  = require('gulp-concat');
var inject  = require('gulp-inject');
var clean   = require('gulp-clean');
var nodemon = require('gulp-nodemon');
var merge   = require('merge-stream');

//Paths of dependencies
var paths = [
    './dist/all.min.js'
];


gulp.task('lint', function() {
    return gulp.src('dev/*.js')
        .pipe(jshint())
        .pipe(jshint.reporter('default'));
});

gulp.task('clean', function(){
    return gulp.src('dist/*')
        .pipe(clean());
});

gulp.task('buildVendorScripts', function(){
    var sigmaScripts =
        gulp.src('node_modules/sigma/build/**/**.min.js')
        .pipe(gulp.dest('dist/node_modules/sigma'));

    var ioScripts = 
        gulp.src('node_modules/socket.io/node_modules/socket.io-client/socket.io.js')
        .pipe(gulp.dest('dist/node_modules/io'));

    return merge(sigmaScripts, ioScripts);
});

gulp.task('deployData', function(){
    return gulp.src('data/data.json')
        .pipe(gulp.dest('dist/data'));
});

gulp.task('deployJS', function() {
    return gulp.src('dev/*.js')
            .pipe(concat('all.js'))
            .pipe(rename('all.min.js'))
            .pipe(uglify())
            .pipe(gulp.dest('dist'));
});

gulp.task('deployHTML', function(cb){
    var sources = gulp.src(paths, {read: false});
    return gulp.src('dev/*.html')
                .pipe(gulp.dest('dist'));
});

gulp.task('watch', function() {
    gulp.watch('dev/*.js', ['lint', 'deployJS']);
    gulp.watch('dev/*.html', ['deployHTML']);
    gulp.watch('data/data.json', ['deployData']);
});


gulp.task('injection', ['lint', 'buildVendorScripts', 'deployHTML' ,'deployJS'], function(){
    var target = gulp.src('./dist/index.html');
    return target
            .pipe(inject(gulp.src('dist/node_modules/**'), 
                {name: 'npm', relative: true}))
            .pipe(inject(gulp.src('dist/all.min.js'), {relative: true}))
            .pipe(gulp.dest('dist'));
});

gulp.task('start', ['injection', 'deployData'], function(){
    gulp.watch('data/data.json', ['deployData']);
    nodemon({
        script: 'app.js',
        ext:'js html'
    })

})

//Default build
gulp.task('default', ['injection', 'deployData']);
